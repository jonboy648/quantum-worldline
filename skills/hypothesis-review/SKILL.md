---
name: qw-hypotheses
description: "List all active quantum-worldline hypotheses with their status, confidence level, feasibility verdict, and earliest testable date. Filter by status or confidence. Use when the user asks 'hypothesis review', 'what hypotheses are open', or 'which are testable now'. Listing only - to actually test one, use simulate."
---

List and review quantum worldline hypotheses.

1. Read all JSON files in research/data/hypotheses/
2. Display as a formatted table:
   | ID | Claim (truncated) | Confidence | Feasibility | Earliest Testable | Status |
3. Sort by confidence (high first), then by earliest_testable (soonest first)
4. If the user asks about a specific hypothesis, show full details including test design and philosophical implications
5. If no hypotheses exist yet, inform the user and suggest running /qw-scan to generate findings that can seed hypothesis generation.
