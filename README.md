# quantum-worldline

**Multi-tier AI agent team for quantum physics research.**

An independent researcher and a 14-agent AI team built a tensor-network research pipeline, measured a
power-law force inside MERA circuits, reproduced conformal data across three CFT classes -- and then
subjected the whole program to a formal adversarial audit that **withdrew its own headline result**. No
physics degree. No university affiliation. One RTX 4060, a few dollars of cloud compute, and a question:
*can math prove that pattern recognition creates geometry?*

The current honest answer: the pipeline works and the conformal data are accurate, but the specific claim
that the emergent geometry carries *quantitative gravitational* content did not survive its own audit. The
record of that failure is kept here in full, and is the part of this repo most worth reading.

---

## Key Results

> ### The former headline is WITHDRAWN
>
> This section previously led with *"the force exponent is alpha = 2\*Delta_T = 4, and it does not depend
> on what the material is made of."* That claim is **retracted as of 2026-08-17**. The published
> alpha = 3.92 +/- 0.16 is an artifact of the fitting procedure: an unweighted least-squares fit in linear
> space places **95.8% of its objective on the single point dr = 2**. Changing only the error model, and
> discarding no data, gives 2.82; log-space regression gives 2.89; across 15 defensible estimator x window
> choices the exponent spans 2.53 to 3.92 and **the published value is the maximum of all fifteen**.
>
> The corrected measurement is **alpha = 2.6 +/- 0.2** -- a genuine plateau, six consecutive local
> log-slopes flat to 7.5%. It matches neither 2\*Delta_T = 4 (stress tensor) nor 2\*Delta_epsilon = 2
> (scalar), so **the exchange channel is an open question.** See
> [`SIM-2026-072`](research/data/simulations/SIM-2026-072.json), [`ERRATA.md`](research/ERRATA.md) E6, and
> [`AUDIT-2026-08-11.md`](docs/governance/AUDIT-2026-08-11.md) D-2/D-3.

| Result | Measurement | Prediction | Status |
|--------|-------------|------------|--------|
| ~~Holographic force exponent~~ | ~~alpha = 4.0 (3.92 / 3.97 / 4.07)~~ | ~~2\*Delta_T = 4~~ | **WITHDRAWN** -- corrected to 2.6 +/- 0.2, channel open |
| Delta_T across 3 classes | 1.998 / 2.007 / 1.997 | Delta_T = 2 in every unitary 2D CFT | accurate (~0.2%), but **fixed in advance by a theorem** |
| OPE structure constant | C_sigma-sigma-epsilon = 0.50 +/- 0.03 | 0.5 (exact) | holds -- a real validation |
| Stress-tensor self-coupling | C_TTT = 3.9936 / 3.381 / 3.163 | 4.000 / 3.3806 / 3.16228 | holds (<=0.16%); **not independent** of c (Virasoro identity) |
| Causal transport time | residual -1.21% at N=16 | T = (pi/2)\*l_AdS | **disputed** -- see note below |
| Effective mass | m_eff = 0.670 | 0.693 | 3.5% |
| Z2 ground state (24q) | E error = 3.33%, P = 1.000 | -- | method result, holds |

The three universality classes are **Ising (c=1/2)**, **tricritical Ising (c=7/10)**, and **3-state Potts
(c=4/5)**. Reproducing Delta_T = 2 in all three is a correctness check on the pipeline, and it passed at
0.2%. What it is *not* is a discovery: Delta_T = 2 is a theorem in every unitary 2D CFT, so no other
outcome was available to a working implementation. The audit classifies 21 of the program's 34 calculated
claims this way -- accurate, and unable to have come out otherwise. See
[`RESEARCH-DIRECTOR.md`](docs/governance/RESEARCH-DIRECTOR.md) §6 on counterfactual novelty.

