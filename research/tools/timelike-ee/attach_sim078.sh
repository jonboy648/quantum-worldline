#!/usr/bin/env bash
# attach_sim078.sh -- reattach to a live SIM-078 pod after the orchestrator died, finish the gate
# stage, fetch everything, and DELETE the pod. The first runner was launched with nohup from a tool
# call and was killed with its parent, leaving the pod billing unattended; this one is harness-tracked
# and deletes the pod on every exit path.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
POD_ID="${POD_ID:?set POD_ID}"; IP="${IP:?set IP}"; PORT="${PORT:?set PORT}"
KEY="$HOME/.ssh/runpod_ed25519"
DEADLINE=$(( $(date +%s) + ${CAP_MIN:-90}*60 ))
LOG="$HERE/runpod_sim078.log"
SSH="ssh -i $KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=20 -p $PORT root@$IP"
SCP="scp -i $KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P $PORT"
cleanup(){ echo "[$(date -u +%FT%TZ)] deleting pod $POD_ID" | tee -a "$LOG"
  curl -s -X DELETE -H "Authorization: Bearer $RUNPOD_API_KEY" "https://rest.runpod.io/v1/pods/$POD_ID" >/dev/null 2>&1
  runpodctl pod delete "$POD_ID" >/dev/null 2>&1; }
trap cleanup EXIT INT TERM

fetch(){ for f in sim078_gates.log sim078_gates.json sim078_g2scan.log sim078_g2scan.json; do
  $SCP "root@$IP:/workspace/tlee/$f" "$HERE/" >/dev/null 2>&1; done; }

echo "[$(date -u +%FT%TZ)] attached to $POD_ID; waiting for the gate stage" | tee -a "$LOG"
while ! $SSH "test -f /workspace/tlee/sim078_gates.done" >/dev/null 2>&1; do
  sleep 60; fetch
  [ $(date +%s) -gt $DEADLINE ] && { echo "cap reached during gates" | tee -a "$LOG"; exit 1; }
done
fetch
echo "[$(date -u +%FT%TZ)] gate stage finished" | tee -a "$LOG"

# G2 failed at chi=128. The registered bar (1e-8) is NOT being changed; the question is whether the
# calculation can be made good enough to meet it, the same way fourth-order Trotter was the answer
# for G1's 1e-6. At delta=0 there is no damping, so real-time operator entanglement is the cost.
echo "[$(date -u +%FT%TZ)] G2 bond-dimension scan (gate unchanged, chi raised)" | tee -a "$LOG"
$SSH "cd /workspace/tlee && rm -f sim078_g2scan.done && nohup bash -c 'python3 - <<PYEOF > sim078_g2scan.log 2>&1
import json, numpy as np, qw_tlee_mpo as m
out={}
for L in (12,16,24):
    for chi in (128,256,512):
        try:
            got,st=m.S_of(L,0.0,5.0,0.0,m.windows(m.V*5.0)[0],chi,0.1)
            mx=float(max(abs(got[t].imag) for t in got))
            out[f\"L{L}_chi{chi}\"]={\"max_abs_Im\":mx,\"pass\":bool(mx<1e-8),\"max_chi\":st[\"max_chi\"],\"disc\":st[\"max_disc\"],\"secs\":st[\"secs_evolve\"]}
            print(f\"G2 L={L} chi={chi}: max|Im S| = {mx:.3e} {\\\"ok\\\" if mx<1e-8 else \\\"FAIL\\\"} disc={st[\\\"max_disc\\\"]:.1e} {st[\\\"secs_evolve\\\"]:.0f}s\",flush=True)
        except Exception as e:
            out[f\"L{L}_chi{chi}\"]={\"error\":str(e)}; print(f\"G2 L={L} chi={chi}: ERROR {e}\",flush=True)
        json.dump(out,open(\"sim078_g2scan.json\",\"w\"),indent=1)
PYEOF
touch sim078_g2scan.done' >/dev/null 2>&1 </dev/null &"
while ! $SSH "test -f /workspace/tlee/sim078_g2scan.done" >/dev/null 2>&1; do
  sleep 60; fetch
  [ $(date +%s) -gt $DEADLINE ] && { echo "cap reached during the G2 scan; partials fetched" | tee -a "$LOG"; exit 1; }
done
fetch
echo "[$(date -u +%FT%TZ)] G2 scan finished" | tee -a "$LOG"
