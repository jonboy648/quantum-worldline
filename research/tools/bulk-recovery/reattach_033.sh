#!/usr/bin/env bash
# reattach_033.sh -- re-watch a LIVE HYP-033 pod after the orchestrator (run_on_runpod_033.sh) lost its
# ssh session. Same fetch loop; on all.done it fetches, verifies the copy, then DELETES the pod.
# The pod is deleted only after a verified final fetch (or at the cap deadline), never on a failed copy.
# Usage: POD_ID=... IP=... PORT=... DEADLINE_ISO=2026-09-26T06:02:00Z ./reattach_033.sh
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SCRATCH="${SCRATCH:-$HERE/runpod_033}"
LOG="$SCRATCH/runpod_033.log"
KEY="$HOME/.ssh/runpod_ed25519"
: "${POD_ID:?}" "${IP:?}" "${PORT:?}" "${DEADLINE_ISO:?}"
DEADLINE=$(date -u -d "$DEADLINE_ISO" +%s)
stamp(){ date -u +%FT%TZ; }
SSH="ssh -i $KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=20 -o ServerAliveInterval=30 -p $PORT root@$IP"
fetch(){ $SSH "cd /workspace/hyp033 && tar czf - logs pod_console.log networks 2>/dev/null" | tar xzf - -C "$SCRATCH"; }
delete_pod(){ echo "[$(stamp)] deleting pod $POD_ID" | tee -a "$LOG"; runpodctl pod delete "$POD_ID" 2>&1 | tail -1 | tee -a "$LOG"
  sleep 10; runpodctl pod list 2>&1 | grep -q "$POD_ID" && echo "[$(stamp)] WARNING: pod still listed" | tee -a "$LOG" || echo "[$(stamp)] pod gone from list" | tee -a "$LOG"; }

echo "[$(stamp)] reattach: watching $POD_ID at $IP:$PORT, deadline $DEADLINE_ISO" | tee -a "$LOG"
while true; do
  fetch 2>/dev/null || echo "[$(stamp)] fetch failed (ssh?); retrying" | tee -a "$LOG"
  echo "[$(stamp)] $(grep -c finished "$SCRATCH/logs/pod.log" 2>/dev/null) finished" | tee -a "$LOG"
  $SSH "test -f /workspace/hyp033/all.done" 2>/dev/null && break
  [ "$(date +%s)" -gt "$DEADLINE" ] && { echo "[$(stamp)] CAP DEADLINE REACHED" | tee -a "$LOG"; break; }
  sleep 600
done

# final fetch, verified: local pod.log must match the pod's byte for byte
for i in 1 2 3 4 5; do
  if fetch && [ "$($SSH 'md5sum < /workspace/hyp033/logs/pod.log' | cut -c1-32)" = "$(md5sum < "$SCRATCH/logs/pod.log" | cut -c1-32)" ]; then
    echo "[$(stamp)] final fetch verified; $(ls -d "$SCRATCH"/networks/*/ | wc -l) network dirs local" | tee -a "$LOG"
    tail -3 "$SCRATCH/pod_console.log" | tee -a "$LOG"
    delete_pod; exit 0
  fi
  echo "[$(stamp)] final fetch attempt $i failed" | tee -a "$LOG"; sleep 60
done
echo "[$(stamp)] FINAL FETCH NOT VERIFIED -- pod $POD_ID LEFT RUNNING for manual fetch" | tee -a "$LOG"; exit 2
