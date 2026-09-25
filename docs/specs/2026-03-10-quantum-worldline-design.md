# Quantum Worldline — Agent Team Design Spec

**Date:** 2026-03-10
**Status:** Approved
**Location:** `D:/quantum-worldline/`
**Type:** Claude Code Plugin

## Purpose

A multi-tier agent team for advancing research at the intersection of quantum computing, physics simulation, and worldline theory. The team discovers papers, tracks hardware, finds mathematical connections, designs and runs quantum circuits, generates testable hypotheses, and interprets implications — automating the research cycle: **discover → hypothesize → gate → test → interpret**.

## Core Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Architecture | Tiered orchestration (3 tier leads + specialists) | Scales cleanly, subagent delegation, parallelize within tiers |
| Interaction | Orchestrator-driven + scheduled scanning | Single entry point for user, automated literature monitoring |
| Data sources | Web + arxiv API (launch), Qiskit (Tier 2 milestone), HuggingFace throughout | Staged complexity, HF woven in from day one |
| Output | Structured JSON + markdown summaries | Machine-readable for agent chaining, human-readable for user |
| Theory ambition | Moderate with feasibility gating | Hypotheses must cite sources and propose tests. Feasibility Checker gates all output. |
| Location | `D:/quantum-worldline/` as Claude Code plugin | Portable, self-contained, installable |

## Plugin Structure

```
D:/quantum-worldline/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json                          # arxiv API server
├── CLAUDE.md
├── agents/
│   ├── worldline-orchestrator.md      # Top-level orchestrator
│   ├── literature-lead.md             # Tier 1 lead
│   ├── physics-scanner.md             # Tier 1: paper discovery
│   ├── hardware-tracker.md            # Tier 1: hardware roadmap
│   ├── math-bridge.md                 # Tier 1: mathematical connections
│   ├── synthesis-agent.md             # Tier 1: cross-domain patterns
│   ├── computation-lead.md            # Tier 2 lead
│   ├── qiskit-builder.md              # Tier 2: quantum circuit design
│   ├── classical-simulator.md         # Tier 2: classical baselines
│   ├── visualization-agent.md         # Tier 2: render results
│   ├── theory-lead.md                 # Tier 3 lead
│   ├── conjecture-generator.md        # Tier 3: hypothesis creation
│   ├── feasibility-checker.md         # Tier 3: hardware reality gate
│   └── philosophy-agent.md            # Tier 3: interpretation
├── skills/
│   ├── weekly-scan.md                 # Scheduled literature digest
│   ├── research-query.md              # On-demand deep dive
│   ├── hardware-status.md             # Quick roadmap check
│   ├── hypothesis-review.md           # Review theory output
│   └── simulate.md                    # Design + run circuits
├── hooks/
│   └── hooks.json                     # Output validation
├── research/
│   ├── data/
│   │   ├── papers/                    # Discovered papers (JSON)
│   │   ├── hardware/                  # Hardware milestones (JSON)
│   │   ├── simulations/               # Circuit designs + results
│   │   └── hypotheses/                # Hypothesis records (JSON)
│   ├── digests/                       # Weekly markdown summaries
│   └── knowledge-base.md             # Accumulated core knowledge
├── templates/
│   ├── paper-record.json
│   ├── hardware-milestone.json
│   ├── hypothesis-record.json
│   └── simulation-result.json
└── docs/
    └── specs/
        └── 2026-03-10-quantum-worldline-design.md
```

## Tier 1: Literature & Intelligence

### Literature Lead (sonnet)
Coordinates Tier 1 specialists. Dispatches Physics Scanner + Hardware Tracker in parallel for broad scans, Math Bridge for connection queries, Synthesis Agent for digest generation.

Returns:
```json
{
  "tier": "literature",
  "status": "NOVEL|CONFIRMED|WATCH",
  "findings": [...],
  "cross_references": [...],
  "recommended_followup": "theory|computation|none"
}
```

