#!/usr/bin/env bash
# run_on_runpod.sh -- SIM-2026-077 on a RunPod CPU pod (decision 2026-09-07: all runs on RunPod, cap 20 USD).
# Creates the pod, ships the drivers, runs the four candidates, fetches results, DELETES the pod. Idempotent
# enough to rerun a single candidate with CAND=C2. Every step prints what it did; nothing is silent.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
NAME="qw-sim077-$(date +%m%d%H%M)"
IMAGE="runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404"       # official image: sshd + registered-key injection
KEY="$HOME/.ssh/runpod_ed25519"
PUB="$(cat "$KEY.pub")"
CANDS="${CANDS:-C1 C2 C3 C4}"
CAP_HOURS="${CAP_HOURS:-12}"                                  # 12 h x ~0.96 USD/h < 20 USD cap; pod self-terminates
LOG="$HERE/runpod_sim077.log"

echo "[$(date -u +%FT%TZ)] creating CPU pod $NAME" | tee -a "$LOG"
if [ "${POD_KIND:-cpu}" = "gpu" ]; then
  # memory-adequate host for exact diagonalization at L=14 (the default CPU flavor is capped at 4 GB RAM, 2 vCPU)
  POD_JSON=$(runpodctl pod create --gpu-id "${GPU_ID:-NVIDIA RTX 2000 Ada Generation}" --cloud-type SECURE --image "$IMAGE" --name "$NAME" \
  --env "{\"PUBLIC_KEY\":\"$PUB\"}" --container-disk-in-gb 20 --ports "22/tcp" --wait --wait-timeout 15m)
else
  POD_JSON=$(runpodctl pod create --compute-type cpu --image "$IMAGE" --name "$NAME" \
  --env "{\"PUBLIC_KEY\":\"$PUB\"}" --container-disk-in-gb 20 --ports "22/tcp" --wait --wait-timeout 15m)
fi
POD_ID=$(echo "$POD_JSON" | python -c "import json,sys;print(json.load(sys.stdin)['id'])")
echo "$POD_JSON" > "$HERE/runpod_sim077_pod.json"
IP=$(echo "$POD_JSON" | python -c "import json,sys;print(json.load(sys.stdin)['ssh']['ip'])")
PORT=$(echo "$POD_JSON" | python -c "import json,sys;print(json.load(sys.stdin)['ssh']['port'])")
COST=$(echo "$POD_JSON" | python -c "import json,sys;print(json.load(sys.stdin).get('costPerHr'))")
echo "[$(date -u +%FT%TZ)] pod $POD_ID at $IP:$PORT, costPerHr=$COST" | tee -a "$LOG"
cleanup() { echo "[$(date -u +%FT%TZ)] deleting pod $POD_ID" | tee -a "$LOG"; runpodctl pod delete "$POD_ID" >/dev/null 2>&1 || true; }
trap cleanup EXIT

SSH="ssh -i $KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=20 -p $PORT root@$IP"
SCP="scp -i $KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P $PORT"
for i in $(seq 1 20); do $SSH true 2>/dev/null && break; echo "  ssh not ready ($i)"; sleep 15; done
$SSH "nproc; free -g | head -2; python3 --version; mkdir -p /workspace/tlee"
$SCP "$HERE/qw_tlee_level1.py" "$HERE/qw_tlee_candidates.py" root@$IP:/workspace/tlee/
$SSH "cd /workspace/tlee && python3 -m pip install -q --break-system-packages numpy scipy 2>&1 | tail -3; python3 -c 'import numpy,scipy;print(numpy.__version__,scipy.__version__)'"
# Each candidate runs DETACHED on the pod; this side polls every 2 minutes, fetching the partial JSON and log
# each time, so a cap, a crash, or a lost connection never loses finished settings (runs 2 and 3 did).
DEADLINE=$(( $(date +%s) + CAP_HOURS*3600 ))
for C in $CANDS; do
  echo "[$(date -u +%FT%TZ)] running $C on $POD_ID (detached)" | tee -a "$LOG"
  $SSH "cd /workspace/tlee && rm -f sim077_$C.done && nohup bash -c 'C1_LS=\"${C1_LS:-10,12,14}\" C1_HZ=\"${C1_HZ:-0.0,0.05,0.02,0.01,0.005}\" OMP_NUM_THREADS=\$(nproc) python3 qw_tlee_candidates.py --cand $C 2>&1 | grep -v Warning > sim077_$C.log; touch sim077_$C.done' >/dev/null 2>&1 </dev/null &"
  while true; do
    sleep 120
    $SCP root@$IP:/workspace/tlee/sim077_$C.log "$HERE/" 2>/dev/null || true
    $SCP root@$IP:/workspace/tlee/sim077_${C}_partial.json "$HERE/" 2>/dev/null || true
    if $SSH "test -f /workspace/tlee/sim077_$C.done" 2>/dev/null; then break; fi
    if [ $(date +%s) -gt $DEADLINE ]; then echo "  CAP reached during $C; partials fetched" | tee -a "$LOG"; break; fi
  done
  $SCP root@$IP:/workspace/tlee/sim077_$C.json "$HERE/" 2>/dev/null || echo "  no final json for $C (partial kept)" | tee -a "$LOG"
  $SCP root@$IP:/workspace/tlee/sim077_$C.log "$HERE/" 2>/dev/null || true
  [ $(date +%s) -gt $DEADLINE ] && break
done
echo "[$(date -u +%FT%TZ)] all candidates done; results in $HERE/sim077_*.json" | tee -a "$LOG"
