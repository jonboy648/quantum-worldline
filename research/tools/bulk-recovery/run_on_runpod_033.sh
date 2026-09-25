#!/usr/bin/env bash
# run_on_runpod_033.sh -- HYP-033 registered grid on a RunPod pod (PREREGISTRATION-HYP033.md rule 4,
# amended 2026-09-22 by Jon: RunPod, not local). Creates the pod through the SIM-078 availability ladder,
# verifies costPerHr and gpuCount before anything runs, ships MERAKit + the drivers, runs hyp033_pod.sh
# detached on the pod, fetches results every few minutes, and DELETES the pod on every exit path or at
# the cap. Cap: 25 USD -> CAP_HOURS = 25 / costPerHr, computed after the price is known.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SCRATCH="${SCRATCH:-$HERE/runpod_033}"
mkdir -p "$SCRATCH/networks"
NAME="qw-hyp033-$(date +%m%d%H%M)"
KEY="$HOME/.ssh/runpod_ed25519"
PUB="$(cat "$KEY.pub")"
CAP_USD="${CAP_USD:-25}"
LOG="$SCRATCH/runpod_033.log"
MERAKIT_TGZ="${MERAKIT_TGZ:?path to merakit.tgz}"
stamp(){ date -u +%FT%TZ; }

BOOT='apt-get update -qq && apt-get install -y -qq openssh-server python3-pip python3-numpy python3-scipy curl >/dev/null 2>&1; mkdir -p /root/.ssh /run/sshd && printf "%s
" "$PUBLIC_KEY" > /root/.ssh/authorized_keys && chmod 700 /root/.ssh && chmod 600 /root/.ssh/authorized_keys; /usr/sbin/sshd -D'
# Ladder (SIM-078 lessons): CPU pods were unavailable account-wide on 2026-09-09; GPU-class hosts carry the
# vCPUs and are cheaper per vCPU (RTX 4000 Ada x16 = 0.28 USD/h). We buy cores and RAM, the GPU idles.
# Rungs "kind:type:vcpu:cloud". Every GPU rung asks for >= 40 GB RAM; NJOBS is sized from the RAM we get.
# Stock was "Low" everywhere on 2026-09-22 and the first pod's host vanished between two attempts, so
# the whole ladder is retried every 3 minutes for up to RETRY_MIN minutes.
LADDER="${LADDER:-gpu:NVIDIA RTX 4000 Ada Generation:16:SECURE;gpu:NVIDIA RTX A4500:16:SECURE;gpu:NVIDIA RTX A6000:16:SECURE;gpu:NVIDIA A40:16:SECURE;gpu:NVIDIA RTX 2000 Ada Generation:16:SECURE;gpu:NVIDIA RTX A6000:16:COMMUNITY;gpu:NVIDIA GeForce RTX 4090:16:COMMUNITY;gpu:NVIDIA GeForce RTX 3090:16:COMMUNITY;gpu:NVIDIA RTX A5000:16:COMMUNITY;cpu:cpu5c:32:SECURE;cpu:cpu3c:32:SECURE;cpu:cpu5g:32:SECURE;cpu:cpu5c:16:SECURE;gpu:NVIDIA RTX 4000 Ada Generation:12:SECURE;gpu:NVIDIA RTX A4500:12:SECURE;gpu:NVIDIA RTX A6000:12:COMMUNITY;gpu:NVIDIA GeForce RTX 4090:12:COMMUNITY;gpu:NVIDIA L4:16:SECURE;gpu:NVIDIA RTX 6000 Ada Generation:16:SECURE;gpu:NVIDIA L40S:16:SECURE}"
RETRY_MIN="${RETRY_MIN:-180}"
RETRY_END=$(( $(date +%s) + RETRY_MIN*60 ))
POD_ID=""
while [ -z "$POD_ID" ]; do
OLDIFS="$IFS"; IFS=';'
for COMBO in $LADDER; do
  KIND="${COMBO%%:*}"; REST="${COMBO#*:}"; CLOUD="${REST##*:}"; REST="${REST%:*}"; WHAT="${REST%:*}"; NV="${REST##*:}"
  REQ=$(PUB="$PUB" NAME="$NAME" BOOT="$BOOT" VCPU="$NV" WHAT="$WHAT" KIND="$KIND" CLOUD="$CLOUD" python -c '
import json, os
k, what, nv, cloud = os.environ["KIND"], os.environ["WHAT"], int(os.environ["VCPU"]), os.environ["CLOUD"]
body = {"name": os.environ["NAME"], "imageName": "ubuntu:22.04", "containerDiskInGb": 30, "ports": ["22/tcp"],
        "env": {"PUBLIC_KEY": os.environ["PUB"]}, "dockerStartCmd": ["bash", "-c", os.environ["BOOT"]], "cloudType": cloud}
if k == "cpu":
    body.update(computeType="CPU", cpuFlavorIds=[what], vcpuCount=nv)
else:
    body.update(computeType="GPU", gpuTypeIds=[what], gpuCount=1, minVCPUPerGPU=nv, minRAMPerGPU=40)
print(json.dumps(body))')
  POD_JSON=$(curl -s -X POST "https://rest.runpod.io/v1/pods" -H "Authorization: Bearer $RUNPOD_API_KEY" -H "Content-Type: application/json" -d "$REQ")
  POD_ID=$(echo "$POD_JSON" | python -c "import json,sys;d=json.load(sys.stdin);print(d.get('id') or '')" 2>/dev/null || echo "")
  if [ -n "$POD_ID" ]; then
    echo "[$(stamp)] got $KIND '$WHAT' x $NV vCPU ($CLOUD) -> pod $POD_ID" | tee -a "$LOG"; echo "$POD_JSON" > "$SCRATCH/pod.json"; break
  fi
  echo "  $KIND '$WHAT' x $NV $CLOUD unavailable: $(echo "$POD_JSON" | head -c 100)" | tee -a "$LOG"
  sleep 2
done
IFS="$OLDIFS"
if [ -z "$POD_ID" ]; then
  [ $(date +%s) -gt $RETRY_END ] && { echo "[$(stamp)] pod create FAILED on every rung for $RETRY_MIN min; giving up" | tee -a "$LOG"; exit 1; }
  echo "[$(stamp)] every rung unavailable; retrying in 3 min" | tee -a "$LOG"; sleep 180
fi
done

cleanup(){ echo "[$(stamp)] deleting pod $POD_ID" | tee -a "$LOG"
  curl -s -X DELETE -H "Authorization: Bearer $RUNPOD_API_KEY" "https://rest.runpod.io/v1/pods/$POD_ID" >/dev/null 2>&1 || true
  runpodctl pod delete "$POD_ID" >/dev/null 2>&1 || true
  sleep 5; curl -s -o /dev/null -w "  pod GET after delete: HTTP %{http_code}\n" -H "Authorization: Bearer $RUNPOD_API_KEY" "https://rest.runpod.io/v1/pods/$POD_ID" | tee -a "$LOG"; }
trap cleanup EXIT; trap 'exit 1' INT TERM

for i in $(seq 1 40); do
  INFO=$(curl -s -H "Authorization: Bearer $RUNPOD_API_KEY" "https://rest.runpod.io/v1/pods/$POD_ID")
  read -r COST GPUN VC RAM IP PORT <<EOF2
$(echo "$INFO" | python -c "
import json,sys
d=json.load(sys.stdin); port=''
for p in (d.get('portMappings') or {}).items():
    if p[0]=='22': port=p[1]
print(d.get('costPerHr'), d.get('gpuCount'), d.get('vcpuCount') or d.get('vcpuCountPerGpu') or '?', d.get('memoryInGb') or '?', d.get('publicIp') or '-', port or '-')")
EOF2
  [ "$IP" != "-" ] && [ "$PORT" != "-" ] && break
  echo "  waiting for pod ($i): cost=$COST gpu=$GPUN vcpu=$VC ram=$RAM"; sleep 15
done
echo "[$(stamp)] pod $POD_ID costPerHr=$COST gpuCount=$GPUN vcpu=$VC ramGB=$RAM ssh $IP:$PORT" | tee -a "$LOG"
case "$COMBO" in cpu:*) if [ "$GPUN" != "0" ] && [ "$GPUN" != "None" ]; then echo "REFUSING: cpu rung returned gpuCount=$GPUN" | tee -a "$LOG"; exit 1; fi;; esac
CAP_HOURS=$(python -c "print(round($CAP_USD/float('$COST'),2))")
# full-matrix (C-HAAR) heavy points need ~16 GB each: size the grid parallelism from the RAM we got
NJOBS="${NJOBS:-$(python -c "print(max(1, min(4, int(float('$RAM')//18))))")}"
echo "[$(stamp)] NJOBS=$NJOBS from ramGB=$RAM" | tee -a "$LOG"
DEADLINE=$(( $(date +%s) + $(python -c "print(int($CAP_HOURS*3600))") ))
echo "[$(stamp)] cap $CAP_USD USD at $COST USD/h = $CAP_HOURS h; deadline $(date -u -d @$DEADLINE +%FT%TZ 2>/dev/null || echo $DEADLINE)" | tee -a "$LOG"

SSH="ssh -i $KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=20 -p $PORT root@$IP"
SCP="scp -i $KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -P $PORT"
for i in $(seq 1 30); do $SSH true 2>/dev/null && break; echo "  ssh not ready ($i)"; sleep 15; done
$SSH "nproc; free -g | head -2; python3 --version; mkdir -p /workspace/hyp033" | tee -a "$LOG"
$SCP "$MERAKIT_TGZ" "$HERE/g0_feasibility.py" "$HERE/hyp033_grid.py" "$HERE/hyp033_haar.py" "$HERE/hyp033_pod.sh" root@$IP:/workspace/hyp033/
$SSH "cd /workspace/hyp033 && tar xzf merakit.tgz --no-same-owner --no-same-permissions && for f in *.sh *.py MERAKit.jl/*.jl; do tr -d '\r' < \"\$f\" > p.tmp && mv p.tmp \"\$f\"; done && chmod +x hyp033_pod.sh \
  && python3 -m pip install -q numpy scipy opt_einsum networkx 2>&1 | tail -2 \
  && python3 -c 'import numpy,scipy,opt_einsum,networkx;print(\"numpy\",numpy.__version__,\"scipy\",scipy.__version__)' \
  && curl -sL https://julialang-s3.julialang.org/bin/linux/x64/1.8/julia-1.8.5-linux-x86_64.tar.gz | tar xz && julia-1.8.5/bin/julia --version" | tee -a "$LOG"
# hard verification of the setup: nothing billable proceeds on a half-installed pod
$SSH "cd /workspace/hyp033 && python3 -c 'import numpy,scipy,opt_einsum,networkx' && julia-1.8.5/bin/julia --version && test -f MERAKit.jl/Manifest.toml"   || { echo "[$(stamp)] SETUP INCOMPLETE -- aborting (pod is deleted by the trap)" | tee -a "$LOG"; exit 1; }
echo "[$(stamp)] selftests on the pod" | tee -a "$LOG"
$SSH "cd /workspace/hyp033 && python3 hyp033_grid.py --selftest haar" | tee -a "$LOG" || { echo "[$(stamp)] SELFTEST FAILED -- aborting" | tee -a "$LOG"; exit 1; }

# RESUME_LOCAL=1: a previous pod's host died after stage 1+2 and the first-network gate. Ship the networks
# already fetched to $SCRATCH/networks (tensors + any partial JSON; the grid skips points already present)
# and mark stages 1, 2 and gate0 done, so the registered networks are reused, never re-optimized.
if [ "${RESUME_LOCAL:-0}" = 1 ]; then
  echo "[$(stamp)] RESUME_LOCAL: uploading $(ls -d "$SCRATCH"/networks/*/ | wc -l) fetched networks" | tee -a "$LOG"
  tar czf - -C "$SCRATCH" networks | $SSH "cd /workspace/hyp033 && tar xzf - --no-same-owner && touch stage1.done stage2.done gate0.done && ls -d networks/*/ | wc -l" | tee -a "$LOG"
fi
echo "[$(stamp)] launching hyp033_pod.sh detached (NJOBS=${NJOBS:-3} SEEDS6=${SEEDS6:-8} SEEDS8=${SEEDS8:-4} SEEDS_GAP=${SEEDS_GAP:-8})" | tee -a "$LOG"
# pod-side watchdog: if this orchestrator dies, the container still exits at the cap (kill PID 1 = sshd)
CAP_SEC=$(( DEADLINE - $(date +%s) ))
$SSH "nohup bash -c 'sleep $CAP_SEC; kill 1' >/dev/null 2>&1 </dev/null &"
$SSH "cd /workspace/hyp033 && rm -f all.done && POD_ID=$POD_ID NPROC_OVERRIDE=$VC NJOBS=${NJOBS:-3} JULIA_PAR=${JULIA_PAR:-8} SEEDS6=${SEEDS6:-8} SEEDS8=${SEEDS8:-4} SEEDS_GAP=${SEEDS_GAP:-8} MAXITER=${MAXITER:-2500} nohup bash -c './hyp033_pod.sh > pod_console.log 2>&1; touch all.done' >/dev/null 2>&1 </dev/null &"

fetch(){ $SSH "cd /workspace/hyp033 && tar czf - logs pod_console.log networks 2>/dev/null" | tar xzf - -C "$SCRATCH" 2>/dev/null || true; }
while true; do
  sleep 180; fetch
  tail -2 "$SCRATCH/pod_console.log" 2>/dev/null | sed 's/^/    /'
  $SSH "test -f /workspace/hyp033/all.done" 2>/dev/null && break
  if [ $(date +%s) -gt $DEADLINE ]; then echo "[$(stamp)] CAP REACHED; partials fetched" | tee -a "$LOG"; break; fi
  if ! $SSH true 2>/dev/null; then echo "[$(stamp)] ssh lost; retrying" | tee -a "$LOG"; fi
done
fetch
# final: also fetch the network tensors (small: ~200 KB each) for the archive
$SSH "cd /workspace/hyp033 && tar czf - networks 2>/dev/null" | tar xzf - -C "$SCRATCH" 2>/dev/null || true
echo "[$(stamp)] finished; results in $SCRATCH/networks" | tee -a "$LOG"
