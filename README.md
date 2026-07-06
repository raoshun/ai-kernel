# AI Kernel

An autonomous AI agent development framework with policy-based execution, capability management, and audit logging.

> **⚠️ 現在のステータス**: このプロジェクトはMVP（Minimum Viable Product）です。現在の executor はPythonコードを直接実行します。AIによる自動コード生成機能を実装するには、OllamaなどのLLM統合が必要です。

## 概要

このプロジェクトは、自律AIエージェントを使って開発を行うためのフレームワークです。タスクを定義すると、AIエージェントがそのタスクを実行します。

## インストール

```bash
# 方法1: pipでインストール
pip install -e .

# 方法2: 直接Pythonモジュールとして実行
python -m ai_kernel run "your task here"
```

## 基本的な使い方

### CLIを使ってタスクを実行

```bash
# 方法1: ai-kernel コマンド（pip install -e . 後）
python -m ai_kernel run "print('Hello, World!')"

# 方法2: Pythonモジュールとして直接実行
python -m ai_kernel run "print('Hello, World!')"

# 計算タスク
python -m ai_kernel run "result = 2 + 3"
```

### プログラムから使う

```python
from ai_kernel.kernel.core import Kernel
from ai_kernel.model.task import Task
from ai_kernel.executor.runner import ExecutorRegistry

# カーネルを初期化
kernel = Kernel()
executor_registry = ExecutorRegistry()

# タスクを作成
task = Task(objective='print("Hello from AI Agent!")')

# 実行をリクエスト
execution = kernel.submit_execution(task)

if execution:
    # 実行
    executor_registry.execute("basic", execution, kernel)
    print(execution.result)
```

---

## AIエージェントに開発を依頼する方法

このフレームワークのメインの使い方は、AIエージェントに具体的なタスクを与えて自律的に開発させることです。

### ステップ1: 開発したいものの要件を準備する

まず作りたいものの要件を文章で書きます。例えば「おしゃれなブロック崩しゲーム」を作りたい場合:

```markdown
## おしゃれなブロック崩しゲームの要件

### 概要
- レトロフューチャでおしゃれなデザインのブロック崩しゲーム
- Python + Pygameで実装

### 視覚効果
- ネオンカラーのブロック（ピンク、シアン、ライムグリーン）
- グロー効果（glow effect）付きのパドルとボール
- 背景は深い宇宙のような深い青から紫のグラデーション
- ブロックが破壊されるときのパーティクル効果

### ゲームプレイ
- パドルはマウスで操作
- ボールは物理ベースの自然な動き
- 3つのライフポイント
- スコアシステム

### サウンド
- ブロック衝突時の効果音
- ゲームオーバー時のサウンド
```

### ステップ2: 要件をエージェントに指示して実行

CLIを使ってAIエージェントにタスクを渡します:

```bash
# ブロック崩しゲームを作成させる
python -m ai_kernel run "Create a stylish block breaker game using Python and Pygame with neon colors, glow effects, particle effects on block destruction, and a space-themed background. Include score system and 3 lives."
```

または、より詳細に:

```bash
python -m ai_kernel run "次の要件に従って、PythonとPygameでおしゃれなブロック崩しゲームを作成してください:
- ネオンカラー（ピンク、シアン、ライムグリーン）のブロック
- グロー効果付きのパドルとボール
- 深い青から紫のグラデーション背景
- ブロック破壊時のパーティクル効果
- マウスでパドルを操作
- 3つのライフ、スコアシステム
"
```

### ステップ3: エージェントが生成したファイルを確認

エージェントがタスクを実行すると、ソースファイルが作成されます。生成されたファイルを確認:

```bash
# 作成されたファイルを確認
ls -la *.py

# または特定のファイルを編集
```

### ステップ4: ゲームを起動してテスト

```bash
python main.py
```

---

## その他の例

### 例1: シンプルな電卓

```bash
python -m ai_kernel run "Create a calculator that can add, subtract, multiply and divide two numbers"
```

### 例2: ファイル整理スクリプト

```bash
python -m ai_kernel run "Create a Python script that organizes files in a folder by their extension"
```

### 例3: Webスクレイパー

```bash
python -m ai_kernel run "Create a web scraper that extracts article titles from a given URL"
```

---

## Architecture

```
┌─────────────────────────────────────┐
│           CLI / API                  │
├─────────────────────────────────────┤
│          Kernel Core                │
│  ┌─────────┐  ┌──────────────┐     │
│  │ Policy  │  │ Capability   │     │
│  │ Engine  │  │ Manager      │     │
│  └─────────┘  └──────────────┘     │
│  ┌─────────┐  ┌──────────────┐     │
│  │ Risk    │  │ Audit        │     │
│  │ Assessor│  │ Logger       │     │
│  └─────────┘  └──────────────┘     │
├─────────────────────────────────────┤
│       Executor Registry             │
│  - Basic Executor                   │
│  - Shell Executor                   │
│  - Python Executor                  │
└─────────────────────────────────────┘
```

## Policy System

タスクの実行にはポリシーエンジンがチェックを行います:
- 許可された操作かどうか
- リスク評価
- キャパビリティの確認

許可された場合のみ実行されます。

## Audit Logs

すべての実行は監査ログに記録されます:

```python
logs = kernel.get_audit_logs()
for log in logs:
    print(f"{log.action}: {log.description}")
```

---

## License

MIT