> **Note on the transport anchor.** Beyond the dt artifact recorded below, the audit raised two unresolved
> problems: the paper's own chi = 3 result gives l_AdS = 0.9102, which moves the prediction to 1.430
> against a measurement of 2.239 (+57%); and the Wang-He derivation cited in support proves t_trans = pi
> *independently of the AdS radius*, so it cannot underwrite a claim of the form T = (pi/2)\*l_AdS. See
> AUDIT D-1 (with its resolution box) and D-13.

> **Note on the transport number.** Earlier versions of this README and of Zenodo v3 quoted **0.72%**.
> That value is a time-grid artifact (dt=0.05) and is **superseded**: the dt-converged residual is
> **-1.21% at N=16**, shrinking from -2.78% at N=12 consistent with finite-size convergence. See
> [`research/ERRATA.md`](research/ERRATA.md) entry E2. The qualitative result T ~ (pi/2)*l_AdS survives;
> the precision claim does not.

A power-law force and Sahay-Lukin-Cotler's exponential force (PRX 15, 021078) were previously described
here as complementary projections of one duality -- we the boundary CFT conformal block, they the bulk AdS
graviton propagator. **That reading is suspended.** It depended on identifying our exponent with the
stress-tensor block, and alpha = 2.6 does not make that identification. The functional forms still differ;
what the difference means is now undetermined.

---

## Architecture

```
User
  |
  v
Worldline Orchestrator ──────────────────────────────────
  |              |                |
  v              v                v
Tier 1:        Tier 2:          Tier 3:
Literature     Computation      Theory
Lead           Lead             Lead
  |              |                |
  ├─ Physics     ├─ Qiskit       ├─ Conjecture
  │  Scanner     │  Builder      │  Generator
  ├─ Hardware    ├─ Classical    ├─ Feasibility
  │  Tracker     │  Simulator    │  Checker
  ├─ Math        └─ Visualization└─ Philosophy
  │  Bridge         Agent           Agent
  └─ Synthesis
     Agent
```

**14 agents** organized in 3 tiers. Tier leads dispatch specialists as subagents. Structured JSON flows up; commands flow down. The orchestrator merges cross-tier findings into weekly digests.

---

## Quick Start

The repo carries a `.claude-plugin/plugin.json`, but it is **not** installed through the plugin manager.
Agents deploy by **copy** and skills by **symlink**:

```bash
# Clone the repo
git clone https://github.com/Jonboy648/quantum-worldline.git
cd quantum-worldline

# Deploy the 14 agents to ~/.claude/agents/ (REQUIRED -- the runtime loads the copies,
# not the files in agents/. Re-run this after editing any agent.)
scripts/sync-agents.sh

# Symlink the 6 skills into ~/.claude/skills/ (skill edits then take effect immediately)
# ...then, from a Claude Code session in this directory:
/weekly-scan
/research-query "What is the current evidence for holographic forces in MERA?"
/hardware-status
```

> **Gotcha worth knowing:** because the plugin is not installed via the manager, `hooks/hooks.json`
> (the research/data ID-format check) never loads and is currently inert.

### Skills

| Skill | Purpose |
|-------|---------|
| `/weekly-scan` | Full literature + hardware sweep (weekly or on-demand) |
| `/research-query` | Route a question through the orchestrator |
| `/hardware-status` | Hardware frontier snapshot |
| `/hypothesis-review` | List active hypotheses with status |
| `/simulate` | Design circuit + classical baseline + compare |
| `/worldline-orchestrator` | Dispatch chooser: full 3-tier team, or a single specialist |

---

## Project Structure

