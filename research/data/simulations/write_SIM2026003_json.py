"""Write the final SIM-2026-003.json with complete honest results."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
import numpy as np

L_ADS = 1.0 / np.log(2)

# v2 VQE results (from logs + recovery run)
E_OPT = -24.666990
E0    = -25.107797
PCT_ERR = abs(E_OPT - E0) / abs(E0) * 100

# Force profile (from recovery run with v2 theta)
seps_fp = list(range(1, 9))
Vs_fp   = [-0.004705, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
Cvac_fp = [0.00772, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
Ctwo_fp = [0.00301, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
magz_avg = -0.7863
V_anal = [float(0.08 - 13.6 * np.exp(-dr / L_ADS)) for dr in seps_fp]

# Circuit
cx_count = 38; depth = 36; NP = 190; N = 20; N_LAYERS = 5
error_h2 = 1.0 - (0.998**cx_count)
error_h3 = 1.0 - (0.995**cx_count)

structured = {
    "id": "SIM-2026-003",
    "description": (
        "VQE optimization of 20-qubit binary MERA (5 layers, 190 params, H-gate init) "
        "to critical Ising GS (J=h=1, OBC N=20). "
        "v2: H-gate initialization, 10-seed COBYLA + 2-phase polish. "
        "AerEstimator(approx=True). Step 3 of HYP-2026-002. "
        "Key finding: MERA converges to ferromagnetic product state; "
        "ZZ connected correlators near-zero at r>=2. Architecture revision required."
    ),
    "type": "vqe_optimization",
    "date": "2026-03-10",
    "hypothesis_id": "HYP-2026-002",
    "paper_ref": "PAPER-2026-003",
    "step": 3,
    "version": "v2_hgate_init",
    "backend": "qiskit_aer_estimator_approximation_true",
    "circuit": {
        "qubits": int(N),
        "layers": int(N_LAYERS),
        "n_params": int(NP),
        "cx_count": int(cx_count),
        "depth": int(depth),
        "architecture": "Hgate_init_binary_MERA_5layer_OBC",
        "hologron_gate": "Ry",
        "hologron_angle_rad": float(np.pi / 3),
        "anchor_site": int(N // 4),
        "causal_cone": "5 layers covers dr=1..32 (full range for N=20)",
        "init_note": "H gates before MERA: |+>^N start, target <Z>=0",
    },
    "vqe": {
        "optimizer": "COBYLA_10seed_multistart_then_2phase_polish",
        "seeds": [0, 1, 2, 3, 42, 7, 13, 99, 5, 17],
        "n_total_evals": 55000,
        "t_per_eval_s": 0.058,
        "E_optimized": float(E_OPT),
        "E0_exact": float(E0),
        "pct_error": float(round(PCT_ERR, 4)),
        "converged_1pct": bool(PCT_ERR < 1.0),
        "converged_2pct": bool(PCT_ERR < 2.0),
        "elapsed_seconds": 7200.0,
        "v2_seed_bests": {
            "seed_0": -24.607, "seed_1": -24.660, "seed_2": -24.632,
            "seed_3": -24.624, "seed_42": -24.646, "seed_7": -23.450,
            "seed_13": -24.648, "seed_99": -24.632, "seed_5": -24.644,
            "seed_17": -24.648,
        },
        "polish_medium": -24.665,
        "polish_fine": float(E_OPT),
        "state_analysis": {
            "magz_avg": float(magz_avg),
            "magz_range": [-0.843, -0.471],
            "magx_avg": 0.529,
            "state_type": "ferromagnetic_product_like",
            "C_connected_r1": 0.00772,
            "C_connected_r2plus": 0.0,
            "diagnosis": (
                "MERA converges to ferromagnetic product state despite H-gate init. "
                "Real-valued MERA ansatz lacks Z2 symmetry protection. "
                "C_connected(r>=2)=0 means no multi-site entanglement captured. "
                "Requires symmetry-enforced or ZX-calculus MERA."
            ),
        },
    },
    "force_profile": {
        "delta_rho": [int(x) for x in seps_fp],
        "V_quantum": [float(x) for x in Vs_fp],
        "V_analytical": V_anal,
        "C_vac": [float(x) for x in Cvac_fp],
        "C_two": [float(x) for x in Ctwo_fp],
        "anchor_site": int(N // 4),
        "magz_avg": float(magz_avg),
        "note": "V~0 because MERA in ferromagnetic product state, not critical GS",
    },
    "fit": {
        "success": False,
        "error": "V(dr) signals ~0: MERA state not converged to critical GS",
        "xi_3layer": 1.233,
        "xi_theory": float(L_ADS),
        "diagnosis": (
            "Holographic fit requires V(dr) ~ C1 - C2*exp(-dr/xi). "
            "Current V~0 everywhere. Classical V(dr=1)=-0.345 is the target scale."
        ),
    },
    "comparison": {
        "paper_C1": 0.080,
        "paper_C2": 13.6,
        "paper_l_AdS": float(L_ADS),
        "xi_3layer_16q": 1.233,
        "xi_5layer_20q": None,
        "xi_theory": float(L_ADS),
        "E_3layer_16q": -19.642,
        "E0_3layer": -20.016,
        "pct_err_3layer": 1.87,
        "E_5layer_20q": float(E_OPT),
        "E0_5layer": float(E0),
        "pct_err_5layer": float(round(PCT_ERR, 4)),
        "expressibility_note": (
            "5-layer 20q ceiling ~1.76% vs 3-layer 16q ~1.87%. Slight improvement. "
            "Both circuits fail to produce critical correlations: C_connected(r>=2)~0. "
            "Root cause: real-valued binary MERA lacks Z2 symmetry protection for TFIM."
        ),
        "classical_comparison": {
            "V_classical_dr1_OBC": -0.344830,
            "V_classical_dr1_PBC": -0.375586,
            "V_quantum_dr1": -0.004705,
            "ratio": round(-0.004705 / -0.344830, 4),
            "interpretation": "1.4% of classical signal captured at dr=1; 0% at dr>=2",
        },
        "normalization_note": (
            "Paper C1=0.08, C2=13.6 uses different normalization than C_two - C_vac. "
            "Classical V(dr=1)=-0.345 vs AdS prediction V(dr=1)=-6.72. "
            "Direct comparison requires matching normalization conventions."
        ),
        "causal_cone_note": "5-layer covers dr=1..32; 3-layer covered only dr=1..8",
    },
    "feasibility": {
        "cx_count": int(cx_count),
        "depth": int(depth),
        "n_params": int(NP),
        "h2_error_pct": float(round(error_h2 * 100, 2)),
        "heron_r3_error_pct": float(round(error_h3 * 100, 2)),
        "h2_feasible_poc": bool(error_h2 < 0.10),
        "hardware_target": "simulator_qiskit_aer",
        "recommendation": (
            "H2 at 7.33% error budget (CX=38) within 10% PoC threshold. "
            "But architecture revision needed before hardware run is meaningful. "
            "Symmetry-enforced MERA would likely use similar CX count."
        ),
    },
    "next_steps": {
        "priority_1": (
            "Symmetry-enforced MERA: enforce Z2 symmetry in circuit ansatz "
            "to prevent ferromagnetic local minimum collapse"
        ),
        "priority_2": (
            "Measure XX correlators with Rz hologrons: current state has <X>=0.53 "
            "(Rz rotates in ZY plane, modifies X-basis correlations)"
        ),
        "priority_3": (
            "7+ layer MERA on 32 qubits: deeper architecture with full causal cone "
            "at N=32 for proper holographic limit"
        ),
        "priority_4": (
            "Match paper normalization: resolve C1/C2 convention difference "
            "before comparing to C1=0.08, C2=13.6, l_AdS=1.443"
        ),
    },
    "hardware_target": "simulator_qiskit_aer",
    "total_elapsed_seconds": 7200.0,
    "theta_opt_path": "D:/quantum-worldline/research/data/simulations/theta_opt_SIM2026003.npy",
}

OUT_JSON = "D:/quantum-worldline/research/data/simulations/SIM-2026-003.json"
with open(OUT_JSON, 'w') as f:
    json.dump(structured, f, indent=2)

print(f"Saved: {OUT_JSON}")
print(f"E_opt={E_OPT:.6f}  E0={E0:.6f}  pct_err={PCT_ERR:.4f}%")
print(f"circuit: {N}q/{N_LAYERS}L/{NP}p/{cx_count}CX/depth={depth}")
print(f"H2 error: {error_h2*100:.2f}%  h2_feasible: {error_h2 < 0.10}")
print(f"V_quantum dr=1..8: {Vs_fp}")
