#!/usr/bin/env bash
# Hook: Notification — Claudeが入力待ちになったときに通知する
# トリガー: Notificationイベント（Claudeがユーザー入力を待つ状態）

# macOS の場合
if command -v osascript &>/dev/null; then
  osascript -e 'display notification "Claudeが入力を待っています" with title "Claude Code"'
  exit 0
fi

# Linux (notify-send) の場合
if command -v notify-send &>/dev/null; then
  notify-send "Claude Code" "Claudeが入力を待っています"
  exit 0
fi

# ターミナルベル（フォールバック）
echo -e "\a"
exit 0
