# DIY Quantum Sensor Survey — UncutGem-Style Sister Projects

**Date:** 2026-05-01
**Team:** diy-quantum-sensor-survey (3 sweeps + synthesis)
**Source files:**
- `research/data/papers/DIY-SENSOR-SURVEY-2026-05-NV-vapor.md` (10 candidates)
- `research/data/papers/DIY-SENSOR-SURVEY-2026-05-photon-clock-gravity.md` (9 candidates)
- `research/data/papers/DIY-SENSOR-SURVEY-2026-05-coldatom-misc.md` (7 candidates + 8 Quantum Village repos)

**Raw count:** 26 entries before dedup. After dedup (pyppm + RowleyLab EF-NMR appear in both Sweep 1 and Sweep 3): **24 unique candidates.**

---

## TL;DR

UncutGem is not alone. There are at least **8 sub-$1000 candidates** that meet your bar (open hardware + paper or technical report + working physical demonstration), plus **5 STRETCH** candidates in the $1k–$5k range, and **a clear set of REJECTs** that mostly require lab facilities you don't have.

The strongest second sensor after UncutGem is **arXiv:2512.03106** — a portable LED-based diamond magnetometer with full PCB design files and a published parts list, explicitly built for outreach and teaching. It is the closest published peer to UncutGem and the most direct upgrade path: same physics, similar cost, more documentation.

The unexpected finding is that **DIY QRNGs are a real category** — three independent open-hardware repos (Spooky-Manufacturing, KevinFasusi, openqbit-diy) all sub-$200, all using a beam splitter on a laser to generate quantum-random bits. None of these connect to your holography research, but each is publishable as "open hardware QRNG with NIST SP 800-22 validation," which is a much shorter path to a paper than UncutGem itself.
