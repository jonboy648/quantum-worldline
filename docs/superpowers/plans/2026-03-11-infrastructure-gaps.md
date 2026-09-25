# Quantum Worldline Infrastructure Gaps — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close all infrastructure gaps so the quantum-worldline agent team is fully wired: symlinked agents, MCP tool access in subagents, Semantic Scholar API key, HuggingFace dataset push, and end-to-end skill tests.

**Architecture:** Six independent fixes. Tasks 1-3 are file edits (agents, MCP config). Task 4 is HF integration. Task 5 is a Semantic Scholar key. Task 6 is end-to-end verification of all skills.

**Tech Stack:** Claude Code agents/skills (markdown), MCP servers (paper-search-mcp), HuggingFace Hub CLI, Semantic Scholar API.

---

## Chunk 1: Agent Symlinks and MCP Tool Access

### Task 1: Replace Agent Copies with Symlinks

**Problem:** 14 agents in `~/.claude/agents/` are copies of files in `D:/quantum-worldline/agents/`. Edits to source require manual re-copy.

**Solution:** Delete copies, create symlinks. Skills already use this pattern successfully.

**Files:**
- Delete: `~/.claude/agents/{classical-simulator,computation-lead,conjecture-generator,feasibility-checker,hardware-tracker,literature-lead,math-bridge,philosophy-agent,physics-scanner,qiskit-builder,synthesis-agent,theory-lead,visualization-agent,worldline-orchestrator}.md`
- Create: symlinks from same paths -> `D:/quantum-worldline/agents/*.md`

- [ ] **Step 1: Verify current agent copies match source**

Run: `for f in /d/quantum-worldline/agents/*.md; do name=$(basename "$f"); diff "$f" ~/.claude/agents/"$name" > /dev/null 2>&1 && echo "OK: $name" || echo "DIFF: $name"; done`

If any show DIFF, inspect before replacing — the copy may have been edited directly.

- [ ] **Step 2: Remove copies and create symlinks**

```bash
for f in /d/quantum-worldline/agents/*.md; do
  name=$(basename "$f")
  rm -f ~/.claude/agents/"$name"
  ln -sf "$f" ~/.claude/agents/"$name"
done
```

- [ ] **Step 3: Verify symlinks resolve correctly**

Run: `ls -la ~/.claude/agents/ | grep quantum-worldline`
Expected: 14 symlinks pointing to `/d/quantum-worldline/agents/*.md`

Run: `head -2 ~/.claude/agents/physics-scanner.md`
Expected: `---` followed by `name: physics-scanner`

- [ ] **Step 4: Commit**

```bash
# Nothing to commit — symlinks are in ~/.claude/ which is outside the repo.
# But update MEMORY.md to reflect the change.
```

Update `MEMORY.md`: change "Agents are copies not symlinks" to "Agents are symlinked from `~/.claude/agents/` -> `D:/quantum-worldline/agents/`"

---

### Task 2: Add MCP Paper-Search Tools to Agent Instructions

**Problem:** Subagents (physics-scanner, literature-lead, math-bridge, hardware-tracker) use `WebSearch`/`WebFetch` for paper discovery. They don't know about the `mcp__paper-search__search_arxiv`, `mcp__paper-search__search_google_scholar`, etc. tools now available. MCP tools ARE propagated to subagents (they inherit the parent's tool set), but agents need to be told to use them.

**Files:**
- Modify: `D:/quantum-worldline/agents/physics-scanner.md` (SEARCH TOOLS section)
- Modify: `D:/quantum-worldline/agents/literature-lead.md` (add tool awareness)
- Modify: `D:/quantum-worldline/agents/math-bridge.md` (add tool awareness)
- Modify: `D:/quantum-worldline/agents/hardware-tracker.md` (add tool awareness)

- [ ] **Step 1: Update physics-scanner.md SEARCH TOOLS section**

Replace the SEARCH TOOLS section with:

```markdown
SEARCH TOOLS (use in this priority order)
- Use mcp__paper-search__search_google_scholar for topic-based discovery (best relevance ranking)
- Use mcp__paper-search__search_arxiv for recent papers and arXiv ID lookups
- Use mcp__paper-search__read_arxiv_paper to read full paper content by arXiv ID
- Use mcp__paper-search__download_arxiv to download papers locally
- Use mcp__paper-search__search_pubmed for biomedical/biological quantum papers
- Use WebSearch as fallback for news, blog posts, non-academic sources
- Use WebFetch for specific URLs (paper pages, blog posts)
- Use HuggingFace tools to search HF papers and datasets
```

- [ ] **Step 2: Update literature-lead.md — add MCP tool note**

After "YOUR SPECIALISTS" section, add:

