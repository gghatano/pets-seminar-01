# 仮名加工情報・匿名加工情報 事例再現デモ

個人情報保護委員会事務局が公開している事例レポートをもとに、実際のデータ加工を Python で再現する **デモ・教材** です。

[▶ Colab でデモを試す](https://colab.research.google.com/github/gghatano/pets-seminar-01/blob/main/notebooks/case01_pseudonymized.ipynb){ .md-button .md-button--primary }
[まず読む（事例概要へ）](case01_pseudonymized/01_case_summary.md){ .md-button }
[1枚チートシート（印刷/PDF可）](cheatsheet.md){ .md-button }

!!! info "この教材について"
    - **学べること**: ① 個人データを「見て」どんな性質があるかを評価する目、② 利用目的から「必要な情報・粒度」を考える力、③ Python での具体的な加工方法。
    - **所要時間の目安**: 読み 15〜20分＋Colab 実行 10分。
    - **前提知識**: 不要（Python を少し読めると理解が深まります）。難しい用語は [用語集](glossary.md) にまとめています。

!!! warning "教材としての位置づけ"
    扱うデータはすべて教材用の**合成データ（ダミーデータ）**で、実在の個人・値とは無関係です。
    実際の個人データに対する法令適合性を保証するものではありません。
    レポート記載事項〔報告〕と、教材用に補った内容〔独自〕は本文中で区別しています（[凡例](glossary.md#出典区分ラベルの凡例)）。

## この教材の中心

「加工コードそのもの」ではなく、
**データを見る → 利用目的を考える → 情報特性を評価する → 加工方針を設計する → 実装して確認する**
という **データ加工設計の思考プロセス** を、具体的な事例で追体験してもらうことを狙いにしています。

## 進め方（3層構成）

媒体を役割で分けています。上から順にたどってください。

| 層 | 媒体 | やること |
|----|------|----------|
| **① 検討** | この HTML サイト | 事例を理解し、なぜその加工にするのかを**設計する** |
| **② 実装** | Google Colaboratory | 設計にもとづいて、実際に**加工処理を実行する** |
| **③ 結果** | この HTML サイト | 加工前後を比べ、**目的の分析が成立するか確認する** |

1. **[① 事例概要](case01_pseudonymized/01_case_summary.md)** から読み始める
2. **[② Colab](case01_pseudonymized/notebook.md)** を開いて上から実行する
3. **[③ 結果](case01_pseudonymized/09_results.md)** で加工の効果を確認する

## 事例

| 事例 | 種別 | ステータス | 実行 |
|------|------|-----------|------|
| **case01** | 仮名加工情報（食品オンライン通販の顧客・購買データ） | ✅ 公開中 | [Colab](https://colab.research.google.com/github/gghatano/pets-seminar-01/blob/main/notebooks/case01_pseudonymized.ipynb) |
| case02 | 匿名加工情報 | 🚧 準備中 | — |

---

詳細な設計・実装指示は [設計・実装指示書 (spec)](spec.md)（開発者向け）を正本とします。
リポジトリ・ご意見: [gghatano/pets-seminar-01](https://github.com/gghatano/pets-seminar-01)