### Physics Scanner (sonnet)
Searches arxiv, web, and HuggingFace papers for research on quantum simulation, QFT on hardware, spacetime simulation, worldline physics, biological quantum modeling. Outputs structured paper records with relevance scoring (1-5). Pushes metadata to HF datasets.

### Hardware Tracker (sonnet)
Monitors IBM, Google, Quantinuum, QuEra, Microsoft, IonQ, PsiQuantum, Atom Computing, Pasqal, Fujitsu/RIKEN. Maintains running "frontier" of best numbers across vendors for physical qubits, logical qubits, error correction ratio, circuit depth, coherence time.

### Math Bridge (opus)
Finds mathematical connections between frameworks across subfields: Radon transforms ↔ quantum tomography, path integrals ↔ worldline formalism, tensor networks ↔ spacetime geometry (AdS/CFT), projection theory ↔ holographic principle, qLDPC codes ↔ algebraic geometry. Most likely agent to find unpublished connections.

### Synthesis Agent (sonnet)
Aggregates outputs from other Tier 1 agents into weekly digests. Identifies patterns, trends, gaps. Produces top 5 findings, hardware frontier update, new connections, research gaps, and relevance to core mission.

## Tier 2: Computation & Simulation

### Computation Lead (sonnet)
Coordinates hands-on computational work. Routes simulation requests, manages quantum vs classical comparison, triggers visualization.

Returns:
```json
{
  "tier": "computation",
  "status": "EXECUTED|DESIGNED|INFEASIBLE",
  "circuit": { "qubits": N, "depth": N, "gates": N },
  "results": { "quantum": {...}, "classical_baseline": {...} },
  "comparison": "advantage|parity|classical_wins",
  "hardware_target": "ibm_heron_r3|simulator|future_starling",
  "visualization_path": "research/data/simulations/..."
}
```

### Qiskit Builder (opus)
Phase 1: Design circuits in Qiskit, transpile, estimate resources, run on local simulator (qiskit-aer). Phase 2: Submit to real IBM hardware (requires API key, user approval, tracks 10 min/month budget). Logs all circuits as reproducible Python scripts. Pushes to HF datasets.

Guardrails: Never submits to real hardware without explicit user approval. Tracks cumulative execution time. Defaults to simulator.

### Classical Simulator (sonnet)
Runs classical equivalents for comparison. Python (numpy, scipy). Same output format as Qiskit Builder for direct comparison. The honest broker — prevents quantum hype.

### Visualization Agent (sonnet)
Renders results as matplotlib/plotly charts, Bloch spheres, probability histograms, timeline diagrams, comparison plots. Can push to HF Spaces.

## Tier 3: Theory & Interpretation

### Theory Lead (sonnet)
Coordinates hypothesis generation, feasibility gating, philosophical interpretation. All output flagged as speculative with confidence levels.

Returns:
```json
{
  "tier": "theory",
  "status": "HYPOTHESIS_GENERATED|NO_VIABLE_CONJECTURE|NEEDS_MORE_DATA",
  "hypotheses": [
    {
      "id": "HYP-2026-003",
      "claim": "...",
      "confidence": "low|medium|high",
      "source_findings": ["PAPER-xxx", "HW-xxx"],
      "testable": true,
      "test_design": "...",
      "hardware_required": "...",
      "earliest_testable": "2027-Q3",
      "philosophical_implications": "...",
      "status": "proposed|under_review|tested|refuted|supported"
    }
  ]
}
```

### Conjecture Generator (opus)
Creates testable hypotheses from Tier 1 findings. Every hypothesis must cite 2+ sources, include a proposed test, state what would refute it. Confidence = high only with multiple independent source chains. Pushes to HF dataset (AI-generated physics hypotheses with test designs).

