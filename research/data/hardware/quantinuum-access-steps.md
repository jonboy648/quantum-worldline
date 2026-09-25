# Quantinuum Helios Access - Actionable Steps

**Date:** 2026-03-18
**Goal:** Get hardware time on Quantinuum Helios for 32-qubit MERA holographic force measurement
**Circuit:** 32 qubits, 3 layers, ~140 CNOTs, ~200 single-qubit gates

---

## Our Circuit's HQC Cost Estimate

Quantinuum bills in Hardware Quantum Credits (HQCs):

```
HQC = 5 + C * (N_1q + 10 * N_2q + 5 * N_m) / 5000
```

For our 32q/3L MERA circuit:
- N_1q = ~200 (single-qubit gates)
- N_2q = 140 (two-qubit gates / CNOTs)
- N_m = 64 (32 initial state preps + 32 final measurements)
- Per-shot gate cost: (200 + 10*140 + 5*64) / 5000 = 1920/5000 = 0.384

| Shots | HQC Cost |
|-------|----------|
| 1 | 5.4 |
| 100 | 12.8 |
| 1,000 | 389 |
| 10,000 | 3,845 |

For statistical significance on force measurements, we need ~1,000-10,000 shots per circuit configuration, across ~10 hologron positions = **3,900 - 38,450 HQCs total**.

---

## Pathway 1: Azure Quantum Free Credits (FASTEST START)

**What you get:** $500 free Azure Quantum Credits = up to **800 HQCs** on Quantinuum hardware + unlimited emulator access. Credits never expire (no time limit).

**What hardware is accessible:** Currently H2-1 and H2-2 (56 physical qubits each) are listed on Azure Quantum. Helios-1 is NOT yet confirmed on Azure Quantum - the Azure provider page (updated Jan 2026) still lists only H2 targets. However, H2 has 56 qubits, which is sufficient for our 32-qubit circuit.

**800 HQCs gets us:** ~2 circuit configurations at 1,000 shots each. Enough for a proof-of-concept run (single hologron position, measure force at 2-3 separations).

### Exact Steps

