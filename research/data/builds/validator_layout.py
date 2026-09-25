"""
Validator atom layout — 15-atom reduced version of HYP-2026-017 production layout.
Used for local braket_ahs emulator smoke test (full 30-atom layout = 54GB RAM blowup).

Geometry:
  Layer 3 (UV, y=0):    8 boundary atoms, 5 um spacing
  Layer 2 (mid, y=10):  4 bond atoms,    10 um spacing
  Layer 1 (IR, y=20):   2 coarse atoms,  20 um spacing
  Layer 0 (bulk, y=30): 1 bulk atom

  Total: 15 atoms. State vector 2^15 = 32768 (fits in <1 MB).

Coordinates in METERS (Braket convention).
"""
from braket.ahs import AtomArrangement

BOUNDARY_SPACING_UM = 5.0
LAYER_OFFSET_Y_UM = 10.0
N_BOUNDARY = 8
N_TOTAL = 15

def build_validator_layout():
    register = AtomArrangement()
    # Layer 3: 8 boundary atoms
    for i in range(8):
        x = i * BOUNDARY_SPACING_UM
        register.add([x * 1e-6, 0.0])
    # Layer 2: 4 bond atoms
    for i in range(4):
        x = (2 * i + 0.5) * BOUNDARY_SPACING_UM
        register.add([x * 1e-6, LAYER_OFFSET_Y_UM * 1e-6])
    # Layer 1: 2 coarse atoms
    for i in range(2):
        x = (4 * i + 1.5) * BOUNDARY_SPACING_UM
        register.add([x * 1e-6, 2 * LAYER_OFFSET_Y_UM * 1e-6])
    # Layer 0: 1 bulk atom
    register.add([3.5 * BOUNDARY_SPACING_UM * 1e-6, 3 * LAYER_OFFSET_Y_UM * 1e-6])
    return register

if __name__ == "__main__":
    reg = build_validator_layout()
    sites = list(reg)
    print(f"validator_layout: {len(sites)} atoms built (expected {N_TOTAL})")
    print(f"  expected boundary: {N_BOUNDARY}, bond: 4, coarse: 2, bulk: 1")