```
quantum-worldline/
├── agents/              14 agent definitions (markdown + frontmatter)
├── skills/              6 skill definitions
├── templates/           JSON schemas for structured output
├── hooks/               Validation hooks
├── docs/                Design specs and implementation plans
├── research/
│   ├── data/
│   │   ├── papers/      139 paper records (through PAPER-138, incl. alias stubs)
│   │   ├── hardware/    76 hardware milestone records (through HW-074)
│   │   ├── hypotheses/  30 hypothesis records with status tracking
│   │   └── simulations/ 74 simulation records (through SIM-072) + Python/Julia drivers
│   ├── digests/         28 research digests (19 weekly scans)
│   ├── learning/        Layered learning guides (intuitive -> physics -> philosophy)
│   ├── ERRATA.md        Known errors + corrections -- CHECK BEFORE QUOTING ANY NUMBER
│   ├── RESEARCH-LOG.md  Chronological narrative
│   └── knowledge-base.md
├── CLAUDE.md            Project conventions for Claude Code
├── .claude-plugin/      Plugin manifest (not installed via plugin manager)
└── .mcp.json            MCP server configuration
```

---

## The Origin

In early 2025, a conversation with an AI explored whether ADHD-style pattern recognition -- the ability to sense connections, hold multiple threads simultaneously, perceive the big picture before the details resolve -- might have a mathematical connection to quantum physics. The question that emerged: *"Is there a way to have math actually prove any of this?"*

MERA (Multi-scale Entanglement Renormalization Ansatz) turned out to be the answer. It's a hierarchical pattern recognition algorithm that processes quantum information at multiple scales -- and its layer structure spontaneously generates a curved spacetime geometry (anti-de Sitter space). The question became: is that geometry real? Does it have forces, signals, gravity?

Eighteen months later, the honest answer is *partly, and less than this README once claimed*. The
machinery works: MERA circuits optimized to criticality reproduce conformal data to a fraction of a
percent across three universality classes, and the OPE coefficient C_sigma-sigma-epsilon = 0.50 +/- 0.03
is a real validation of the pipeline against an exactly known number. But the specific bridge from
"accurate CFT representation" to "geometry with gravitational content" is the piece that broke. The force
exponent that was supposed to carry it is withdrawn, and the transport anchor is disputed on two
independent grounds.

The audit put this as a test: delete every occurrence of the word *geometric* from the manuscript and see
what technical content is lost. The answer was none. That is the open problem the program now actually
has, and it is stated as [`RESEARCH-DIRECTOR.md`](docs/governance/RESEARCH-DIRECTOR.md) §29 -- what
operational content, if any, does emergent geometry add beyond an accurate tensor-network representation
of a CFT?

The program has been just as willing to record what *failed*. Six hypotheses were refuted outright
(HYP-014, 016, 022, 023 plus HYP-017 shelved on five killer issues and HYP-024 traced to a finite-size
artifact); HYP-008, the force-law hypothesis this project was largely built around, fell to
NOT_ESTABLISHED on 2026-08-17 under its own re-analysis. Those negatives are in
`research/data/hypotheses/` alongside the survivors, which is the point. The most useful single artifact
here may be [`AUDIT-2026-08-11.md`](docs/governance/AUDIT-2026-08-11.md): a 23-agent adversarial review,
including agents briefed specifically to destroy the project's own conclusions, that succeeded.

---

## Research Data

All structured research data is included:

- **139 paper records** cataloged with relevance scores, status verdicts (NOVEL/CONFIRMED/CONTRADICTS/ACTIONABLE/WATCH), and cross-references
- **76 hardware milestones** tracking Quantinuum, IBM, IonQ, QuEra, Google, Pasqal, and others
- **74 simulation records** from architecture validation through the force law (SIM-011), the universality ladder (SIM-051/052/062/063), the C_TTT extraction (SIM-067/068/069), the Yang-Lee central charge (SIM-070/071), and the re-analysis that withdrew the headline (SIM-072)
- **31 hypotheses** with confidence levels, feasibility verdicts, test designs, and refutation criteria -- **including the refuted ones**, with the evidence that killed them
- **19 weekly scan digests** documenting the research progression
- **3-part learning guide** (intuitive, physics, connections) with figures
- **`research/ERRATA.md`** -- a maintained record of our own published errors and their corrections

---

## Hardware Path

The paper includes a hardware design for Quantinuum Helios:

