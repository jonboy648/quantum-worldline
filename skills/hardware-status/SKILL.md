---
name: qw-hardware
description: "Quick snapshot of the current quantum hardware frontier -- best numbers across all vendors for qubits, error correction, coherence, and circuit depth. One-screen summary. Use when the user asks 'hardware status', 'best qubit counts', or whether a hypothesis is testable on today's machines. For a full literature + hardware sweep use weekly-scan."
---

Display the current quantum hardware frontier.

1. Read research/knowledge-base.md and extract the "Current Hardware Frontier" table.
2. Display the frontier table to the user.
3. If the user wants updated numbers, spawn hardware-tracker as a direct subagent (no team needed) with prompt: "Check for any new quantum hardware announcements since the last scan. Report new findings."
4. Update the frontier table if new data is found.
