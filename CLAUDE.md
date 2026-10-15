# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Quantum Worldline is a plugin-format repo (`.claude-plugin/plugin.json`) containing a multi-tier agent team for quantum physics and worldline simulation research. It is NOT installed through the plugin manager: agents deploy by copy (`scripts/sync-agents.sh` -> `~/.claude/agents/`) and skills by symlink into `~/.claude/skills/`. Because the plugin is not installed, `hooks/hooks.json` (the research/data ID-format check) never loads and is currently inert. The team automates the research cycle: **discover → hypothesize → gate → test → interpret**.

## Architecture

**Tiered orchestration with subagent delegation:**
- **Worldline Orchestrator** — single user entry point, dispatches tier leads
- **Tier 1 (Literature)** — Literature Lead → Physics Scanner, Hardware Tracker, Math Bridge, Synthesis Agent
- **Tier 2 (Computation)** — Computation Lead → Qiskit Builder, Classical Simulator, Visualization Agent
- **Tier 3 (Theory)** — Theory Lead → Conjecture Generator, Feasibility Checker, Philosophy Agent

Tier leads dispatch their specialists via the Agent tool. Specialists return structured JSON to their lead. The orchestrator aggregates across tiers.

## Governing Scientific Standard (adopted 2026-08-11)

**`docs/governance/RESEARCH-DIRECTOR.md` is the standard all research work is held to.** Read it
before proposing, running, or writing up any result. It supersedes informal practice on:
- **Claim levels (§5)**: every result is Level 1 (validation) / 2 (method) / 3 (new physics in
  framework) / 4 (discriminating). Never present Level 1 as Level 4.
- **Counterfactual novelty (§6)**: before running anything, record how many outcomes were genuinely
  possible. If conformal symmetry fixes the answer, that is near-zero novelty — say so.
- **Independence ledger (§7)**: agreements between quantities derived from the same inputs are
  consistency checks, not evidence. Classify every cross-check.
- **Novelty gates (§8)**: no result is called novel until literature + derivation + prior-art gates
  are recorded. Banned without evidence: "to our knowledge", "novel", "first", "unprecedented".
- **Killer tests (§12)**: every hypothesis needs a named outcome that would kill it, documented
  BEFORE results are interpreted.
- **Matched controls (§19)** and **out-of-sample prediction (§18)** on every major numerical claim.
- **The trunk question (§29)**: what operational content, if any, does emergent geometry add beyond
  an accurate CFT tensor-network representation? Work should orbit this.

Audit artifacts live in `research/data/audit/`; the standing audit is
`docs/governance/AUDIT-2026-08-11.md`.

## External Status Must Be Freshly Checked (added 2026-08-23, after a real miss)

**Never report the status of anything outside this repo from an internal note. Check the source.**

On **2026-08-17** the project discovered that PRD had rejected accession DV13971 on **2026-08-12** -- 5
days earlier. (Date corrected 2026-10-15 from the commit history: commit 0bdb172 recorded the discovery on 2026-08-17, five days late; this section was written on 2026-08-23 and originally said 08-23 and 11 days.) Three internal records (`TASKS.md`, memory `paper_status.md`, `RESEARCH-LOG.md:1031`)
all confidently said "With editors". All three were written by the same process on the same day from
a single lookup. They agreed with each other and with nothing external. A withdrawal letter was
drafted and nearly sent to an editor who had already closed the file.

This is the **independence failure of RESEARCH-DIRECTOR.md §7** -- agreement among same-origin
sources is a consistency check, not evidence -- occurring in operational records rather than in
physics. The 23-agent audit that caught the physics instance walked straight past this one.

**The rule:**
- Any claim about a journal decision, an email reply, a portal state, a service status, or a remote
  job **must be re-verified against the external source in the same session it is reported.**
- Internal records *restate* an external status; they never *refresh* it. Three agreeing notes and
  zero lookups is zero lookups.
- When quoting a status from a note, say when it was last actually checked. If that is unknown or
  stale, check it or label it explicitly as unverified.
- **Do not rely on a session cron for this.** `CronCreate` jobs are session-only and expire in 7
  days; an expired reply-watcher is what caused this miss in the first place. The durable mechanism
  is this rule plus the session-start read of `NEXT-SESSION.md`.

**Session-start habit:** if anything is outstanding with an external party (submission, reply,
approval, remote run), check that source before reporting on it -- for email, `email_search` on
joncackler@gmail.com, which is where all paper correspondence lives.

## Key Paths

- Agents: `agents/*.md` — CANONICAL SOURCE, but NOT what the runtime loads. Claude Code loads the deployed copies in `~/.claude/agents/`; after editing any agent here, run `scripts/sync-agents.sh` or the edit silently never takes effect. (All 14 copies verified byte-identical 2026-07-06.)
- Skills: `skills/<name>/SKILL.md` — symlinked into `~/.claude/skills/`, so skill edits take effect immediately (no sync step)
- Structured output: `research/data/{papers,hardware,simulations,hypotheses,builds,theory}/`
- Weekly digests: `research/digests/`
- Chronological narrative: `research/RESEARCH-LOG.md` (unlimited; the memory index only points)
- Known errors / corrections: `research/ERRATA.md` (check before quoting published numbers)
- JSON schemas: `templates/*.json`
- Design spec: `docs/specs/2026-03-10-quantum-worldline-design.md`

