# Quantinuum Helios Access Research

**Date:** 2026-03-17
**Purpose:** Evaluate all pathways to Helios hardware access for our MERA holographic force experiment
**Status:** RESEARCH ONLY - no applications submitted

---

## 1. Access Channels Overview

There are five distinct pathways to Quantinuum hardware, summarized here from most to least accessible:

| Channel | Cost | Hardware | Best For |
|---|---|---|---|
| Azure Quantum (free credits) | $0 (500 USD credits = 40 HQCs) | H2 emulator + hardware | Initial testing, emulator validation |
| ORNL QCUP | Free (US researchers) | H2-1, H2-2, Helios-1 | Production runs, full experiment |
| Quantinuum Nexus (direct) | Pay-as-you-go (contact sales) | H2, Helios | Direct relationship, custom pricing |
| Q-Net / Startup Partner Program | Varies (partnership) | H2, Helios, Nexus, InQuanto | Startups in quantum ecosystem |
| Azure Quantum Subscription | $125K-$175K/month | H2 (10K-17K HQCs) | Enterprise users only |

---

## 2. Pricing Model — Hardware Quantum Credits (HQCs)

### HQC Formula

```
HQC = 5 + C * (N_1q + 10 * N_2q + 5 * N_m) / 5000
```

Where:
- **C** = number of shots
- **N_1q** = single-qubit gate count (Rxy/phased_x; Rz gates are FREE)
- **N_2q** = native two-qubit gate count (ZZPhase, equivalent to CNOT)
- **N_m** = state preparation + measurement operations (including initial prep, mid-circuit, and final)
- **5** = fixed base cost per job submission

### Our Circuit HQC Estimates

**32q/3-layer MERA force measurement (recommended config):**
- N_1q ~ 350 single-qubit gates (Rz excluded from billing)
- N_2q = 140 CNOTs (native two-qubit gates)
- N_m = 32 (initial state prep) + 32 (final measurement) = 64 SPAM operations
- C = 280,000 shots (vacuum + two-hologron, 140K each)

```
HQC = 5 + 280,000 * (350 + 10*140 + 5*64) / 5000
    = 5 + 280,000 * (350 + 1400 + 320) / 5000
    = 5 + 280,000 * 2070 / 5000
    = 5 + 115,920
    = 115,925 HQCs (for 32q force profile alone)
```

**16q/3-layer baseline validation:**
- N_1q ~ 175, N_2q = 56, N_m = 32
- C = 140,000 shots

```
HQC = 5 + 140,000 * (175 + 560 + 160) / 5000
    = 5 + 140,000 * 895 / 5000
    = 5 + 25,060
    = 25,065 HQCs
```

**Full program (all experiments):**
- 16q force: ~25K HQCs
- 32q force: ~116K HQCs
- Transport (16q, 200K shots): ~40K HQCs
- **Total: ~181K HQCs**

### Dollar Cost Per HQC

Quantinuum does NOT publish a per-HQC dollar price for pay-as-you-go. What we know:

| Source | Rate | Derivation |
|---|---|---|
| Azure free credits | $12.50/HQC | $500 = 40 HQCs |
| Azure Standard subscription | $12.50/HQC | $125,000/month = 10,000 HQCs |
| Azure Premium subscription | $10.29/HQC | $175,000/month = 17,000 HQCs |
| Pay-as-you-go (direct) | Unknown | Must contact Sales@Quantinuum.com |

**IMPORTANT NOTE:** The Azure pricing page was updated 2025-09-17. Earlier sources cited Standard at $135K and Premium at $185K; the current prices are $125K and $175K respectively. The per-HQC rate is consistent at ~$12.50 (Standard) and ~$10.29 (Premium).

### Cost Estimates for Our Experiment

| Experiment | HQCs | Cost @ $12.50/HQC | Cost @ $10.29/HQC |
|---|---|---|---|
| 16q force profile | 25,065 | $313,313 | $257,919 |
| 32q force profile | 115,925 | $1,449,063 | $1,192,868 |
| Transport (16q) | ~40,000 | $500,000 | $411,600 |
| Full program | ~181,000 | $2,262,500 | $1,862,490 |

**These numbers are dramatically higher than our earlier helios-mera-design.md estimates** ($7.4K academic, $15-44K commercial), which were based on assumed per-shot pricing of $0.005-$0.03. The HQC formula penalizes two-qubit gates at 10x the rate of single-qubit gates, and our 140-CNOT circuit drives the cost up enormously.

