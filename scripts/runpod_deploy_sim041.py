"""
One-shot RunPod deploy for SIM-2026-041 (scale-invariant MERA spectrum).

RunPod migrated to the REST API at rest.runpod.io/v1 (the old GraphQL spin script 403s). This:
  spin   -> POST /v1/pods : high-RAM CPU pod (cpu5m), PyTorch image, start cmd installs quimb+autograd,
            decodes the embedded sim041 from base64, runs it, writes results to /workspace.
  status -> GET /v1/pods/{id}
  fetch  -> (manual: read /workspace via the pod's outputs; or re-run with a results-print tail)
  kill   -> DELETE /v1/pods/{id}

Usage:
  python runpod_deploy_sim041.py spin     # provision + auto-run sim041
  python runpod_deploy_sim041.py status <podId>
  python runpod_deploy_sim041.py kill <podId>

Requires RUNPOD_API_KEY in env (verified valid 2026-06-18: rpa_EQKL..., rotated from the old key).
Standing RunPod authorization is end-to-end (spin/run/monitor/fetch/kill without per-step asks).
COST: cpu5m is ~$0.10-0.40/hr; a sub-1hr run is a few cents to ~$0.40.
"""
import base64
import json
import os
import sys
import urllib.request

API = "https://rest.runpod.io/v1"
KEY = os.environ.get("RUNPOD_API_KEY")
if not KEY:
    sys.exit("RUNPOD_API_KEY not set")
SIM041 = "D:/quantum-worldline/research/data/simulations/sim041_scaleinv_mera_spectrum.py"


def req(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(f"{API}{path}", data=data, method=method,
                               headers={"Authorization": f"Bearer {KEY}",
                                        "Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(r, timeout=60).read())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()[:500]}")
        raise


def spin():
    with open(SIM041, "rb") as f:
        script_b64 = base64.b64encode(f.read()).decode()
    # start command: install deps, decode sim041, run it, keep results on /workspace
    start = (
        "bash -lc '"
        "set -e; cd /workspace; "
        "pip install -q quimb autograd scipy numpy >/workspace/pip.log 2>&1; "
        f"echo {script_b64} | base64 -d > sim041.py; "
        "echo RUNNING >/workspace/STATUS; "
        "python -u sim041.py >/workspace/run.log 2>&1; "
        "echo DONE >/workspace/STATUS; "
        "sleep infinity'"   # keep pod alive so results can be fetched before teardown
    )
    body = {
        "name": "qw-sim041-scaleinv-mera",
        "imageName": "runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04",
        "cloudType": "SECURE",
        "cpuFlavorIds": ["cpu5m"],
        "vcpuCount": 8,                # cpu5m ~8GB/vCPU -> ~64GB RAM, ample for the contraction
        "containerDiskInGb": 30,
        "volumeInGb": 10,
        "volumeMountPath": "/workspace",
        "ports": ["22/tcp"],
        "dockerStartCmd": ["bash", "-lc", start.split("bash -lc '", 1)[1].rstrip("'")],
        "env": {},
    }
    print("Provisioning pod...")
    r = req("POST", "/pods", body)
    pid = r.get("id") or r.get("podId")
    print(json.dumps(r, indent=2)[:800])
    print(f"\nPOD ID: {pid}")
    print(f"Monitor: python {sys.argv[0]} status {pid}")
    return pid


def status(pid):
    r = req("GET", f"/pods/{pid}")
    print(json.dumps(r, indent=2)[:1500])


def kill(pid):
    req("DELETE", f"/pods/{pid}")
    print(f"deleted pod {pid}")


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
