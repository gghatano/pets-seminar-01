# 合成データ生成スキル（vendored）

このディレクトリのスキルは、[gghatano/mockdata-generator](https://github.com/gghatano/mockdata-generator)
の `.agents/skills/` を取り込んだものです（upstream commit `6099258`）。
本プロジェクトのダミーデータ生成（`docs/spec.md` 第8・15節）に活用します。

## スキル一覧

| スキル | 役割 |
|--------|------|
| `synthesize` | PM エージェント。以下5ステップを逐次サブエージェントに委譲し end-to-end で実行する。 |
| `0_input_prepare` | 原資料 → `input/`（table_definition / sample_data / data_spec.md / constraints.md）を整備 |
| `1_spec_ingest` | `input/` → `work/inferred_schema.json`, `work/constraint_plan.md` |
| `2_generation_plan` | → `work/generation_plan.md` |
| `3_generator_impl` | → `src/generator.py`, `output/*.csv` |
| `4_evaluate_and_refine` | → `output/evaluation_report.md`, `output/quality_gate.json` ほか |

## 本プロジェクトへの適用（マッピング）

upstream の想定は `examples/<task>/{source,input,work,src,output}` というタスク作業ディレクトリです。
本プロジェクトでは以下のように対応づけて使います。

`<case>` は事例ディレクトリ名（`case01_pseudonymized` / `case02_anonymized` / …）。

| upstream の成果物 | 本プロジェクトでの対応 |
|-------------------|------------------------|
| `input/table_definition*` | `docs/<case>/03_table_definition_before.md` |
| `input/data_spec.md` / `input/constraints.md` | `docs/<case>/02_dummy_data_spec.md`（データモデル・件数・分布・制約） |
| `src/generator.py` | `src/dummy_data/<case>.py` |
| `output/*.csv` | `data/<case>/raw/` |
| `output/evaluation_report.md` ほか評価成果物 | ダミーデータの品質確認（spec.md 第22節 step15）に利用 |

### 使い方の例

作業用ディレクトリ（例: `work/synthesize/case01/`）を用意し、`docs/case01_pseudonymized/`
の設計文書を `input/` として渡してパイプラインを実行します。生成された `generator.py` と
出力 CSV を、上表に従って `src/dummy_data/` と `data/*/raw/` に反映します。

Claude Code:

```text
/synthesize work/synthesize/case01
```

（`work/synthesize/` は生成器の作業領域です。最終成果物は `src/dummy_data/` と
`data/*/raw/` に配置し、生成器は seed 固定で再実行可能にします — spec.md 第15節。）

## 運用知見: synthesize を使うか、手書き生成器にするか

case01 の実装で得た判断基準（`case-study` スキルとも整合）:

- **手書きの読みやすい生成器を基本とする**（`src/dummy_data/<case>.py`）。本プロジェクトの教材性は
  「生成コードが読んで分かる」ことに価値がある。レポートで構造・加工方法が明示された事例を忠実に再現する
  ケース（＝case01 のような事例）はこちらが適する。実際 case01 は手書き生成器で実装した。
- **`synthesize` パイプラインを使うのは**、仕様が複雑・未知で、スキーマ推定（`1_spec_ingest`）や
  制約プランニング・評価ループ（`4_evaluate_and_refine`）の恩恵が大きい場合。多数テーブル・多数制約を
  自動で詰めたいときに向く。
- どちらを使っても、最終成果物は `src/dummy_data/` と `data/<case>/raw/`、seed 固定・再現可能、
  `groupby` で狙った傾向を検証、という受け入れ条件は共通。

## 注意

- スキル本体を編集する場合は、意図が upstream と分岐する点をコミットメッセージに明記してください。
- 個人情報の直接コピーは禁止（本プロジェクトの原則。spec.md 第2.1節、skill の Rules）。
