# ② 実装（Google Colaboratory）

加工設計（[① 検討](05_processing_design.md)）にもとづく **加工処理の実行** は、
Google Colaboratory 上の Notebook で行います。ブラウザだけで上から順に実行できます。

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gghatano/pets-seminar-01/blob/main/notebooks/case01_pseudonymized.ipynb){ .md-button }

!!! note "ステータス"
    Notebook は現在プレースホルダです。加工仕様（[06 加工仕様](06_processing_spec.md)）の確定後に実装します。

!!! warning "Colab 互換の注意"
    Notebook は Google Colaboratory 上（現状 pandas 2 系）で実行します。ローカル開発環境（uv）は
    より新しい pandas に解決されることがあるため、**Notebook のコードは pandas 2 系互換の API で記述**してください。
    ダミーデータは生成済み CSV を配布するため、生成器（`src/dummy_data/`）のバージョン差は結果に影響しません。

## Notebook で行うこと

- GitHub 上の生成済みダミーデータの取得（ローカルファイルに依存しない）
- 加工処理の段階実行（識別子の処理 → 直接識別情報の削除 → 生年月日等の一般化 → 住所等の一般化 → 不要項目の削除 → 履歴情報の維持）
- 各ステップで「何を・なぜ加工するか」「Python コード」「加工結果」を確認

Notebook の中核処理は、コードを読めば何をしているか分かる粒度で書きます（過度に関数へ隠蔽しない）。
詳細な設計は本サイトの [① 検討](05_processing_design.md) を正本とし、Notebook には理解に必要な要点のみ掲載します。

## 実行結果の確認

加工前後の比較・確認テスト結果・加工後分析は [③ 結果](09_results.md) にまとめます。
将来的には、実行済み Notebook を `mkdocs-jupyter` でこのサイトに埋め込み、
「サイト上の結果 = 実際の実行結果」を保証する構成にします。
