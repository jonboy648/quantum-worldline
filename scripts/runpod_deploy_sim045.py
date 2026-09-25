"""
RunPod deploy for SIM-2026-045 (STABLE scale-invariant MERA, EV ScInv1/ScInv2) at chi=6.

ONLY run after the chi=4 Ising control PASSES the gate locally (c=0.5, sigma=0.125, eps=1.0, T=2.0
in one converged state). chi=6 operator space = 6^6 = 46656; the spectrum eigensolve is matrix-free
(LinearOperator) so RAM is modest, but the per-round rho eigensolve + h_bar + spectrum is heavy ->
RunPod CPU box. The script embeds sim045 (base64), overrides CHI=6 via a sed, runs, keeps results.

REST API at rest.runpod.io/v1 (GraphQL 403s). Standing RunPod authorization is end-to-end
(spin/run/monitor/fetch/kill, no per-step asks). Key in env RUNPOD_API_KEY (rpa_EQKL..., rotated valid).
COST: cpu5m ~$0.10-0.40/hr; expect a sub-1hr run -> a few cents to ~$0.40.

Usage:
  python runpod_deploy_sim045.py spin            # provision + auto-run sim045 at chi=6
  python runpod_deploy_sim045.py status <podId>
  python runpod_deploy_sim045.py log <podId>     # cat /workspace/run.log via a fresh exec (ssh)
  python runpod_deploy_sim045.py kill <podId>
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://rest.runpod.io/v1"
KEY = os.environ.get("RUNPOD_API_KEY")
if not KEY:
    sys.exit("RUNPOD_API_KEY not set (export the rotated rpa_EQKL... key)")
SIM045 = "D:/quantum-worldline/research/data/simulations/sim045_scaleinv_stable.py"
CHI = int(os.environ.get("QW_CHI", "6"))


def req(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(f"{API}{path}", data=data, method=method,
                               headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(r, timeout=60).read())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()[:500]}"); raise


def spin():
    with open(SIM045, "rb") as f:
        script_b64 = base64.b64encode(f.read()).decode()
    seed_path = os.environ.get("QW_SEED_FILE")   # local padded seed npz to upload (chi-ramp warm start)
    seed_cmds = ""
    seed_env = ""
    if seed_path and os.path.exists(seed_path):
        with open(seed_path, "rb") as f:
            seed_b64 = base64.b64encode(f.read()).decode()
        seed_cmds = f"echo {seed_b64} | base64 -d > seed.npz; "
        seed_env = "export QW_SEED=/workspace/seed.npz; "
        print(f"embedding seed {seed_path} ({len(seed_b64)} b64 chars)")
    inner = (
        "set -e; cd /workspace; "
        "pip install -q torch scipy numpy >/workspace/pip.log 2>&1; "
        f"echo {script_b64} | base64 -d > sim045.py; "
        f"{seed_cmds}"
        f"sed -i 's/^CHI = .*/CHI = {CHI}/' sim045.py; "
        "echo RUNNING >/workspace/STATUS; "
        f"{seed_env}"
        "python -u sim045.py >/workspace/run.log 2>&1; "
        "echo DONE >/workspace/STATUS; "
        "sleep infinity"
    )
    body = {
        "name": f"qw-sim045-stable-chi{CHI}",
        "imageName": "runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04",
        "cloudType": "SECURE",
        "cpuFlavorIds": ["cpu5m"],
        "vcpuCount": 16,                 # more vCPUs help the per-round eigensolves + autograd
        "containerDiskInGb": 30,
        "volumeInGb": 10,
        "volumeMountPath": "/workspace",
        "ports": ["22/tcp"],
        "dockerStartCmd": ["bash", "-lc", inner],
        "env": {},
    }
    print(f"Provisioning pod for sim045 chi={CHI}...")
    r = req("POST", "/pods", body)
    pid = r.get("id") or r.get("podId")
    print(json.dumps(r, indent=2)[:800])
    print(f"\nPOD ID: {pid}\nMonitor: python {sys.argv[0]} status {pid}")
    return pid


def status(pid):
    print(json.dumps(req("GET", f"/pods/{pid}"), indent=2)[:1500])


def kill(pid):
    req("DELETE", f"/pods/{pid}"); print(f"deleted pod {pid}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "spin"
    if cmd == "spin":
        spin()
    elif cmd == "status":
        status(sys.argv[2])
    elif cmd == "kill":
        kill(sys.argv[2])
    else:
        print(__doc__)
