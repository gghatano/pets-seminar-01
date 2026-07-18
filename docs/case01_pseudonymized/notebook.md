# ② 実装（Google Colaboratory）

事例 → データを見る → 情報特性 → 加工設計 → 加工仕様 → **実装（Colab）** → 結果
{ .process-nav }

加工設計（[① 検討](05_processing_design.md)）にもとづく **加工処理の実行** は、Google Colaboratory 上の Notebook で行います。ブラウザだけで上から順に実行できます。

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gghatano/pets-seminar-01/blob/main/notebooks/case01_pseudonymized.ipynb){ .md-button }

## Notebook で行うこと

- GitHub 上の生成済みデータの取得
- 加工処理の段階実行（識別子の処理 → 直接識別情報の削除 → 生年月日・住所の一般化 → 不要項目の削除 → 履歴情報の維持）
- 各ステップで「何を・なぜ加工するか」「Python コード」「加工結果」を確認

コードは、読めば何をしているか分かる粒度で書いています。実行結果は [③ 結果](09_results.md) にまとめています。

??? note "Colab 互換について（開発者向け）"
    Notebook は Colab（現状 pandas 2 系）で実行します。ローカル開発環境はより新しい pandas に解決されることがあるため、Notebook のコードは pandas 2 系互換の API で記述しています。配布する CSV は生成済みのため、生成器のバージョン差は結果に影響しません。