## Agent Conventions

- All agents use markdown frontmatter: `name`, `description` (with examples), `model`, `memory: user`, `color`
- Tier leads use `sonnet`, creative/precision specialists use `opus`
- All structured output goes to `research/data/` as JSON matching schemas in `templates/`
- Agents return structured JSON to their lead, not free-form text
- Status verdicts: `NOVEL`, `CONFIRMED`, `CONTRADICTS`, `ACTIONABLE`, `WATCH`
- Subagent rules: leads dispatch specialists, specialists never dispatch other agents

## Data Flow

```
User → Orchestrator → Tier Lead(s) → Specialist(s)
     → Structured JSON (research/data/)
     → Tier Lead aggregates → Orchestrator merges
     → Summary to user + markdown digest + HF dataset push
```

## Skills

| Skill | Purpose |
|---|---|
| `/weekly-scan` | Full literature + hardware sweep (weekly or on-demand) |
| `/research-query` | Route question through orchestrator |
| `/hardware-status` | Hardware frontier snapshot |
| `/hypothesis-review` | List active hypotheses |
| `/simulate` | Circuit design + classical baseline + compare |
| `/worldline-orchestrator` | Dispatch-mode chooser: agent team of 3 tier leads for full ops, or a single specialist subagent for quick queries |

## MCP Servers

- **paper-search**: arXiv/PubMed/bioRxiv search + download (`.mcp.json`). **WARNING (2026-06-08): its search endpoints are QUERY-BLIND** — they return the latest-submission firehose regardless of keywords. For topical search use the arXiv export API via WebFetch (`http://export.arxiv.org/api/query?search_query=abs:...&sortBy=submittedDate&sortOrder=descending`); use MCP read/download only for known paper IDs, fail-fast.
  - **SEQUENTIAL, NEVER PARALLEL (2026-07-21, scan #17).** The arXiv export API serializes and burst-blocks: firing theme-cluster queries from parallel agents trips HTTP 429 and **silently drops query lines**, which reads downstream as a falsely "empty" window. Space queries ~3-5s apart and check each cluster's newest-submission date against the window. Scan #18 confirmed the fix (zero dropped lines).
  - Avoid multi-way `OR` queries with 4+ phrases — one such re-run returned semantically unrelated results (magnon/polariton/ARPES). Prefer clean single- or two-phrase queries.
- **HuggingFace**: Already available via installed plugin
- **email-mcp**: draft ids (`r...`) are a different id-space from message ids — drafts cannot be sent or deleted via the API; send fresh with email_send/email_reply and discard stale drafts in the Gmail UI.

## Simulation Tooling (MERAKit)

- `research/tools/MERAKit.jl/` is GITIGNORED (vendored package). After editing any `qw_*.jl` driver there, copy it to `research/tools/merakit-setup/` (the tracked mirror) before committing.
- Run env: `research/tools/merakit-setup/RUN-MERAKIT.md` (Julia 1.8 via `+1.8`, clean HOME, `OPENBLAS_NUM_THREADS=1`). Launch from inside the MERAKit.jl dir — Bash cwd DRIFTS between tool calls; put an explicit `cd` in the same command as the `julia` invocation.
- RunPod CPU pods: `ubuntu:22.04` + `computeType:"CPU"` + `env:{PUBLIC_KEY:...}` + sshd dockerStartCmd; plain images do NOT auto-inject account keys. Use `~/.ssh/runpod_ed25519` (the default `~/.ssh/id_*` keys are ACL-locked — unreadable from Bash AND PowerShell). On the pod: `Pkg.instantiate()` against the shipped Manifest.toml — do NOT run setup.jl (it deletes the known-good Manifest, then resolve fails on a fresh registry).

## Zenodo

- API token (deposit scopes): `C:\Users\jonca\.zenodo-token`. The records belong to the joncackler@gmail.com Zenodo account (ORCID login); the GitHub-SSO Zenodo account owns NOTHING.
- Record GET output is NOT PUT-safe: round-tripping silently strips resource_type/creators/rights/subjects/publisher/related_identifiers — rebuild those in canonical id-shape. Cookie-auth API writes need the `X-CSRFToken` header. Details: memory [zenodo-doi].

## Catalogue Rules

- **Dedup before assigning IDs**: `grep -l "<arxiv-id>" research/data/papers/*.json` first — scan-9 re-catalogued two papers that already had records. Duplicate records become alias stubs (`alias_of` field), never silent deletions.
- Verify ID high-water marks on disk before any scan; memory counters drift.

## Development Rules

- When adding a new agent, follow the existing frontmatter pattern in any `agents/*.md` file, then run `scripts/sync-agents.sh` to deploy it to `~/.claude/agents/` (required for it to load)
- New agents must specify which tier they belong to and who their lead is
- All hypothesis output must pass through the Feasibility Checker before being reported
- Structured data files in `research/data/` must validate against `templates/` schemas
- The Qiskit Builder never submits to real IBM hardware without explicit user approval
