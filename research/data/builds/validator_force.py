"""
Validator force estimator — bitstring to energy proxy + Renyi-2 entropy for 8-boundary AHS validator.
TFIM-Rydberg mapping: <Z_i> ~ 1 - 2 * density_i, E_proxy = -sum<Z_i Z_{i+1}> - sum(2*sqrt(p(1-p)))
"""
import numpy as np

N_BOUNDARY = 8


def bitstrings_to_density(result):
    measurements = result.measurements
    if not measurements:
        return np.zeros(15), 0
    n_atoms = len(measurements[0].pre_sequence)
    density = np.zeros(n_atoms)
    valid = 0
    for shot in measurements:
        if shot.status.name == "SUCCESS":
            density += np.array(shot.post_sequence, dtype=float)
            valid += 1
    if valid > 0:
        density /= valid
    return density, valid


def density_to_energy_proxy(density, n_boundary=N_BOUNDARY):
    zi = 1.0 - 2.0 * density[:n_boundary]
    zz = float(np.sum(zi[:-1] * zi[1:]))
    p = density[:n_boundary]
    xi = 2.0 * np.sqrt(np.maximum(p * (1.0 - p), 1e-10))
    return float(-zz - np.sum(xi))


def force_dr(E_dual, E0, E_single_j, E_single_k):
    """F(dr) = E_dual - E0 - (E_single_j - E0) - (E_single_k - E0)"""
    return float(E_dual - E0 - (E_single_j - E0) - (E_single_k - E0))


def renyi2_collision(measurements, sites):
    """Renyi-2 entropy on subsystem `sites` from bitstrings via collision probability."""
    valid = []
    for shot in measurements:
        if shot.status.name == "SUCCESS":
            bits = np.array(shot.post_sequence, dtype=int)
            valid.append(bits[sites])
    if len(valid) < 4:
        return float("nan")
    arr = np.array(valid)
    n_shots = len(arr)
    purity_sum = 0.0
    n_pairs = 0
    for i in range(n_shots):
        for j in range(i + 1, n_shots):
            h = int(np.sum(arr[i] != arr[j]))
            purity_sum += (-0.5) ** h
            n_pairs += 1
    if n_pairs == 0:
        return float("nan")
    purity = max(purity_sum / n_pairs, 1e-10)
    return float(-np.log2(purity) * np.log(2))  # nats


if __name__ == "__main__":
    # Synthetic test: bitstring "00000000" 50 times -> all-zero density
    fake_density = np.zeros(15)
    e0 = density_to_energy_proxy(fake_density)
    print(f"validator_force: E0(all-zero) = {e0:.4f}")
    fake_density[:8] = 0.5
    e_mid = density_to_energy_proxy(fake_density)
    print(f"validator_force: E(half-density) = {e_mid:.4f}")