```markdown
MCP TOOLS AVAILABLE
Your specialists have access to paper-search MCP tools:
- mcp__paper-search__search_google_scholar (best for topic discovery)
- mcp__paper-search__search_arxiv (best for recent papers, ID lookups)
- mcp__paper-search__read_arxiv_paper (read full paper by arXiv ID)
- mcp__paper-search__download_arxiv (download paper locally)
- mcp__paper-search__search_pubmed (biomedical papers)
Instruct specialists to prefer these over WebSearch for academic papers.
```

- [ ] **Step 3: Update math-bridge.md — add MCP tool note**

Add after the existing tool instructions:

```markdown
PAPER SEARCH TOOLS
- Use mcp__paper-search__search_google_scholar for finding mathematical connections in literature
- Use mcp__paper-search__search_arxiv for specific arXiv papers
- Use mcp__paper-search__read_arxiv_paper to read full papers when found
```

- [ ] **Step 4: Update hardware-tracker.md — add MCP tool note**

Add after existing tool instructions:

```markdown
PAPER SEARCH TOOLS
- Use mcp__paper-search__search_google_scholar for hardware research papers
- Use mcp__paper-search__search_arxiv for recent hardware announcements with papers
```

- [ ] **Step 5: Verify symlinks propagated changes**

Run: `grep "paper-search" ~/.claude/agents/physics-scanner.md`
Expected: shows the new MCP tool references (because it's a symlink now)

- [ ] **Step 6: Commit**

```bash
cd /d/quantum-worldline
git add agents/physics-scanner.md agents/literature-lead.md agents/math-bridge.md agents/hardware-tracker.md
git commit -m "feat: add paper-search MCP tools to research agents"
```

---

### Task 3: Verify MCP Tool Propagation to Subagents

**Problem:** Unknown whether subagents dispatched via the Agent tool inherit MCP tools from the parent context. Need to test empirically.

- [ ] **Step 1: Dispatch a minimal test agent**

Launch a general-purpose agent with prompt:
"List all tools available to you that contain 'paper' or 'arxiv' in their name. Then call mcp__paper-search__search_arxiv with query 'quantum error correction' and max_results 1. Return the result."

- [ ] **Step 2: Evaluate result**

If the agent can see and call the MCP tools: CONFIRMED. No further action.
If the agent cannot see them: MCP tools do NOT propagate. Agents must fall back to WebSearch. Update agent instructions to note this limitation. Update MEMORY.md.

- [ ] **Step 3: Update MEMORY.md with finding**

Add under Infrastructure section:
```
- **MCP tool propagation**: [CONFIRMED/NOT SUPPORTED] — subagents [can/cannot] access paper-search MCP tools
```

---

## Chunk 2: Semantic Scholar API Key

### Task 4: Configure Semantic Scholar API Key

**Problem:** paper-search-mcp supports optional Semantic Scholar API key for enhanced features (citation graphs, related papers, higher rate limits). Currently running without it.

**Files:**
- Modify: `D:/quantum-worldline/.mcp.json` (add env var)

- [ ] **Step 1: Check if user already has a Semantic Scholar API key**

Ask user: "Do you have a Semantic Scholar API key? If not, you can get a free one at https://www.semanticscholar.org/product/api#api-key-form"

- [ ] **Step 2: Add key to .mcp.json**

Once user provides key, update `.mcp.json`:

```json
{
  "mcpServers": {
    "paper-search": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "D:/quantum-worldline/.mcp-servers/paper-search",
        "-m",
        "paper_search_mcp.server"
      ],
      "env": {
        "SEMANTIC_SCHOLAR_API_KEY": "<USER_KEY_HERE>"
      }
    }
  }
}
```

- [ ] **Step 3: Test Semantic Scholar search**

Restart session, then run:
`mcp__paper-search__search_semantic_scholar` with query "MERA tensor network holographic"

Expected: returns papers with citation counts and related paper links.

- [ ] **Step 4: Update MEMORY.md**

Change "No API keys required (Semantic Scholar key optional)" to note key is configured.

---

## Chunk 3: HuggingFace Dataset Push

### Task 5: Wire Up HuggingFace Dataset Push

**Problem:** Design spec calls for paper metadata and hypothesis records to push to a HuggingFace dataset automatically. Never tested.

**Files:**
- Verify: HF CLI authentication (`huggingface-cli whoami`)
- Create: HF dataset repo (if needed)
- Modify: `D:/quantum-worldline/agents/synthesis-agent.md` (add HF push step)
- Modify: `D:/quantum-worldline/agents/worldline-orchestrator.md` (add HF push after digest)

- [ ] **Step 1: Check HF CLI authentication**

Run: `huggingface-cli whoami`
Expected: shows authenticated user. If not, run `huggingface-cli login`.

- [ ] **Step 2: Check if HF dataset repo exists**

Run: `huggingface-cli repo info --repo-type dataset jonca/quantum-worldline-research 2>&1 || echo "NOT FOUND"`

If NOT FOUND, create it:
Run: `huggingface-cli repo create quantum-worldline-research --type dataset`

- [ ] **Step 3: Test manual push of existing data**

```bash
cd /d/quantum-worldline
huggingface-cli upload jonca/quantum-worldline-research research/data/papers/ papers/ --repo-type dataset
```

Expected: uploads paper JSON files to HF dataset.

- [ ] **Step 4: Add HF push instruction to synthesis-agent.md**

Add to the OUTPUT section:

```markdown
HUGGINGFACE PUSH
After producing a digest, push updated data to HuggingFace:
- Use the hugging-face-cli skill or Bash to run:
  `huggingface-cli upload jonca/quantum-worldline-research research/data/ data/ --repo-type dataset`
- This pushes papers, hypotheses, simulations, and hardware records.
- Only push after a complete scan, not after individual paper additions.
```

- [ ] **Step 5: Add HF push step to worldline-orchestrator.md**

Add after the "merge and summarize" section:

```markdown
DATASET PUSH
After producing the final digest, push research data to HuggingFace:
- Run: `huggingface-cli upload jonca/quantum-worldline-research research/data/ data/ --repo-type dataset`
- Report push status in the summary.
```

- [ ] **Step 6: Commit**

```bash
cd /d/quantum-worldline
git add agents/synthesis-agent.md agents/worldline-orchestrator.md
git commit -m "feat: add HuggingFace dataset push to research pipeline"
```

---

## Chunk 4: End-to-End Skill Verification

### Task 6: Test All Custom Skills

**Problem:** 5 custom skills exist but haven't been tested end-to-end since installation.

**Skills to test:**
1. `/qw-scan` (weekly-scan) — full literature + hardware sweep
2. `/qw-query` (research-query) — route question through orchestrator
3. `/qw-hardware` (hardware-status) — hardware frontier snapshot
4. `/qw-hypotheses` (hypothesis-review) — list active hypotheses
5. `/qw-simulate` (simulate) — circuit design + classical baseline

- [ ] **Step 1: Test /qw-hardware**

This is the simplest skill — should just produce a snapshot. Run it and verify it returns structured hardware data.

Expected: table of current best numbers for qubits, error rates, coherence times.

- [ ] **Step 2: Test /qw-hypotheses**

Should list HYP-2026-001 through HYP-2026-007 with status and confidence.

Expected: table of hypotheses with status (ACTIVE, TESTING, etc.)

- [ ] **Step 3: Test /qw-query with a simple question**

Run: `/qw-query "What is the current status of holographic force measurements on MERA circuits?"`

Expected: orchestrator dispatches appropriate tier lead, returns structured answer.

- [ ] **Step 4: Test /qw-scan (abbreviated)**

Run: `/qw-scan` — this dispatches the full research team. Monitor for errors.

Expected: Literature Lead dispatches specialists, produces digest, saves to research/digests/.

Note: This is the most complex skill. If earlier tasks fixed MCP tool access, the agents should now use paper-search tools.

- [ ] **Step 5: Test /qw-simulate (dry run)**

Run: `/qw-simulate "Design a 4-qubit GHZ state circuit and simulate it"`

Expected: Computation Lead dispatches Qiskit Builder, gets circuit + simulation results.

- [ ] **Step 6: Document results**

Update MEMORY.md with which skills work and any issues found. Log any that need fixes.

---

## Summary of Changes

| Gap | Fix | Effort |
|-----|-----|--------|
| Agent copies vs symlinks | Replace copies with symlinks | 2 min |
| MCP tools in agents | Update 4 agent .md files with tool references | 5 min |
| MCP tool propagation | Empirical test with subagent | 2 min |
| Semantic Scholar API key | User provides key, add to .mcp.json | 2 min |
| HuggingFace dataset push | Test HF CLI, add push instructions to 2 agents | 10 min |
| End-to-end skill tests | Run all 5 skills, document results | 15 min |

**Total estimated effort:** ~35 min of implementation, spread across independent tasks.

**Dependencies:**
- Task 1 (symlinks) should complete before Task 2 (agent edits) so edits propagate automatically
- Task 3 (MCP propagation test) should run after Task 2
- Task 4 (Semantic Scholar) requires user input (API key)
- Task 5 (HF push) requires HF authentication check
- Task 6 (skill tests) should run last, after all other fixes