**CRITICAL REASSESSMENT:** At commercial Azure rates, the full experiment would cost ~$2.3M. This makes commercial access completely infeasible. The only viable paths are:

1. **QCUP (free research allocations)**
2. **Research partnership with Quantinuum (negotiated credits)**
3. **Azure Quantum Credits program (up to ~$10K grants)**
4. **Significant circuit optimization to reduce N_2q**

**Alternative: reduce experiment scope.** A minimal 16q/3L validation run with 10K shots (not 140K) would cost ~1,800 HQCs = ~$22,500 at commercial rates. Still expensive, but approaching feasibility for a grant-funded project.

---

## 3. ORNL QCUP (Quantum Computing User Program)

**This is our best pathway for free access.**

### What It Is
- Oak Ridge National Laboratory runs QCUP to provide US researchers free access to quantum hardware
- Partners: IBM Quantum, IQM, IonQ, **Quantinuum** (H2-1, H2-2, **Helios-1**)
- Access through Quantinuum Nexus platform

### Eligibility
- Must be a US-based researcher (university, national lab, or independent)
- All proposed work must be **open, fundamental research**
- No export-controlled, PHI, or other controlled data
- Need a project PI (principal investigator)

### Application Process
1. Submit project proposal at: https://my.olcf.ornl.gov/project-application-new
   - Select "OLCF Quantum Computing User Program"
2. Proposal reviewed by Quantum Resource Utilization Council (QRUC) + independent referees
3. Review criteria: scientific merit + feasibility on available resources
4. Applications accepted **year-round** (no fixed deadlines)
5. Once approved, receive a 6-character project ID
6. Apply for user accounts at: https://my.olcf.ornl.gov/account-application-new

### Credit Allocation
- Start with **0 HQCs** on hardware (H2-1, H2-2, Helios-1 share the same quota pool)
- Get **6,000 seconds** of emulator time
- PI must request hardware credits monthly via "Quantum Allocation Request" form on myOLCF
- Requests must be **justified using emulator results** (demonstrate workload feasibility)
- Credits reset monthly on the 1st - allocations do NOT carry over
- Monthly request deadline: 25th of previous month
- Allocations granted in two phases: first 3 weeks (guaranteed) + final week (resource-dependent)

### Our Strategy
- The experiment qualifies as open fundamental research (holographic geometry from MERA)
- We have extensive emulator-validated results (SIM-2026-002 through 008)
- The proposal would cite Anand et al. (PRX Quantum 2023) as direct precedent on Quantinuum hardware
- **Risk:** Allocation size is not published. We need ~25K HQCs minimum (16q validation). Monthly allocation may be much smaller, requiring multiple months of access.

### Key Constraint
- "Only project PIs can request credits" - need a PI with a US institution affiliation
- For an independent researcher, this may require collaboration with a university PI

---

## 4. Azure Quantum Credits Program

### Free Tier
- **$500 in credits** per Azure Quantum workspace, no application needed
- Covers: IonQ, Quantinuum H2, Rigetti, PASQAL
- $500 = 40 HQCs on Quantinuum (enough for ~1-2 trivial test circuits, NOT for our experiment)
- Good for: testing circuit compilation, running on emulators, validating the pipeline

### Research Grants (Larger Allocations)
- Grants of **up to $10,000** available for project teams and educators
- Application required (no published deadline - rolling)
- Past recipients: University of Washington, Bar-Ilan University, KPMG/DTU collaboration
- $10,000 = ~800 HQCs at commercial rates (still insufficient for full experiment)
- Contact: AzureQuantumInfo@microsoft.com

### How to Apply
1. Create Azure Quantum workspace in Azure Portal
2. Get automatic $500 in free credits
3. For larger grants: apply through Azure Quantum Credits program
4. Application link: via Azure Portal or contact AzureQuantumInfo@microsoft.com

### Assessment
- Free $500 is useful for pipeline validation on emulators
- $10K grant is useful but covers only ~3% of our 16q validation run at commercial rates
- **Best use: validate circuit compilation and run on H2 emulator before requesting QCUP allocation**

---

## 5. Quantinuum Direct Access (Nexus Platform)

### Sign Up
- Direct sign-up: https://nexus.quantinuum.com/signup
- Platform includes emulators, syntax checkers, and (with credits) hardware access
- Free emulator access may be available without purchasing hardware credits

