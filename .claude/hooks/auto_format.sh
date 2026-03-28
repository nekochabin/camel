#!/usr/bin/env bash
# Hook: PostToolUse (Edit/Write) — ファイル編集後に自動フォーマットを実行する
# 対応: Python (black/ruff), Markdown (prettier), JSON (jq)

FILE_PATHS="$1"

# ファイルパスが空の場合は何もしない
if [ -z "$FILE_PATHS" ]; then
  exit 0
fi

format_file() {
  local file="$1"

  # ファイルが存在しない場合はスキップ
  [ -f "$file" ] || return 0

  case "$file" in
    *.py)
      # ruff が使えれば ruff、なければ black を試みる
      if command -v ruff &>/dev/null; then
        ruff format --quiet "$file" 2>/dev/null
      elif command -v black &>/dev/null; then
        black --quiet "$file" 2>/dev/null
      fi
      ;;
    *.json)
      if command -v jq &>/dev/null; then
        tmp=$(mktemp)
        jq . "$file" > "$tmp" 2>/dev/null && mv "$tmp" "$file"
      fi
      ;;
    *.md)
      # prettier が使えれば実行（任意）
      if command -v prettier &>/dev/null; then
        prettier --write --parser markdown --log-level silent "$file" 2>/dev/null
      fi
      ;;
  esac
}

# スペース区切りで複数ファイルが渡される場合に対応
for f in $FILE_PATHS; do
  format_file "$f"
done

exit 0