- 32 boundary qubits, 3 MERA layers
- **57 CNOT gates** (pytket compilation with Helios-native gateset)
- **0.57% accumulated logical error** (vs 41.2% on IBM Heron -- not viable)
- QCUP proposal PHY204 submitted to ORNL, requesting 15,671 HQC. **Status: stalled** -- the ORNL
  contact redirected to a general help address and the proposal has not advanced. Access for
  unaffiliated researchers remains the open problem; commercial cloud credits are the documented
  end-run.

**Hardware precedent (2026-07):** PAPER-137 (arXiv:2607.12047) reports what its authors describe as the
first trapped-ion realization of a HaPPY holographic code, experimentally confirming the FLM
bulk-boundary entropy formula. That is
direct precedent that holographic-tensor-network circuits of this class are runnable on today's hardware.

---

## How This Was Built

This project was built through genuine AI-human collaboration:

- **Jon Cackler** (Independent Researcher): Research direction, physics intuition, domain questions, experimental design decisions
- **Claude** (Anthropic): Literature search, simulation code, agent infrastructure, computation, paper drafting

The 14-agent architecture was designed to automate the research cycle: **discover -> hypothesize -> gate -> test -> interpret**. Each agent has a specific role, structured output format, and position in the tier hierarchy. The system has run 19 literature scans, generated 31 hypotheses, executed 74 simulations, produced the paper -- and, in a 23-agent adversarial pass, retracted its central claim. All coordinated through the orchestrator.

A deliberate design choice: every hypothesis must pass a **Feasibility Checker** gate before it can be
reported, and each one carries explicit refutation criteria written *before* the test runs. That is why
the refuted hypotheses are still in the repo. A pipeline in which nothing ever fails is a pipeline that
is not testing anything.

**No priority claim is made for the architecture.** Multi-agent AI systems for autonomous scientific
discovery are already published: **Kosmos** (Rosenfeld et al., arXiv:2511.02824) performs autonomous
discovery with a multi-agent architecture, and **SciSciGPT** (Wang et al., *Nature Computational
Science*, 2026) is a multi-agent system for science-of-science research; see also Sun et al.,
*Nature* (2026) on how AI tools reshape individual versus collective exploration. What this repo
offers instead is the complete working record of one such system applied end to end to a single
physics program: the agents, the structured data, the refuted hypotheses, the errata -- and a formal
adversarial audit of its own output ([`docs/governance/AUDIT-2026-08-11.md`](docs/governance/AUDIT-2026-08-11.md))
that withdrew the project's own headline number. The audit trail is the contribution, not the novelty.

> *Withdrawn 2026-08-17:* this line previously read "This may be the first open-source example of a
> multi-tier AI agent team producing original scientific research with quantitative results." That is
> an ungated priority claim (RESEARCH-DIRECTOR.md §8) and it is retracted -- the three references above
> sat uncited in the project's own bibliography when it was written. Audit ref: CLM-042 / D-5.

---

## Citation

Preprint and full reproduction package are archived on Zenodo:

> J. Cackler, "Power-Law Holographic Forces and Causal Transport in MERA Quantum Circuits" (2026).
> Concept DOI: [10.5281/zenodo.19660302](https://doi.org/10.5281/zenodo.19660302) (always resolves to the current version).

Submitted to Physical Review D. arXiv posting is pending endorsement -- the standard obstacle for an
unaffiliated author, and the reason the Zenodo record exists.

> **Correction pending.** Both the submitted manuscript and the archived Zenodo record carry the
> withdrawn alpha = 3.92 +/- 0.16 as their central result. The error was found in an internal audit after
> submission; a correction package is prepared at
> [`docs/governance/PRD-CORRECTION-PACKAGE.md`](docs/governance/PRD-CORRECTION-PACKAGE.md) and the
> journal contact is pending. **Do not cite the force exponent from either artifact.** Cite
> [`SIM-2026-072`](research/data/simulations/SIM-2026-072.json) for the corrected measurement.

---

## License

MIT License. See [LICENSE](LICENSE).
