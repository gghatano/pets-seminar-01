# ② 実装（Google Colaboratory） — 6/7

<div class="wizard" markdown="1">
加工プロセス
{ .wizard-cap }

1. [全体概要](01_case_summary.md)
2. [データ概要理解](03_table_definition_before.md)
3. [データ詳細理解](04_column_classification.md)
4. [加工設計](05_processing_design.md)
5. [加工仕様](06_processing_spec.md)
6. **実装**
7. [結果確認](09_results.md)
</div>

加工設計（[① 検討](05_processing_design.md)）にもとづく **加工処理の実行** は、Google Colaboratory 上の Notebook で行います。ブラウザだけで上から順に実行できます。

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gghatano/pets-seminar-01/blob/main/notebooks/case01_pseudonymized.ipynb){ .md-button }

## Notebook で行うこと

- GitHub 上の生成済みデータの取得
- 加工処理の段階実行（識別子の処理 → 直接識別情報の削除 → 生年月日・住所の一般化 → 不要項目の削除 → 履歴情報の維持）
- 各ステップで「何を・なぜ加工するか」「Python コード」「加工結果」を確認

コードは、読めば何をしているか分かる粒度で書いています。実行結果は [③ 結果](09_results.md) にまとめています。

??? note "Colab 互換について（開発者向け）"
    Notebook は Colab（現状 pandas 2 系）で実行します。ローカル開発環境はより新しい pandas に解決されることがあるため、Notebook のコードは pandas 2 系互換の API で記述しています。配布する CSV は生成済みのため、生成器のバージョン差は結果に影響しません。
