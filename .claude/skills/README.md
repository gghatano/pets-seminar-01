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

| upstream の成果物 | 本プロジェクトでの対応 |
|-------------------|------------------------|
| `input/table_definition*` | `docs/case01_pseudonymized/03_table_definition_before.md` |
| `input/data_spec.md` / `input/constraints.md` | `docs/case01_pseudonymized/02_dummy_data_spec.md`（データモデル・件数・分布・制約） |
| `src/generator.py` | `src/dummy_data/case01_pseudonymized.py` |
| `output/*.csv` | `data/case01_pseudonymized/raw/` |
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

## 注意

- スキル本体を編集する場合は、意図が upstream と分岐する点をコミットメッセージに明記してください。
- 個人情報の直接コピーは禁止（本プロジェクトの原則。spec.md 第2.1節、skill の Rules）。
