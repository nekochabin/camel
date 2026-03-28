#!/usr/bin/env bash
# Hook: Stop — セッション終了時に日次ログへサマリを追記する
# 保存先: ~/.claude/logs/YYYY-MM-DD.md

LOG_DIR="${HOME}/.claude/logs"
mkdir -p "$LOG_DIR"

DATE=$(date +"%Y-%m-%d")
TIME=$(date +"%H:%M")
LOG_FILE="${LOG_DIR}/${DATE}.md"

# ヘッダーがなければ初期化
if [ ! -f "$LOG_FILE" ]; then
  cat > "$LOG_FILE" << EOF
# 作業ログ: ${DATE}

## セッション一覧
EOF
fi

# セッション区切りを追記
cat >> "$LOG_FILE" << EOF

---
### セッション終了: ${TIME}

**作業ディレクトリ**: $(pwd)
**Gitブランチ**: $(git branch --show-current 2>/dev/null || echo "（Gitなし）")
**変更ファイル数**: $(git diff --name-only HEAD 2>/dev/null | wc -l | tr -d ' ')件

> 次回再開時のメモ: （ここに手動で記入）

EOF

echo "ログを保存しました: $LOG_FILE"
exit 0
