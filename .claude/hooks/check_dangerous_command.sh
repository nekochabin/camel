#!/usr/bin/env bash
# Hook: PreToolUse (Bash) — 危険なコマンドを実行前に検出して警告する
# 終了コード 2 を返すと Claude はそのコマンドをブロックする

TOOL_INPUT="$1"

# 検出対象パターン（危険度: 高）
DANGEROUS_PATTERNS=(
  "rm -rf"
  "rm -r /"
  "git reset --hard"
  "git push --force"
  "git push -f"
  "DROP TABLE"
  "DROP DATABASE"
  "truncate"
  "> /dev/sd"
  "dd if="
  "chmod -R 777"
  "sudo rm"
  ":(){ :|:& };:"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$TOOL_INPUT" | grep -qi "$pattern"; then
    echo "⚠️  危険なコマンドが検出されました: \"$pattern\"" >&2
    echo "このコマンドを実行するには、明示的な承認が必要です。" >&2
    echo "意図的に実行したい場合は、その旨を指示してください。" >&2
    exit 2  # Claude Code にブロックを伝える
  fi
done

exit 0