### Feasibility Checker (opus)
Reality gate. Evaluates hardware feasibility, circuit feasibility, mathematical feasibility, resource feasibility. Verdicts: TESTABLE_NOW, TESTABLE_NEAR_TERM, TESTABLE_FUTURE, INFEASIBLE, NEEDS_REFINEMENT. Infeasible hypotheses archived with reason, not deleted.

### Philosophy Agent (opus)
Interprets findings through existing philosophical frameworks (eternalism, presentism, relational QM, IIT, holographic principle). Interpretation only — never generates hypotheses. Tracks which frameworks are strengthened/weakened. Explicitly labeled as philosophical interpretation. Can publish to HF papers.

## Orchestrator

### Worldline Orchestrator (opus)
Single entry point. Classifies requests, dispatches tier leads in parallel when possible, aggregates structured returns, presents unified summaries with cross-tier connections.

Status verdicts: NOVEL, CONFIRMED, CONTRADICTS, ACTIONABLE, WATCH.

Can escalate cross-tier: Literature finds paper → Theory generates hypotheses → Computation assesses feasibility.

## Skills

| Skill | Trigger | Action |
|---|---|---|
| `/qw-scan` | Weekly cron or on-demand | Full literature + hardware sweep → digest |
| `/qw-query` | On-demand | Route question through orchestrator |
| `/qw-hardware` | On-demand | Hardware frontier snapshot |
| `/qw-hypotheses` | On-demand | List active hypotheses with status |
| `/qw-simulate` | On-demand | Design circuit + classical baseline + compare |

## Data Flow

```
User → Orchestrator → Tier Lead(s) → Specialist(s)
                                          ↓
                                    Structured JSON (research/data/)
                                          ↓
                              Tier Lead aggregates
                                          ↓
                              Orchestrator merges
                                          ↓
                    Summary to user + Markdown digest
                                          ↓
                              HF Dataset push (async)
```

Cross-tier loop: discover → hypothesize → gate → test → interpret

## Model Allocation

| Agent | Model | Rationale |
|---|---|---|
| Worldline Orchestrator | opus | Decision-making, user-facing |
| Literature Lead | sonnet | Coordination |
| Physics Scanner | sonnet | Search + summarize |
| Hardware Tracker | sonnet | Structured extraction |
| Math Bridge | opus | Cross-domain mathematical reasoning |
| Synthesis Agent | sonnet | Pattern aggregation |
| Computation Lead | sonnet | Coordination |
| Qiskit Builder | opus | Correct quantum circuits |
| Classical Simulator | sonnet | Standard numerical work |
| Visualization Agent | sonnet | Chart generation |
| Theory Lead | sonnet | Coordination |
| Conjecture Generator | opus | Creative cross-domain reasoning |
| Feasibility Checker | opus | Rigorous assessment |
| Philosophy Agent | opus | Nuanced interpretation |

6 Opus, 8 Sonnet.

## Subagent Rules

1. Tier leads CAN dispatch their specialist agents
2. Specialists CANNOT dispatch other agents — return to lead
3. Orchestrator CAN dispatch leads and (bypass) specialists directly
4. All agents write structured output to research/data/
5. All agents have memory: user
6. No agent modifies another agent's output — append only

## Color Scheme

| Tier | Color |
|---|---|
| Orchestrator | cyan |
| Tier 1 (Literature) | blue |
| Tier 2 (Computation) | green |
| Tier 3 (Theory) | purple |

## MCP Integration

- **arxiv**: Lightweight MCP server wrapping arxiv REST API. Tools: search_papers, get_paper, get_citations. Fallback to WebSearch.
- **HuggingFace**: Already installed as plugin. No additional config.
- **IBM Quantum**: Deferred to Tier 2 milestone. Qiskit Builder writes Python scripts initially.

## Hooks

PostToolUse on Write: validate files in research/data/ against JSON schemas in templates/. Warn on malformed, don't block.

## Scheduled Operations

- Weekly (Sunday evening): /qw-scan full literature + hardware sweep
- On new hypothesis: auto-route through Feasibility Checker
