#!/bin/bash
# usage: run.sh <id> <variant> <skill> <search:0|1>
X=$(dirname "$0"); C="$CASES"
id=$1; v=$2; sk=$3; se=$4
task=$(cat "$C/$sk.md")
prompt="先完整阅读 \`skills/$sk/SKILL.md\`，并按它的指引阅读它指向的文件，然后按该 skill 完成下面的任务。

任务：
$task"
flag=""; [ "$se" = 1 ] && flag="--search"
timeout 1500 codex $flag exec -m gpt-6.1-terra -c model_reasoning_effort="medium" -s read-only --skip-git-repo-check --json -C "$X/snap/$v" -o "$X/out/$id.md" "$prompt" > "$X/out/$id.jsonl" 2> "$X/out/$id.err" < /dev/null
echo "$id exit=$?" >> "$X/out/status.txt"
