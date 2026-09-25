---
name: qw-scan
description: "Run a full quantum worldline literature and hardware sweep. Produces a weekly digest with top findings, hardware frontier updates, mathematical connections, and research gaps. Use for 'weekly scan', 'run the digest', or 'what's new in quantum this week'; scheduled weekly or on demand. For hardware numbers alone use hardware-status; for a specific question use research-query."
---

Run a full research scan using the quantum-worldline agent team.

Read ~/.claude/agent-memory/worldline-orchestrator/MEMORY.md for ID counters, key findings to track, and workflow notes.

## Standing Rules (2026-06-08 — inject these into EVERY teammate prompt)

1. **MCP search is QUERY-BLIND**: the paper-search MCP search endpoints return the latest-submission firehose regardless of keywords. All topical search goes through the arXiv export API via WebFetch: `http://export.arxiv.org/api/query?search_query=abs:%22...%22&sortBy=submittedDate&sortOrder=descending` (prefixes `abs:`/`ti:`/`cat:`; URL-encode). MCP read/download only for known paper IDs, fail-fast.
2. **Dedup before assigning IDs**: `grep -l "<arxiv-id>" research/data/papers/*.json` before creating any new PAPER/HW record. Duplicates become alias stubs (`alias_of` field), never new IDs.
3. **Verify ID high-water on disk** before the scan (memory counters drift): `ls research/data/papers/ | sort -V | tail`.
4. **Verdict write-backs are mandatory**: every hypothesis touched gets status + feasibility_verdict + dated result_note written into its JSON, same session.
5. **Anchor list must use ERRATA-corrected numbers** — check `research/ERRATA.md` (e.g. transport residual is ~1.2% at N=16 dt-converged, NOT 0.72%).

## Team Configuration

Create an agent team called "qw-scan" with 3 teammates:

### Teammate 1
- name: literature-lead
- model: sonnet
- agent_type: literature-lead
- task: "Run a full Tier 1 scan. Dispatch all specialists as subagents: physics-scanner for new papers, hardware-tracker for hardware updates, math-bridge for cross-field connections. Run synthesis-agent to produce a digest. Flag any findings with relevance >= 4 for theory routing."

### Teammate 2
- name: theory-lead
- model: sonnet
- agent_type: theory-lead
- task: "Stand by for findings from literature-lead. When notable findings arrive (relevance >= 4), run the full hypothesis pipeline: conjecture-generator -> feasibility-checker -> philosophy-agent for surviving hypotheses. Archive infeasible hypotheses."

### Teammate 3
- name: computation-lead
- model: sonnet
- agent_type: computation-lead
- task: "Stand by for TESTABLE_NOW hypotheses from theory-lead. If any arrive, design test circuits and classical baselines via qiskit-builder and classical-simulator subagents. Visualize results via visualization-agent."

## Task Dependencies

```
Task 1: "Full literature and hardware scan" (literature-lead)
Task 2: "Generate and evaluate hypotheses from notable findings" (theory-lead, blockedBy: [1])
Task 3: "Design and run simulations for testable hypotheses" (computation-lead, blockedBy: [2])
Task 4: "Synthesize cross-tier findings into weekly digest" (lead, blockedBy: [1, 2, 3])
```

## Synthesis (Lead's Job - Task 4)

After all teammates complete:
1. Read all output from tier leads
2. Classify findings: NOVEL, CONFIRMED, CONTRADICTS, ACTIONABLE, WATCH
3. Save digest to research/digests/ with today's date
4. Update research/knowledge-base.md if frontier numbers changed
5. Update ~/.claude/agent-memory/worldline-orchestrator/MEMORY.md with new ID counters and key findings
6. Display: executive summary, findings by tier, cross-tier connections, next steps
7. Shut down teammates and clean up team
