# 教材設計ロールプレイ プロンプトテンプレート

> 用途: camel の RolePlaying に渡すプロンプトの再利用テンプレート集
> 使い方: `<　>` の部分を自分の状況に合わせて書き換えてから使う

---

## 1. タスクプロンプト（task_prompt）

```
<対象者（例: 非エンジニアの営業職）>向けに、
<テーマ（例: 生成AIツールの業務活用）>を学ぶための
<形式（例: 半日研修 / eラーニング3モジュール / ワークショップ）>の教材を設計する。
```

**記入例**
```
新任マネージャー向けに、
1on1面談の進め方を学ぶための
90分ワークショップの教材を設計する。
```

---

## 2. ロール設定（role pair）

教材設計でよく使うロールの組み合わせ:

| assistant_role_name（専門家側） | user_role_name（依頼者側） |
|--------------------------------|--------------------------|
| インストラクショナルデザイナー | 人材育成担当者 |
| ファシリテーター | 研修企画者 |
| eラーニング設計者 | HR マネージャー |
| 教育コンサルタント | 事業部長 |
| 学習設計アドバイザー | 新任トレーナー |

---

## 3. システムプロンプト（camelのassistant_prompt.txtの教材設計版）

```
Never forget you are a <ASSISTANT_ROLE> and I am a <USER_ROLE>.
Never flip roles! Never instruct me!
We share a common interest in collaborating to design effective learning materials.

You must help me design educational content that meets the following criteria:
- Learner-centered: focuses on what participants can DO after learning
- Practical: includes exercises, examples, and real-world applications
- Structured: follows a logical flow (Introduction → Content → Practice → Summary)

Here is the task: <TASK>. Never forget our task!

I must instruct you based on my organizational needs and your expertise.
I must give you one instruction at a time.
You must provide a specific, actionable proposal that completes each instruction.
Always explain your reasoning so I can learn from your design choices.

Unless I say the task is completed, always start with:
Proposal: <YOUR_PROPOSAL>

<YOUR_PROPOSAL> must be concrete and include examples where applicable.
Always end with: Next request.
```

---

## 4. タスク自動生成プロンプト（generate_tasks版）

```
List <NUM_TASKS> diverse subtasks that <ASSISTANT_ROLE> can help
<USER_ROLE> complete cooperatively to design effective learning materials.
Focus on: needs analysis, learning objectives, content structure,
engagement activities, and evaluation methods.
Be concise and practical.
```

**記入例（5タスク版）**
```
List 5 diverse subtasks that an Instructional Designer can help
an HR Manager complete cooperatively to design effective learning materials.
Focus on: needs analysis, learning objectives, content structure,
engagement activities, and evaluation methods.
Be concise and practical.
```

---

## 5. Claudeに直接使う教材設計プロンプト（camelなし版）

camelを使わず、Claudeと直接教材設計を進める場合のテンプレート:

### 探索フェーズ（ニーズ分析）
```
以下の研修について、教材設計を始める前に情報を整理してください。

【対象者】<例: 入社1〜3年目の営業職、約20名>
【テーマ】<例: 提案書の作り方>
【形式】<例: 半日集合研修>
【背景・課題】<例: 提案書の品質にばらつきがある>

整理してほしい観点:
1. 想定される受講者の現状スキルと課題
2. 研修終了後に「できるようになること」の候補（学習目標案）
3. 教材に含めるべきコンテンツの候補
4. リスクや設計上の注意点

まだ教材の中身は作らないでください。
```

### 計画フェーズ（教材構成案）
```
以下の条件で教材構成案を作成してください。

【対象者】<　>
【学習目標】<　>
【時間・形式】<　>

各セクションについて以下を明記してください:
- セクション名と所要時間
- 学習活動の種類（講義 / 演習 / ディスカッション / ケーススタディ）
- 達成目標（このセクションで何ができるようになるか）

まだ各セクションの詳細は作らないでください。
```

### 実行フェーズ（セクション詳細化）
```
構成案の「<セクション名>」だけを詳細化してください。
以下を含めてください:
- 進行スクリプト（ファシリテーターが話す内容の骨子）
- 演習・ワークの具体的な手順
- 参加者に配布するワークシートの案

詳細化後、変更点・理由・確認方法・次のセクション候補を要約してください。
```

---

*最終更新: 2026-03-28*
*参照元: camel/prompts/ai_society/ のテンプレート構造をベースに教材設計向けに改変*
