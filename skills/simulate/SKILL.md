---
name: qw-simulate
description: "Design a quantum circuit, run it on a simulator, compare with classical baseline, and visualize results. Takes a system description or hypothesis ID as input. Use when the user says 'simulate X', 'run the circuit', 'test hypothesis HYP-N numerically', or wants a sim-vs-classical comparison."
---

Run a quantum simulation with classical comparison for: $ARGUMENTS

Read ~/.claude/agent-memory/worldline-orchestrator/MEMORY.md for context and ID counters.

## Team Configuration

Create an agent team called "qw-simulate" with teammates:

### Teammate 1
- name: computation-lead
- model: sonnet
- agent_type: computation-lead
- task: "Design and run simulation for: $ARGUMENTS. Dispatch these subagents: qiskit-builder (circuit design + quantum simulation on qiskit-aer), classical-simulator (baseline comparison), visualization-agent (render results). Save circuits to research/data/simulations/."

### Teammate 2 (if hypothesis ID referenced)
- name: theory-lead
- model: sonnet
- agent_type: theory-lead
- task: "Provide context on the hypothesis being tested. After simulation completes, evaluate results against predictions and update feasibility verdict."

## Task Dependencies

```
Task 1: "Design circuit and run quantum + classical simulations" (computation-lead)
Task 2: "Evaluate results against hypothesis predictions" (theory-lead, blockedBy: [1]) — only if hypothesis referenced
Task 3: "Present comparison results" (lead, blockedBy: [1, 2])
```

## Output

Present:
- Circuit specs (qubits, depth, gates)
- Quantum vs classical results
- Verdict: advantage / parity / classical_wins
- Visualization
- If testing a hypothesis: updated feasibility verdict
- Shut down teammates and clean up team
