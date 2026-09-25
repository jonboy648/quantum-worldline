---
name: qw-query
description: "Route a single quantum physics or worldline theory question through the quantum worldline system. Natural language in, structured multi-tier response out. Use when the user asks a one-off research question. Not for the weekly digest (weekly-scan), quick hardware numbers (hardware-status), running circuits (simulate), or listing hypotheses (hypothesis-review)."
---

Route the user's research question through the quantum-worldline system.

Read ~/.claude/agent-memory/worldline-orchestrator/MEMORY.md for ID counters and accumulated knowledge.

## Dispatch Classification

### Quick queries (direct subagent, no team)
| Request | Dispatch |
|---------|----------|
| "What's the latest IBM hardware?" | hardware-tracker subagent |
| "Find papers on X" | physics-scanner subagent |
| "Is hypothesis X feasible?" | feasibility-checker subagent |
| "What does X mean philosophically?" | philosophy-agent subagent |

For these, spawn the relevant specialist directly as a subagent. No team needed.

### Multi-tier queries (agent team)

Create an agent team called "qw-query" with relevant tier leads:

#### For broad research ("Research X", "What's new in X"):
**Teammate 1:**
- name: literature-lead
- model: sonnet
- agent_type: literature-lead
- task: "Research: $ARGUMENTS. Dispatch physics-scanner and hardware-tracker subagents. Flag findings with relevance >= 4."

**Teammate 2:**
- name: theory-lead
- model: sonnet
- agent_type: theory-lead
- task: "Evaluate notable findings from literature-lead. Run hypothesis pipeline if warranted."

**Task Dependencies:**
```
Task 1: "Literature research on $ARGUMENTS" (literature-lead)
Task 2: "Theory evaluation of notable findings" (theory-lead, blockedBy: [1])
Task 3: "Synthesize and present results" (lead, blockedBy: [1, 2])
```

#### For simulation queries ("Can we simulate X"):
**Teammate 1:**
- name: computation-lead
- model: sonnet
- agent_type: computation-lead
- task: "Assess simulation feasibility for: $ARGUMENTS. Dispatch qiskit-builder and classical-simulator subagents."

**Task Dependencies:**
```
Task 1: "Simulation feasibility assessment" (computation-lead)
Task 2: "Present results" (lead, blockedBy: [1])
```

## Output
Present with: executive summary, findings by tier, status verdicts (NOVEL/CONFIRMED/CONTRADICTS/ACTIONABLE/WATCH), recommended next steps. Shut down teammates and clean up team when done.
