# QUANTUM-VILLAGE-2026-001: Quantum Village GitHub & Community Recon

**Date:** 2026-04-26  
**Investigator:** qv-investigator (literature-lead team)  
**Sources:** github.com/QuantumVillage, quantumvillage.org, arxiv:2509.18329, Hackaday, Quantum Zeitgeist

---

## Section 1: Org Footprint

| Field | Detail |
|---|---|
| GitHub URL | https://github.com/QuantumVillage |
| Website | https://www.quantumvillage.org |
| arXiv preprint | https://arxiv.org/abs/2509.18329 |
| Org type | Not-for-profit, incorporated as Quantum Village Inc. |
| Co-founders | Mark Carney (CTO, pure mathematician, quantum cybersecurity), Victoria Kumaran (Exec Director, art/design background) |
| DEF CON track | Annual village since ~DC28; DC33 (Aug 2025) theme: "Sense and Security" |
| Public repos | 10 in GitHub org; 20+ in Carney's personal account (QCmonk) |
| Primary languages | C, Python, Jupyter Notebook, VHDL, Prolog (metadata artifacts), JavaScript |
| License model | AGPL-3.0 for hardware; MIT for educational; MPL-2.0 for QRNG; commercial license available for UncutGem |

---

## Section 2: Repo-by-Repo Summary

| Repo | Purpose | Language | Last Updated | Stars | Topic Alignment |
|---|---|---|---|---|---|
| **UncutGem** | Full-stack open-source NV center diamond magnetometer (V2 at DC33) | C / Arduino | Jan 2026 | 170 | **DIRECT** — NV magnetometry |
| **EntropyLoop** | Phase-diffusion QRNG using fiber optics + Raspberry Pi Pico, ~$35 | C / MicroPython | Apr 2026 | 33 | Adjacent — quantum hardware |
| **qicks** | Fork of QICK (Xilinx RFSoC control kit) with security extensions; targets ZCU111/ZCU216/RFSoC4x2; QICK-DAWG extension covers NV control | Jupyter/VHDL/Python | May 2024 | 1 (136 forks) | **DIRECT** — NV/qubit control firmware |
| **quantum-music** | Quantum-inspired music generation tools | C | Jun 2025 | 13 | None |
| **awesome-quantum-security** | Curated reading list: PQC, quantum network hacking, QKD vulnerabilities | — | Apr 2025 | 7 | Indirect — security posture |
| **QVxC3S-Resources** | Slides/resources from C3S 2025 presentation | JavaScript | Apr 2025 | 6 | None |
| **oscrypto** | Cryptographic discovery queries for osquery | — | Sep 2025 | 2 | None |
| **DEFCON31-MediaDump** | Slides, files, code from DC31 talks | — | Aug 2023 | 7 | Archive value |
| **HackGPT** | "Bot-in-the-middle" LLM attack PoC (Le Hack 2023) | Python | Oct 2023 | 15 | None |
| **micro-quantum** | Embedded quantum circuit simulator (browser toy, Quirk-based) | C | Jul 2023 | 21 | Educational |

**Mark Carney personal (QCmonk):**

| Repo | Purpose | Language |
|---|---|---|
| **qChain** | Simulation of quantum magnetometer sensor for sparse magnetic field signals | Python |
| **qfunk** | General quantum information methods library | Python |
| (+18 others not fully enumerated due to profile load limit) | | |

---

## Section 3: Topical Alignment with User's Interests

### NV Magnetometry — HIGH ALIGNMENT
UncutGem is a direct hit. It is a complete, buildable NV center magnetometer at ~£115/$100 using:
- ADF4351 microwave generator (35 MHz–4.4 GHz sweep)
- 532nm green LED excitation (replacing costly lasers)
- ESP32 + Arduino firmware
- BPW34 photodiode + opamp chain
- Custom PCB with full schematics in `/hardware/PCB`

Paper (arXiv:2509.18329) describes: 2.87 GHz zero-field splitting, 2.614–3.126 GHz sweep range, sensitivity ~0.005–0.01 T for benchtop bar magnets. Not yet at neuroscience OPM-MEG sensitivity (fT range), but the architecture is correct and the team explicitly lists magnetocardiography and PNT as target applications.

### OPM-MEG — INDIRECT
UncutGem V2 architecture (LED not laser, epoxy diamond encapsulation) reduces cost but also reduces sensitivity vs. SERF/OPM-MEG. No vapor-cell OPM work found anywhere in their repo or talks. Gap confirmed.

### Rydberg Electrometry — NOT PRESENT
No Rydberg atom or vapor cell work in any QV repo or talk listing found. The DEF CON 33 "Sense and Security" theme covered NV sensing; Rydberg was not in evidence.