1. **Create an Azure account** (if you don't have one)
   - Go to: https://azure.microsoft.com/free/
   - Requires: email, phone number, credit/debit card (for identity verification - you won't be charged for free credits)
   - Choose "Pay-as-you-go" subscription

2. **Create an Azure Quantum workspace**
   - Sign in to: https://portal.azure.com
   - Click "Create a resource" and search "Azure Quantum"
   - Select "Azure Quantum" then "Create"
   - Use **Quick create** (recommended) - this automatically adds Quantinuum, IonQ, Rigetti, and Microsoft providers
   - Enter a workspace name, select a region (e.g., "West US"), click "Create"
   - Deployment takes a few minutes

3. **Verify free credits**
   - In your workspace, go to the "Operations" section, then "Quotas" blade
   - You should see 800 HQCs for Quantinuum credited automatically
   - Credits appear immediately upon workspace creation

4. **Submit jobs via Qiskit or Q#**
   - Install: `pip install azure-quantum qiskit`
   - Target IDs:
     - Syntax checker (free): `quantinuum.sim.h2-1sc`
     - Emulator (free with subscription): `quantinuum.sim.h2-1e`
     - Hardware: `quantinuum.qpu.h2-1`
   - Always validate with syntax checker first, then emulator, then hardware

**Key URLs:**
- Azure portal: https://portal.azure.com
- Workspace creation docs: https://learn.microsoft.com/en-us/azure/quantum/how-to-create-workspace
- Free credits FAQ: https://learn.microsoft.com/en-us/azure/quantum/azure-quantum-credits
- Quantinuum provider details: https://learn.microsoft.com/en-us/azure/quantum/provider-quantinuum
- Pricing details: https://learn.microsoft.com/en-us/azure/quantum/pricing
- Contact: AzureQuantumInfo@microsoft.com

**Limitation:** 800 HQCs is enough for proof-of-concept but not for the full force profile measurement (~3,900+ HQCs needed). For the full experiment, use Pathway 2 or 3.

---

## Pathway 2: ORNL QCUP (BEST FOR FULL EXPERIMENT)

**What you get:** Free allocation of HQCs on Quantinuum hardware (including Helios-1), reviewed and granted by merit. QCUP has confirmed access to **H2-1, H2-2, and Helios-1** (plus emulators and syntax checkers). This is the only confirmed free pathway to Helios specifically.

**Eligibility:** Open to researchers worldwide for open, fundamental research. QCUP users include "US national labs, universities, government, and industry." No explicit US-only restriction, but all work must be unclassified and publishable. No export-controlled, PHI, or controlled data.

**Applications:** Accepted year-round. Merit-reviewed by the Quantum Resource Utilization Council (QRUC) and independent referees.

### Exact Steps

1. **Prepare your proposal** (before going to the form). You will need:
   - Project title and PI information
   - Description of the nature, methodology, and merits of the project
   - Justification for why QCUP quantum resources are needed
   - Estimated resource requirements (HQCs) - justified with emulator results
   - Statement that all work is open fundamental research

2. **Submit the project proposal**
   - Go to: https://my.olcf.ornl.gov/project-application-new
   - Select "OLCF Quantum Computing User Program" from the program dropdown
   - Fill out all required fields
   - Submit

3. **Wait for QRUC review**
   - Timeline: not published, but reviews are rolling (no fixed deadlines)
   - You will be notified of the decision via email
   - If approved, you sign a PI Agreement

4. **Set up user accounts**
   - Once project is approved, you receive a 6-character OLCF Project ID
   - Apply for individual user account at: https://www.olcf.ornl.gov/for-users/documents-forms/quantum-account-application/
   - PI must approve each user account

5. **Request Quantinuum-specific allocation**
   - Log into myOLCF
   - Use the Quantum Allocation Request form
   - Specify HQC amounts justified by emulator results (run on Helios-1E first)
   - OLCF handles vendor access setup - you receive an email invitation from Quantinuum

6. **Access Quantinuum via Nexus**
   - Log in at: https://nexus.quantinuum.com
   - Or use OLCF JupyterHub for browser-based development
   - Or configure local Python with Guppy/pytket
   - Available backends: `H2-1`, `H2-2`, `Helios-1`, plus emulators `H2-1E`, `H2-2E`, `Helios-1E`

**Key URLs:**
- QCUP main page: https://www.olcf.ornl.gov/olcf-resources/compute-systems/quantum-computing-user-program/
- Project proposal form: https://my.olcf.ornl.gov/project-application-new
- User account application: https://www.olcf.ornl.gov/for-users/documents-forms/quantum-account-application/
- QCUP access documentation: https://docs.olcf.ornl.gov/quantum/quantum_access.html
- Quantinuum on QCUP: https://docs.olcf.ornl.gov/quantum/quantum_systems/quantinuum.html
- QCUP FAQs: https://www.olcf.ornl.gov/olcf-resources/compute-systems/quantum-computing-user-program/qcup-faqs/
- Support: help@olcf.ornl.gov

**Recommendation:** This is the strongest pathway for a full experiment. The proposal aligns well with QCUP's mission (fundamental open research on quantum hardware). Start here in parallel with Pathway 1.

---

## Pathway 3: Quantinuum Nexus Direct (HELIOS CLOUD ACCESS)

**What you get:** Direct cloud access to Helios through Quantinuum's own platform. Commercial pricing - no published rates for Helios (contact sales). H2 Standard plan is $125,000/month for 10k HQCs via Azure.

**Access model:** Not instant. You register interest and Quantinuum evaluates fit. "Not everyone will be able to access Nexus during this time." Promotional access may be granted to good-fit customers.

### Exact Steps

1. **Register interest for Nexus**
   - Go to: https://nexus.quantinuum.com/signup
   - Fill out the registration form (name, email, organization, use case)
   - This puts you on the interest list

2. **Request Helios cloud access specifically**
   - Go to: https://www.quantinuum.com/products-solutions/quantinuum-systems/helios
   - Scroll to the contact form ("If you're interested in on-premises or cloud access to Helios, fill out this form")
   - Describe your research and circuit requirements

3. **Contact sales for academic pricing**
   - Email: Sales@Quantinuum.com
   - Reference: academic/research use, 32-qubit MERA circuit, ~4,000-40,000 HQCs needed
   - Ask about: academic discount programs, research partnerships, promotional credits

4. **If granted access, log in to Nexus**
   - URL: https://nexus.quantinuum.com/auth/login
   - Documentation: https://docs.quantinuum.com/nexus/
   - Getting started guide: https://docs.quantinuum.com/nexus/trainings/notebooks/basics/getting_started.html

**Key URLs:**
- Nexus signup: https://nexus.quantinuum.com/signup
- Nexus login: https://nexus.quantinuum.com/auth/login
- Helios product page: https://www.quantinuum.com/products-solutions/quantinuum-systems/helios
- Nexus documentation: https://docs.quantinuum.com/nexus/
- Signup documentation: https://docs.quantinuum.com/nexus/user_guide/sign_up.html
- Sales contact: Sales@Quantinuum.com

**Limitation:** Pricing is opaque and likely expensive without a research partnership. Best used as a supplementary approach alongside QCUP.

---

## Experiment Pitch (for applications and outreach)

> We propose the first measurement of holographic gravitational forces in a MERA quantum circuit on Quantinuum Helios. Our 32-qubit, 3-layer circuit (140 CNOTs) implements a multiscale entanglement renormalization ansatz for the critical transverse-field Ising model. Classical simulator results demonstrate holographic transport matching Anti-de Sitter lightcone predictions at 0.72% accuracy, and gravitational force decay consistent with stress-tensor exchange (m_eff = 1.85). Hardware execution would confirm emergent Anti-de Sitter geometry in a quantum processor - the first experimental evidence that a programmable quantum device reproduces the causal and geometric structure of a holographic spacetime. The all-to-all connectivity of Helios trapped-ion qubits maps our MERA topology with zero SWAP overhead, and the circuit depth (140 two-qubit gates) is well within Helios's coherence budget at 99.92% two-qubit gate fidelity.

---

## Recommended Action Plan

| Priority | Action | Timeline | Blocker |
|----------|--------|----------|---------|
| 1 | Create Azure Quantum workspace, claim 800 free HQCs | Today | None |
| 2 | Run MERA circuit on H2 emulator via Azure (validate compilation) | This week | Azure account |
| 3 | Submit QCUP proposal for Helios allocation | This week | Need emulator results to justify HQC request |
| 4 | Register on Quantinuum Nexus | This week | None |
| 5 | Submit Helios interest form on Quantinuum website | This week | None |
| 6 | Run proof-of-concept on H2 hardware with Azure free credits | After emulator validation | Emulator success |
| 7 | Full force profile on Helios via QCUP | After QCUP approval | QCUP review |

**Critical path:** Steps 1-3 can all happen in parallel this week. The QCUP proposal is the gating item for Helios access, so submit it as soon as emulator results are in hand.
