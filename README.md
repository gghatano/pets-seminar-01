# pets-seminar-01

仮名加工情報・匿名加工情報 事例再現デモプロジェクト

🌐 **公開サイト: <https://gghatano.github.io/pets-seminar-01/>**

個人情報保護委員会事務局が公開している仮名加工情報・匿名加工情報の事例レポートを一次情報として参照し、
掲載事例のデータ加工を Python で再現する **デモ・教材** です。
Jupyter Notebook は Google Colaboratory から実行できる形で提供します。

> 本プロジェクトの中心的な価値は加工コードそのものではなく、
> 「データを見て、利用目的を考え、情報特性を評価し、適切な加工方針を設計し、その結果を実装・確認する」
> という **データ加工設計の思考プロセス** を、具体的な事例を通じて理解できることに置きます。
> 実際の個人データに対する法令適合性を保証するものではありません。

詳細な設計・実装指示は [`docs/spec.md`](docs/spec.md) を正本とします。

## 事例

| 事例 | 種別 | ステータス | Notebook |
|------|------|-----------|----------|
| case01 | 仮名加工情報（オンライン通販の顧客・購買データ） | 実装済み | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gghatano/pets-seminar-01/blob/main/notebooks/case01_pseudonymized.ipynb) |
| case02 | 匿名加工情報 | 未着手（プレースホルダ） | — |

## 開発環境（uv）

依存関係の管理には [uv](https://docs.astral.sh/uv/) を使用します。

```bash
# 依存関係の同期（.venv を作成）
uv sync

# ダミーデータ生成（case01）
uv run python src/dummy_data/case01_pseudonymized.py

# テスト
uv run pytest

# Notebook 編集（ローカル）
uv run jupyter lab

# デモサイト（GitHub Pages 用）をローカルで確認
uv run mkdocs serve

# サイトをビルド（CI と同じ strict モード）
uv run mkdocs build --strict
```

必要環境: Python 3.11+ / uv

## ディレクトリ構成

```text
.
├── docs/                     # 設計成果物の正本（Notebook に全文複製しない）
│   ├── spec.md               # プロジェクト設計・実装指示書
│   ├── references/           # 参照した一次資料の整理
│   ├── case01_pseudonymized/ # 仮名加工情報 事例の設計8文書
│   └── case02_anonymized/    # 匿名加工情報 事例（プレースホルダ）
├── data/                     # 生成済みダミーデータ（Notebook が raw URL 等で取得）
├── notebooks/                # Google Colaboratory 用デモ Notebook
├── src/dummy_data/           # ダミーデータ生成スクリプト（seed 固定・再現可能）
├── tests/                    # ダミーデータ生成等の自動テスト
└── .claude/skills/           # 合成データ生成スキル（下記参照）
```

## 合成データ生成スキル

`.claude/skills/` に、[gghatano/mockdata-generator](https://github.com/gghatano/mockdata-generator)
の仕様駆動・合成データ生成パイプライン（`synthesize` PM + 5 ステップ）を取り込んでいます。
本プロジェクトのダミーデータ生成（`docs/*/02_dummy_data_spec.md` → `src/dummy_data/*.py` →
`data/*/raw/`）に活用します。適用方法は
[`.claude/skills/README.md`](.claude/skills/README.md) を参照してください。

## 配信・公開構成（3層）

デモは媒体を役割で分けて公開します（`docs/spec.md` 第25節）。

| 層 | 媒体 | 内容 |
|----|------|------|
| ① 検討 | GitHub Pages（HTML） | 事例理解・情報特性評価・**加工設計の決定** |
| ② 実装 | Google Colaboratory | 加工処理の**実行** |
| ③ 結果 | GitHub Pages（HTML） | 加工前後比較・**確認テスト結果**・加工後分析 |

- サイトは MkDocs + Material（`mkdocs.yml`）で `docs/` の Markdown から生成します。
- `main` への push で GitHub Actions（`.github/workflows/pages.yml`）が Pages へ自動デプロイします
  （公開先: <https://gghatano.github.io/pets-seminar-01/>）。

## 作業の進め方

`docs/spec.md` 第22節の実装順序に従います。設計成果物間に矛盾がある状態で Notebook 実装に進みません。
タスクは GitHub Issue で管理します。
