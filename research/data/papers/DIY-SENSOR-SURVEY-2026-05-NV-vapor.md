# DIY Sensor Survey 2026-05 — NV / Vapor Cell

Status: complete
Date: 2026-05-01
Owner: scanner-nv-vapor-v2 (completed by main session after teammate stall)

## Candidates

| Project | Family | Source | Paper | BOM $ | Sensitivity | Difficulty | Notes |
|---|---|---|---|---|---|---|---|
| UncutGem v2 | NV | github.com/QuantumVillage/UncutGem | arXiv:2509.18329 | ~$100 | not stated | beginner | DEF CON 33 release, LED-pumped |
| Portable LED-NV magnetometer | NV | arXiv:2512.03106 | arXiv:2512.03106 | ~$200 | nT-scale | beginner | full PCB + parts list, outreach build |
| CW-ODMR NV magnetometer | NV | mdpi.com/2673-8724/5/3/18 | MDPI Magnetism 5(3)18 | <$1000 | µT range | intermediate | inexpensive components paper |
| pi3diamond | NV | github.com/HelmutFedder/pi3diamond | (software only) | requires hardware | research-grade | advanced | Python control software, not BOM |
| pyppm | vapor/EFNMR | github.com/geekysuavo/pyppm | (no paper) | ~$200-500 | mT range | intermediate | Earth's-field NMR DIY |
| RowleyLab EF-NMR | vapor/EFNMR | github.com/RowleyLab/EF-NMR | (no paper) | ~$300-500 | mT range | intermediate | hardware + software |
| OPMLab (NIH) | OPM | github.com/nih-megcore/OPMLab | (software only) | requires QuSpin sensors | sub-pT | advanced | software-only |
| Modular OPM system | OPM | arXiv:2106.05877 | arXiv:2106.05877 | $5k+ STRETCH | sub-pT | advanced | reconfigurable academic build |
| TeachSpin Diode Laser Spectroscopy | vapor | teachspin.com/diode-laser-spectroscopy | (commercial doc) | ~$15k REJECT | hyperfine | intermediate | commercial Rb SAS, not DIY |
| Thorlabs SKSAS | vapor | thorlabs.com SKSAS | (commercial) | ~$3k STRETCH | hyperfine | intermediate | commercial SAS kit |

Total: 10 candidates. Top 3 for the user: UncutGem v2, arXiv:2512.03106 portable LED-NV, MDPI CW-ODMR.
