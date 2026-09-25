#!/bin/bash
# Sync quantum-worldline agents from source to ~/.claude/agents/
# Run after editing any agent .md file in D:/quantum-worldline/agents/
SRC="/d/quantum-worldline/agents"
DST="$HOME/.claude/agents"
count=0
for f in "$SRC"/*.md; do
  name=$(basename "$f")
  cp "$f" "$DST/$name"
  count=$((count + 1))
done
echo "Synced $count agents from $SRC -> $DST"