### What's Available
- Quantinuum Nexus: cloud platform for running, tracking, managing quantum jobs
- Includes JupyterHub environment and H-Series emulator
- Hardware backends: H2-1, H2-2, Helios-1 (require HQCs)
- Syntax checkers: free (validate circuits without execution)

### Pay-as-You-Go Pricing
- Not publicly listed on Quantinuum's website
- Must contact: **Sales@Quantinuum.com**
- Likely same HQC rate as Azure ($12.50/HQC) or negotiated

### Research Collaboration
- Contact form: https://www.quantinuum.com/contact (select "Sales" or "General")
- Quantinuum has published research with academic collaborators (Anand et al., RIKEN, Sanger Institute)
- They may offer research credits for novel, publishable work
- Our experiment (first holographic force measurement on quantum hardware) could be compelling

---

## 6. Q-Net and Startup Partner Program

### Q-Net Community
- Hub for Quantinuum users: documentation, tutorials, webinars, trainings
- 2,500+ active users
- 170+ research papers on Quantinuum systems
- Annual Q-Net meeting (exclusive summit)
- Apply at: https://www.quantinuum.com/q-net

### Startup Partner Program
- For small businesses/startups in the quantum ecosystem
- Access to Nexus and InQuanto platforms
- Apply through Q-Net page
- **Assessment:** Our project is a research project, not a startup. This channel is less relevant unless we frame the work as building a product/service on Quantinuum hardware.

---

## 7. Government & Third-Party Programs

### DARPA Quantum Benchmarking Initiative (QBI)
- Quantinuum selected for Stage B (2025-2026)
- Tests utility-scale quantum computing (computational value > cost by 2033)
- NOT directly applicable to us (this is for quantum hardware vendors, not researchers)
- Relevant context: Quantinuum is proving Helios can deliver utility-scale results

### NRC Canada - Quantum Algorithms for Scientific Discovery
- Call for proposals for quantum algorithms research
- Partners with Canadian institutions
- Could be relevant if collaborating with a Canadian researcher

### NERSC IBM Quantum Innovation Center
- 2026 call for proposals
- IBM hardware only (not Quantinuum)

### Microsoft Quantum Pioneers Program
- Focused on measurement-based quantum computing
- Not directly relevant to our trapped-ion MERA experiment

---

## 8. Strategic Partnerships to Emulate

Quantinuum has established research partnerships with several institutions that could serve as models:

| Partner | Arrangement | Relevance |
|---|---|---|
| RIKEN (Japan) | On-site H2 installation, joint research | National lab partnership model |
| Sanger Institute (UK) | Q4Bio challenge, technology partner | Challenge/grant-based |
| STFC Hartree Centre (UK) | Joint Statement of Endeavour, H-Series access for UK researchers | Government partnership |
| Singapore NQO | MoU, Helios installation in Singapore (2026) | National partnership |
| NVIDIA | NVAQC founding collaborator, InQuanto + cuQuantum integration | Technology partnership |
| JPMorgan Chase | Joint published research (Nature 2026) | Industry partnership |
| University of Minnesota (MSI) | Faculty access to Quantinuum hardware | University-level partnership |

### What These Partnerships Have in Common
- Institutional backing (national lab, university, government, large company)
- Defined research agenda with publication plan
- Often facilitated by government funding or MoU
- Quantinuum benefits from published results demonstrating their hardware capabilities

---

## 9. Contact Information

| Purpose | Contact |
|---|---|
| Sales / Pay-as-you-go pricing | Sales@Quantinuum.com |
| General inquiries | https://www.quantinuum.com/contact |
| Azure Quantum questions | AzureQuantumInfo@microsoft.com |
| QCUP applications | https://my.olcf.ornl.gov/project-application-new |
| Nexus platform sign-up | https://nexus.quantinuum.com/signup |
| Q-Net community | https://www.quantinuum.com/q-net |

---

## 10. Recommended Action Plan

