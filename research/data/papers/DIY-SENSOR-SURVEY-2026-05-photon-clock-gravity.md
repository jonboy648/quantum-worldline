# DIY Sensor Survey 2026-05 — Photon / Clock / Gravity / Squeezed Light
Status: in progress
Started: 2026-05-01

## Candidates

| Project | Family | Source | Paper | BOM $ | Sensitivity | Difficulty | Notes |
|---|---|---|---|---|---|---|---|
| OpenSPAD (GaudiLabs) | single-photon | gaudi.ch/GaudiLabs | (no paper) | ~$300-500 | single-photon | advanced | open hardware drive/timing/cooling for SPAD |
| Mark Beck Reed College Bell test | single-photon/Bell | diyphysics.com (Beck) | "Quantum Mechanics: Theory and Experiment" textbook | ~$5k STRETCH | CHSH violation | advanced | undergrad standard, Perkin-Elmer C30902S-DTC SPCM |
| Undergraduate Bell + state tomography | single-photon/Bell | arXiv:2407.11570 | arXiv:2407.11570 | ~$3-5k STRETCH | CHSH | intermediate-adv | recent published setup with parts list |
| Type-I BBO entangled photon source (diyphysics.com) | entangled | diyphysics.com | (Kwiat-style design) | ~$1.5k STRETCH | entanglement vis | advanced | 405nm Blu-Ray diode pump, 2x BBO crystals |
| Thorlabs EDU-QOPA1/M | quantum-optics | thorlabs.com | educational kit | ~$10k REJECT | basic | beginner | commercial kit not DIY |
| FE-5680A Rb frequency standard | clock | ko4bb.com/doku2015 + ka7oei.com | (datasheets, FAQ) | ~$50-200 | 1e-11 | beginner | eBay surplus, ham community |
| Spooky-Manufacturing QRNG | QRNG | github.com/Spooky-Manufacturing/QRNG | (no paper) | ~$100-200 | true random | intermediate | polarizing beam splitter, real DIY |
| KevinFasusi qrng | QRNG | github.com/KevinFasusi/qrng | (no paper) | ~$100 | true random | intermediate | full firmware + hardware repo |
| openqbit-diy MiniQRNG | QRNG | github.com/openqbit-diy/MiniQRNG | (handbook) | ~$50-100 | true random | beginner | smartphone-targeted, includes circuit diagrams |
