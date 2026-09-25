"""Fetch R5 results, stop the R5 pod, surface verdict.

Designed to be run by Windows Task Scheduler ~8-10 hr after launch.
Idempotent: if results aren't ready yet, exits with rc=1 so Scheduler can retry.
"""
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

API_KEY = os.environ.get("RUNPOD_API_KEY")
if not API_KEY:
    sys.exit("RUNPOD_API_KEY not set. Export it before running: "
             "export RUNPOD_API_KEY=rpa_... (PowerShell: $env:RUNPOD_API_KEY='rpa_...')")
SESSION_PATH = Path("D:/quantum-worldline/research/data/builds/runpod_r5_session.json")
SESSION = json.loads(SESSION_PATH.read_text())
HOST = SESSION["ssh_host"]
PORT = str(SESSION["ssh_port"])
USER = SESSION["ssh_user"]
POD_ID = SESSION["pod_id"]
LOCAL_RESULTS = Path(SESSION["results_fetch_local_path"])
LOCAL_RESULTS.mkdir(parents=True, exist_ok=True)

SSH_OPTS = [
    "-o", "StrictHostKeyChecking=no",
    "-o", "UserKnownHostsFile=/dev/null",
    "-o", "ConnectTimeout=20",
    "-p", PORT,
]


def ssh(cmd):
    return subprocess.run(
        ["ssh", *SSH_OPTS, f"{USER}@{HOST}", cmd],
        capture_output=True, text=True, timeout=120,
    )


def scp_from(remote, local):
    return subprocess.run(
        ["scp", *SSH_OPTS, f"{USER}@{HOST}:{remote}", str(local)],
        capture_output=True, text=True, timeout=300,
    )


def stop_pod():
    req = urllib.request.Request(
        f"https://rest.runpod.io/v1/pods/{POD_ID}/stop",
        headers={"Authorization": f"Bearer {API_KEY}"},
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.status, resp.read().decode()[:500]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:500]


def main():
    print(f"=== R5 fetch+teardown for pod {POD_ID} ({HOST}:{PORT}) ===")

    print("\n=== Checking pod state ===")
    r = ssh(
        "ps -ef | grep -E 'run_r5|HYP-2026' | grep -v grep | head -3; "
        "echo '--- log tail ---'; "
        "tail -40 /workspace/qw-r5/results/run_r5.log 2>/dev/null || "
        "tail -40 /workspace/qw-r5/run_r5_outer.log 2>/dev/null"
    )
    print(r.stdout)
    if r.returncode != 0:
        print("SSH failed:", r.stderr[:500])
        return 2

    print("\n=== Checking for results tarball ===")
    r = ssh(
        "ls -la /workspace/qw-r5/results/ 2>/dev/null; "
        "ls /workspace/qw-r5/results/hyp-017-r5-results.tar.gz 2>/dev/null && echo EXISTS"
    )
    print(r.stdout)
    if "EXISTS" not in r.stdout:
        print("\nResults tarball not yet ready. Pod still running. Re-schedule wakeup.")
        return 1

    print("\n=== Fetching results ===")
    r = scp_from(
        "/workspace/qw-r5/results/hyp-017-r5-results.tar.gz",
        LOCAL_RESULTS / "hyp-017-r5-results.tar.gz",
    )
    if r.returncode != 0:
        print("scp failed:", r.stderr[:500])
        return 2
    print(f"Downloaded to {LOCAL_RESULTS}")

    print("\n=== Extracting ===")
    subprocess.run(
        ["tar", "-xzf", "hyp-017-r5-results.tar.gz"],
        cwd=LOCAL_RESULTS, check=True,
    )
    for p in sorted(LOCAL_RESULTS.glob("*.json")):
        print(f"  {p.name}")
    for p in sorted(LOCAL_RESULTS.glob("*.png")):
        print(f"  {p.name}")
    for p in sorted(LOCAL_RESULTS.glob("*.log")):
        print(f"  {p.name}")

    print("\n=== Stopping pod ===")
    code, body = stop_pod()
    print(f"  HTTP {code}: {body[:300]}")

    print("\n=== R5 verdict summary ===")
    main_json = LOCAL_RESULTS / "HYP-2026-017-results.json"
    if main_json.exists():
        try:
            d = json.loads(main_json.read_text())
            alpha_block = d.get("alpha_fit", {})
            forces = d.get("forces", {})
            tee = d.get("tee", {})
            print(f"\n{main_json.name}:")
            print(f"  alpha_fit: {alpha_block}")
            print(f"  S_topo:    {tee.get('S_topo', 'n/a')} +/- {tee.get('S_topo_err', 'n/a')}")
            print(f"  forces:    {forces}")
            print(f"  wall_s:    {d.get('wall_time_s', '?')}")
            # Structural gate: did we get to a finite alpha and finite S_topo?
            alpha = alpha_block.get("alpha")
            stopo = tee.get("S_topo")
            ok_alpha = (
                alpha is not None
                and isinstance(alpha, (int, float))
                and alpha == alpha  # not nan
                and abs(alpha) != float("inf")
            )
            ok_tee = (
                stopo is not None
                and isinstance(stopo, (int, float))
                and stopo == stopo
                and abs(stopo) != float("inf")
            )
            print(f"\nGate: alpha finite = {ok_alpha}, S_topo finite = {ok_tee}")
            if ok_alpha and ok_tee:
                print("R5 STRUCTURAL GATE: PASS")
            else:
                print("R5 STRUCTURAL GATE: FAIL (non-finite values; investigate log)")
        except Exception as e:
            print(f"  parse failed -- {e}")
    else:
        print(f"  No {main_json.name} found in archive")

    return 0


if __name__ == "__main__":
    sys.exit(main())
