"""
教材設計ロールプレイサンプル

「インストラクショナルデザイナー（AI Assistant）」と
「研修担当者（AI User）」が対話しながら教材を設計するシナリオ。

使い方:
    export OPENAI_API_KEY=<your key>
    python examples/training_design.py

カスタマイズポイント:
    - task_prompt: 設計したい教材テーマを変える
    - assistant_role_name: 専門家の役割（例: 「eラーニング設計者」「ファシリテーター」）
    - user_role_name: 依頼者の役割（例: 「新任マネージャー」「HR担当者」）
    - chat_turn_limit: 対話ターン数（デフォルト10、長くするほど詳細化される）
"""

from colorama import Fore

from camel.agents import RolePlaying
from camel.utils import print_text_animated


def main() -> None:
    # --- カスタマイズポイント ---
    task_prompt = (
        "生成AIツールを業務に活用するための、"
        "非エンジニア向け半日研修の教材を設計する"
    )
    assistant_role_name = "インストラクショナルデザイナー"
    user_role_name = "人材育成担当者"
    chat_turn_limit = 10  # 短めに設定（探索・計画フェーズの練習用）
    # --------------------------

    role_play_session = RolePlaying(
        assistant_role_name,
        user_role_name,
        task_prompt=task_prompt,
        with_task_specify=True,   # タスクを自動で具体化する
        with_task_planner=False,  # ステップ分解は今回オフ
    )

    print(Fore.GREEN +
          f"AI Assistant（{assistant_role_name}）のシステムメッセージ:\n"
          f"{role_play_session.assistant_sys_msg}\n")
    print(Fore.BLUE +
          f"AI User（{user_role_name}）のシステムメッセージ:\n"
          f"{role_play_session.user_sys_msg}\n")
    print(Fore.YELLOW + f"元のタスク:\n{task_prompt}\n")
    print(Fore.CYAN +
          f"具体化されたタスク:\n{role_play_session.specified_task_prompt}\n")
    print(Fore.RED + f"最終タスク:\n{role_play_session.task_prompt}\n")

    n = 0
    assistant_msg, _ = role_play_session.init_chat()
    while n < chat_turn_limit:
        n += 1
        assistant_return, user_return = role_play_session.step(assistant_msg)
        assistant_msg, assistant_terminated, assistant_info = assistant_return
        user_msg, user_terminated, user_info = user_return

        if assistant_terminated:
            print(Fore.GREEN +
                  f"Assistantが終了しました。理由: "
                  f"{assistant_info['termination_reasons']}")
            break
        if user_terminated:
            print(Fore.GREEN +
                  f"Userが終了しました。理由: "
                  f"{user_info['termination_reasons']}")
            break

        print_text_animated(
            Fore.BLUE + f"【{user_role_name}】\n\n{user_msg.content}\n")
        print_text_animated(
            Fore.GREEN + f"【{assistant_role_name}】\n\n{assistant_msg.content}\n")

        if "CAMEL_TASK_DONE" in user_msg.content:
            print(Fore.GREEN + "タスク完了。")
            break


if __name__ == "__main__":
    main()
