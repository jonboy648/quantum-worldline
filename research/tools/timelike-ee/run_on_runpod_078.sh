#!/usr/bin/env bash
# run_on_runpod_078.sh -- SIM-2026-078 (PREREGISTRATION-HYP032-B.md) on a RunPod CPU pod.
# All HYP-032 computation runs here, none locally, per the standing decision. Cap 25 USD.
# Order is fixed by the pre-registration: G1 and G2 first, and the grid runs ONLY if they pass.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME="qw-sim078-$(date +%m%d%H%M)"
IMAGE="runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404"
KEY="$HOME/.ssh/runpod_ed25519"
PUB="$(cat "$KEY.pub")"
SETTINGS="${SETTINGS:-A B C}"
CAP_HOURS="${CAP_HOURS:-8}"
LOG="$HERE/runpod_sim078.log"

# runpodctl pod create has no vCPU or CPU-flavor flag, so creation goes through REST v2, which does.
# cpu5c = Compute-Optimized, ramMultiplier 2, so 32 vCPU brings 64 GB -- the pre-registered shape.
# Image is ubuntu:22.04, NOT a CUDA image: memory [runpod-cpu-pod-gotcha] records that REST /pods
# with a CUDA image provisions a GPU box regardless of cpuFlavorIds. gpuCount is verified below.
echo "[$(date -u +%FT%TZ)] creating CPU pod $NAME (${VCPU:-32} vCPU, cpu5c)" | tee -a "$LOG"
BOOT='apt-get update -qq && apt-get install -y -qq openssh-server python3-pip python3-numpy python3-scipy >/dev/null 2>&1; mkdir -p /root/.ssh /run/sshd && printf "%s
" "$PUBLIC_KEY" > /root/.ssh/authorized_keys && chmod 700 /root/.ssh && chmod 600 /root/.ssh/authorized_keys; /usr/sbin/sshd -D'
# Availability ladder. 32 vCPU compute-optimised was sold out on the first attempt, exactly as the
# RTX 2000 Ada was for SIM-077. Order: most cores first, then relax the flavor, then the core count.
# Anything at or above 8 vCPU is still a large speed-up over SIM-077's 2, so the run is not blocked.
# Availability ladder. Rungs are "kind:flavor-or-gpu:vcpu".
#  - vcpuCount must be a POWER OF TWO on CPU pods (24 is rejected outright, not just unavailable).
#  - On 2026-09-09 every CPU flavor was unavailable in BOTH clouds at 4, 8, 16 and 32 vCPU, so the
#    CPU rungs can all miss. GPU-class hosts stay available and carry the vCPUs we actually need;
#    SIM-077 ended up on them for the same reason. We do not use the GPU, only its cores.
# Rungs are separated by ';' because GPU type ids contain spaces.
LADDER="${LADDER:-cpu:cpu5c:32;cpu:cpu3c:32;cpu:cpu5g:32;cpu:cpu5c:16;cpu:cpu3c:16;cpu:cpu5c:8;gpu:NVIDIA RTX A4500:16;gpu:NVIDIA RTX 4000 Ada Generation:16;gpu:NVIDIA RTX 2000 Ada Generation:16;gpu:NVIDIA A40:16;gpu:NVIDIA RTX A6000:16;gpu:NVIDIA RTX A4500:8;gpu:NVIDIA RTX 4000 Ada Generation:8;gpu:NVIDIA RTX A6000:8}"
POD_ID=""
OLDIFS="$IFS"; IFS=';'
for COMBO in $LADDER; do
  KIND="${COMBO%%:*}"; REST="${COMBO#*:}"; WHAT="${REST%:*}"; NV="${REST##*:}"
  REQ=$(PUB="$PUB" NAME="$NAME" BOOT="$BOOT" VCPU="$NV" WHAT="$WHAT" KIND="$KIND" python -c '
import json, os
k, what, nv = os.environ["KIND"], os.environ["WHAT"], int(os.environ["VCPU"])
body = {"name": os.environ["NAME"], "imageName": "ubuntu:22.04",
        "containerDiskInGb": 20, "ports": ["22/tcp"],
        "env": {"PUBLIC_KEY": os.environ["PUB"]},
        "dockerStartCmd": ["bash", "-c", os.environ["BOOT"]]}
if k == "cpu":
    body.update(computeType="CPU", cpuFlavorIds=[what], vcpuCount=nv, cloudType="SECURE")
else:
    body.update(computeType="GPU", gpuTypeIds=[what], gpuCount=1, minVCPUPerGPU=nv)
print(json.dumps(body))')
  POD_JSON=$(curl -s -X POST "https://rest.runpod.io/v1/pods"     -H "Authorization: Bearer $RUNPOD_API_KEY" -H "Content-Type: application/json" -d "$REQ")
  POD_ID=$(echo "$POD_JSON" | python -c "import json,sys;d=json.load(sys.stdin);print(d.get('id') or '')" 2>/dev/null || echo "")
  if [ -n "$POD_ID" ]; then
    echo "[$(date -u +%FT%TZ)] got $KIND '$WHAT' x $NV vCPU -> pod $POD_ID" | tee -a "$LOG"
    echo "$POD_JSON" > "$HERE/runpod_sim078_pod.json"
    break
  fi
  echo "  $KIND '$WHAT' x $NV unavailable: $(echo "$POD_JSON" | head -c 120)" | tee -a "$LOG"
done
IFS="$OLDIFS"
[ -z "$POD_ID" ] && { echo "pod create FAILED on every rung of the ladder" | tee -a "$LOG"; exit 1; }

# Verify what we actually got BEFORE running anything -- costPerHr and gpuCount, per the gotcha.
for i in $(seq 1 40); do
  INFO=$(curl -s -H "Authorization: Bearer $RUNPOD_API_KEY" "https://rest.runpod.io/v1/pods/$POD_ID")
  read -r COST GPUN VC RAM IP PORT <<EOF2
$(echo "$INFO" | python -c "
import json,sys
d=json.load(sys.stdin)
ip=port=''
for p in (d.get('portMappings') or {}).items():
    if p[0]=='22': port=p[1]
ip = d.get('publicIp') or ''
print(d.get('costPerHr'), d.get('gpuCount'), d.get('vcpuCount') or d.get('vcpuCountPerGpu') or '?', d.get('memoryInGb') or '?', ip or '-', port or '-')")
EOF2
  [ "$IP" != "-" ] && [ "$PORT" != "-" ] && break
  echo "  waiting for pod ($i): cost=$COST gpu=$GPUN vcpu=$VC ram=$RAM"; sleep 15
done
echo "[$(date -u +%FT%TZ)] pod $POD_ID  costPerHr=$COST gpuCount=$GPUN vcpu=$VC ramGB=$RAM  ssh $IP:$PORT" | tee -a "$LOG"
# A GPU-class host is an accepted outcome here (we bought its cores, not its GPU) but it must be
# a DELIBERATE one: refuse only if a cpu: rung somehow yielded a GPU box, which is the CUDA-image gotcha.
case "$COMBO" in cpu:*)
  if [ "$GPUN" != "0" ] && [ "$GPUN" != "None" ]; then
    echo "REFUSING TO RUN: a cpu rung returned gpuCount=$GPUN (the CUDA-image gotcha). Deleting." | tee -a "$LOG"
    curl -s -X DELETE -H "Authorization: Bearer $RUNPOD_API_KEY" "https://rest.runpod.io/v1/pods/$POD_ID" >/dev/null; exit 1
  fi;;
esac
if [ "$GPUN" != "0" ] && [ "$GPUN" != "None" ]; then
  echo "  NOTE: running on a GPU-class host for its $VC vCPUs; the GPU is unused. costPerHr=$COST" | tee -a "$LOG"
fi

cleanup(){ echo "[$(date -u +%FT%TZ)] deleting pod $POD_ID" | tee -a "$LOG";
  curl -s -X DELETE -H "Authorization: Bearer $RUNPOD_API_KEY" "https://rest.runpod.io/v1/pods/$POD_ID" >/dev/null 2>&1 || true;
  runpodctl pod delete "$POD_ID" >/dev/null 2>&1 || true; }
trap cleanup EXIT

SSH="ssh -i $KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=20 -p $PORT root@$IP"
SCP="scp -i $KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P $PORT"
for i in $(seq 1 20); do $SSH true 2>/dev/null && break; echo "  ssh not ready ($i)"; sleep 15; done
$SSH "nproc; free -g | head -2; python3 --version; mkdir -p /workspace/tlee"
$SCP "$HERE/qw_tlee_level1.py" "$HERE/qw_tlee_candidates.py" "$HERE/qw_tlee_mpo.py" root@$IP:/workspace/tlee/
$SSH "python3 -m pip install -q --break-system-packages numpy scipy 2>&1 | tail -2; python3 -c 'import numpy,scipy;print(\"numpy\",numpy.__version__,\"scipy\",scipy.__version__)'"

fetch(){ for f in "$@"; do $SCP root@$IP:/workspace/tlee/$f "$HERE/" 2>/dev/null || true; done; }
detach(){  # $1 tag, $2 command -- detached, so a dropped connection never loses finished work
  $SSH "cd /workspace/tlee && rm -f $1.done && nohup bash -c '$2 > $1.log 2>&1; touch $1.done' >/dev/null 2>&1 </dev/null &"
}
wait_for(){ # $1 tag, $2.. files to fetch every 2 min
  local tag="$1"; shift
  while true; do
    sleep 120; fetch "$tag.log" "$@"
    $SSH "test -f /workspace/tlee/$tag.done" 2>/dev/null && break
    [ $(date +%s) -gt $DEADLINE ] && { echo "  CAP reached during $tag; partials fetched" | tee -a "$LOG"; return 1; }
  done
  fetch "$tag.log" "$@"; return 0
}
DEADLINE=$(( $(date +%s) + CAP_HOURS*3600 ))

echo "[$(date -u +%FT%TZ)] G1 + G2 (the grid does not start unless both pass)" | tee -a "$LOG"
detach sim078_gates "python3 qw_tlee_mpo.py --gate all --chi 128"
wait_for sim078_gates sim078_gates.json || exit 1
if ! grep -q "GATES: PASS" "$HERE/sim078_gates.log"; then
  echo "[$(date -u +%FT%TZ)] GATES FAILED -- stopping. See sim078_gates.log/json." | tee -a "$LOG"; exit 1
fi
echo "[$(date -u +%FT%TZ)] gates PASS" | tee -a "$LOG"

for S in $SETTINGS; do
  echo "[$(date -u +%FT%TZ)] setting $S" | tee -a "$LOG"
  detach "sim078_setting$S" "python3 qw_tlee_mpo.py --run --setting $S --chi 128 --dbeta 0.25"
  wait_for "sim078_setting$S" "sim078_setting$S.json" || break
done
echo "[$(date -u +%FT%TZ)] done; results in $HERE/sim078_*.json" | tee -a "$LOG"