### Immediate (No Cost)
1. **Sign up for Quantinuum Nexus** (https://nexus.quantinuum.com/signup) - get free emulator access
2. **Create Azure Quantum workspace** - claim $500 free credits for emulator testing
3. **Validate circuit compilation** - translate our MERA circuit to pytket, test on H2/Helios emulator

### Short-Term (Research Access)
4. **Apply to QCUP** (if US-based with institutional PI) - best path to free Helios hardware
   - Prepare proposal citing Anand et al. precedent
   - Include emulator validation results
   - Request 16q validation run first (~25K HQCs)
5. **Contact Quantinuum Sales** (Sales@Quantinuum.com) - inquire about:
   - Pay-as-you-go pricing for Helios
   - Research collaboration / credits for publishable work
   - Whether they have an academic discount program
6. **Apply for Azure Quantum Credits** ($10K grant) for supplementary emulator time

### Medium-Term (If QCUP Not Available)
7. **University collaboration** - partner with a physics department that has Quantinuum access
   - University of Minnesota (MSI) has faculty access
   - Any Q-Net member institution
8. **Grant funding** - NSF, DOE, or DARPA proposals with Quantinuum hardware line item
9. **Quantinuum research pitch** - email research team with proposal for first holographic force measurement on quantum hardware (publishable in PRX Quantum or Nature Physics)

### Cost-Reduction Strategies
10. **Circuit optimization** - reduce N_2q (two-qubit gate count) to lower HQC cost
    - Our 140 CNOT count dominates the HQC formula (10x weight)
    - pytket compilation may reduce CNOT count by 20-40%
    - Native ZZPhase decomposition may be more efficient than CNOT decomposition
11. **Reduce shot count** - start with 10K shots (5x less than 5-sigma target) for proof-of-concept
12. **Start with 16q** - 25K HQCs vs 116K HQCs for 32q

---

## 11. Critical Finding: Cost Reassessment

Our earlier helios-mera-design.md estimated costs of $7.4K (academic) to $44K (commercial) based on assumed per-shot pricing. The actual HQC formula reveals costs that are **50-100x higher** because:

1. Two-qubit gates are weighted 10x in the HQC formula
2. Our 140-CNOT circuit is heavily penalized
3. The base HQC rate from Azure subscriptions is ~$12.50/HQC

**This fundamentally changes the access strategy.** Commercial purchase is infeasible. The viable paths are:
- **QCUP free allocation** (if sufficient monthly credits are granted)
- **Research partnership** (Quantinuum may offer credits for novel, publishable work)
- **Significant circuit compression** (reduce from 140 to ~50 CNOTs via pytket optimization)
- **Reduced experiment scope** (10K shots instead of 280K)

The cost structure strongly favors optimizing the circuit compilation before any hardware submission. Every CNOT eliminated saves ~$700 per 280K-shot run at commercial rates.

---

## Sources

- Quantinuum Helios product page: https://www.quantinuum.com/products-solutions/quantinuum-systems/helios
- Quantinuum HQC glossary: https://www.quantinuum.com/glossary-item/hardware-quantum-credits-hqcs
- Helios job costing docs: https://docs.quantinuum.com/systems/trainings/helios/getting_started/costing.html
- Azure Quantum pricing: https://learn.microsoft.com/en-us/azure/quantum/pricing
- Azure Quantum Credits FAQ: https://learn.microsoft.com/en-us/azure/quantum/credits-faq
- Azure Quantum Credits blog: https://azure.microsoft.com/en-us/blog/quantum/2022/10/20/azure-quantum-credits-program-propels-quantum-innovation-and-exploration-for-researchers-educators-and-students/
- OLCF QCUP: https://www.olcf.ornl.gov/olcf-resources/compute-systems/quantum-computing-user-program/
- QCUP Quantinuum docs: https://docs.olcf.ornl.gov/quantum/quantum_systems/quantinuum.html
- QCUP access docs: https://docs.olcf.ornl.gov/quantum/quantum_access.html
- Quantinuum Q-Net: https://www.quantinuum.com/q-net
- Quantinuum Nexus: https://nexus.quantinuum.com/signup
- Quantinuum contact: https://www.quantinuum.com/contact
- Helios launch press release: https://www.quantinuum.com/press-releases/quantinuum-announces-commercial-launch-of-new-helios-quantum-computer-that-offers-unprecedented-accuracy-to-enable-generative-quantum-ai-genqai
- DARPA QBI: https://www.quantinuum.com/press-releases/quantinuum-selected-by-darpa-to-advance-to-stage-b-of-quantum-benchmarking-initiative
- Azure Quantum HQC conversion: https://learn.microsoft.com/en-us/answers/questions/2152983/conversion-rate-between-azure-quantum-credit-and-o
