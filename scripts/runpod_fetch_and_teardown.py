"""Fetch RunPod results, stop the pod, surface verdict.

Run by the scheduled wakeup ~8 hr after launch.
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
SESSION = json.loads(Path("D:/quantum-worldline/research/data/builds/runpod_session.json").read_text())
HOST = SESSION["ssh_host"]
PORT = str(SESSION["ssh_port"])
USER = SESSION["ssh_user"]
POD_ID = SESSION["pod_id"]
LOCAL_RESULTS = Path(SESSION["results_fetch_local_path"])
LOCAL_RESULTS.mkdir(parents=True, exist_ok=True)

SSH_OPTS = ["-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", "-p", PORT]


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
    print("=== Checking pod state ===")
    r = ssh("ps aux | grep -E 'run_all|validator' | grep -v grep | head -5; echo --- log tail ---; tail -30 /workspace/qw-validator/run_all.log")
    print(r.stdout)
    if r.returncode != 0:
        print("SSH failed:", r.stderr[:500])
        return 2

    print("\n=== Checking for results tarball ===")
    r = ssh("ls -la /workspace/qw-validator/results/ 2>/dev/null; ls /workspace/qw-validator/results/hyp-017-validator-results.tar.gz 2>/dev/null && echo EXISTS")
    print(r.stdout)
    if "EXISTS" not in r.stdout:
        print("\nResults tarball not yet ready. Pod still running. Re-schedule wakeup.")
        return 1

    print("\n=== Fetching results ===")
    r = scp_from("/workspace/qw-validator/results/hyp-017-validator-results.tar.gz",
                 LOCAL_RESULTS / "hyp-017-validator-results.tar.gz")
    if r.returncode != 0:
        print("scp failed:", r.stderr[:500])
        return 2
    print(f"Downloaded to {LOCAL_RESULTS}")

    print("\n=== Extracting ===")
    subprocess.run(["tar", "-xzf", "hyp-017-validator-results.tar.gz"],
                   cwd=LOCAL_RESULTS, check=True)
    for p in sorted(LOCAL_RESULTS.glob("*.json")):
        print(f"  {p.name}")

    print("\n=== Stopping pod ===")
    code, body = stop_pod()
    print(f"  HTTP {code}: {body[:300]}")

    print("\n=== Verdict summary ===")
    for json_path in sorted(LOCAL_RESULTS.glob("*.json")):
        try:
            d = json.loads(json_path.read_text())
            alpha = d.get("alpha_fit", {}).get("alpha")
            forces = d.get("forces", {})
            verdict = d.get("verdict", "n/a")
            wall = d.get("wall_time_s", "?")
            print(f"\n{json_path.name}:")
            print(f"  verdict: {verdict}")
            print(f"  alpha:   {alpha}")
            print(f"  forces:  {forces}")
            print(f"  wall_s:  {wall}")
        except Exception as e:
            print(f"  {json_path.name}: parse failed -- {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
