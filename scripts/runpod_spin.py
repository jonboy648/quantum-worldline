"""Spin a CPU pod on RunPod for HYP-2026-017 validator diagnostics."""
import json
import os
import sys
import urllib.request

API_KEY = os.environ.get("RUNPOD_API_KEY")
if not API_KEY:
    sys.exit("RUNPOD_API_KEY not set. Export it before running: "
             "export RUNPOD_API_KEY=rpa_... (PowerShell: $env:RUNPOD_API_KEY='rpa_...')")
URL = "https://api.runpod.io/graphql"


def graphql(query, variables=None):
    payload = {"query": query}
    if variables is not None:
        payload["variables"] = variables
    req = urllib.request.Request(
        URL,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        method="POST",
    )
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())


def main():
    # 1) discover available CPU pod templates / images
    q = """
    query CpuTypes {
      cpuTypes {
        id
        displayName
        cores
        threadsPerCore
        groupId
      }
    }
    """
    print("Querying CPU types...")
    r = graphql(q)
    print(json.dumps(r, indent=2)[:2000])


if __name__ == "__main__":
    sys.exit(main())
