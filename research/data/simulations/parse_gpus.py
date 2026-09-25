import json
with open("D:/quantum-worldline/research/data/simulations/runpod_gpus.json") as f:
    data = json.load(f)
for gpu in data['data']['gpuTypes']:
    name = gpu['displayName']
    if any(x in name for x in ['A6000', 'A5000', '4090', 'A100']):
        mem = gpu['memoryInGb']
        sp = gpu.get('securePrice') or 'N/A'
        cp_ = gpu.get('communityPrice') or 'N/A'
        print(f"{gpu['id']:30s} {name:25s} {mem:3d}GB  ${sp}/hr  community: ${cp_}/hr")