### MagNav — MENTIONED AS APPLICATION
The UncutGem paper explicitly names "Position, Navigation, and Timing (PNT)" and "space-ready CubeSat configurations" as target applications — these directly point toward MagNav use cases. No standalone MagNav repo exists, but UncutGem is the foundational hardware.

### BCI / Neural Sensing — NOT PRESENT
No BCI-specific work found. The gap between UncutGem's ~10 mT sensitivity floor and the fT sensitivity needed for MEG-based BCI is large; QV does not appear to be pursuing this direction.

### Quantum Control Hardware (QICK/QICKS) — RELEVANT
The qicks repo is a security-extended fork of Sandia's QICK platform. QICK-DAWG (external, sandialabs/qick-dawg) explicitly extends QICK for NV center control. If the user wants to drive NV centers with arbitrary microwave pulse sequences, QICK + QICK-DAWG is the serious hardware path (Xilinx RFSoC). QV's qicks fork adds security analysis angles.

---

## Section 4: Repos Worth Cloning

1. **github.com/QuantumVillage/UncutGem** — Clone immediately. Full hardware build: schematics, BOM, firmware. V2 is the current version (released DC33 Aug 2025). AGPL-3.0 means derivatives must open-source. Commercial license available from QV Inc. if needed.

2. **github.com/QuantumVillage/qicks** — Clone if pursuing FPGA-based microwave control for NV or superconducting qubits. The fork is lightly starred (1 star) but has 136 forks suggesting quiet adoption. The upstream QICK project (Yale + Fermilab) is more active.

3. **github.com/QCmonk/qChain** — Carney's personal magnetometer simulation. Python. Useful as a reference for signal modeling.

4. **github.com/QuantumVillage/EntropyLoop** — Clone if building anything that needs hardware entropy (key generation, randomness testing). $35 build. MicroPython path is beginner-friendly.

---

## Section 5: People Worth Following

| Person | GitHub | Role | Relevant Work |
|---|---|---|---|
| Mark Carney | github.com/QCmonk | Co-founder/CTO QV | UncutGem architect, qChain magnetometer sim, qfunk QI library, Univ. Vienna affiliation |
| Victoria Kumaran | (not found on GitHub) | Exec Director | Community/comms lead; no code repos identified |

**Adjacent organizations to watch:**
- **sandialabs/qick-dawg** — Sandia National Labs NV control extension for QICK. Direct hardware complement to UncutGem's sensing layer.
- **QCmonk/qfunk** — General QI methods; watch for sensing additions.

---

## Section 6: Honest Gaps

**What QV does NOT publish that the user might have hoped for:**

- **OPM / SERF magnetometer**: No vapor-cell work at all. UncutGem is NV-only. OPM-MEG requires alkali vapor cells (Rb/Cs) in a SERF regime — a completely different technology stack that QV has not touched.

- **Rydberg electrometry**: Nothing. No vapor cell, no atom trap, no RF sensing via Rydberg levels. This is a distinct research community (NIST, Raithel group, etc.) that has no intersection with QV's current portfolio.

- **BCI / neural MEG**: Not on their radar. Their stated medical application is magnetocardiography (easier: heart signal is ~100 pT vs. brain ~100 fT). The gap to MEG-grade BCI sensing is 6 orders of magnitude in sensitivity.

- **MagNav software stack**: They name PNT as an application but publish no map-matching, trajectory estimation, or anomaly navigation code. The hardware sensor exists; the nav algorithm layer does not.

- **Government / DARPA / NIST partnerships**: No visible funding trail. No SBIR, no NIST STTR, no DARPA collaboration mentioned on quantumvillage.org or in any repo. QV appears self-funded / community-funded. IBM Q sponsorship is plausible given their quantum computing education angle but not confirmed in any source found.

- **Post-quantum crypto CTF content**: The Quantum-CTF competition is referenced but no standalone repo with CTF challenge code was found. The awesome-quantum-security list is a reading list, not challenge code.

**Sensitivity reality check for UncutGem:**  
Current V2 sensitivity (~mT range for bar magnets) is educational/demonstration grade. Reaching pT-range (magnetocardiography) or fT-range (MEG) would require lock-in amplification, magnetic shielding, spin-bath optimization, and ensemble NV geometries not present in the current design. The paper is honest about this; the platform is explicitly framed as a learning tool and democratization effort, not a research-grade magnetometer.

---

## Summary Assessment

Quantum Village's GitHub is primarily an **NV-center magnetometry + quantum education** org. UncutGem is genuinely interesting open hardware — the first fully open-source NV diamond magnetometer with a complete build path under $100. The QICKS fork and Carney's personal repos extend the utility toward microwave pulse control. The org does not publish work on OPM, Rydberg, BCI, or MagNav algorithms. Post-quantum crypto appears in their curation list but not as active engineering output. For the user's interests, UncutGem + qicks + qChain are worth deep-reading; everything else is background noise.
