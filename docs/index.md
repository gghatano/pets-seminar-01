# 仮名加工情報・匿名加工情報 事例再現デモ

個人情報保護委員会事務局の事例レポートを参考に、**仮名加工情報**と**匿名加工情報**という2種類の加工を、実際のデータ加工 Python コードで再現する **デモ・教材** です。「どう加工するか」より、**どう考えて加工方針を決めるか**（データ加工設計の思考プロセス）を追体験することを狙いにしています。

## 学べる2つの加工

<div class="grid cards" markdown>

-   __case01 ・ 仮名加工情報__

    ---

    食品オンライン通販の顧客・購買データを、社内分析のために **仮名加工**します。会員IDを整理番号に置換するなど、*他の情報と照合しなければ個人を特定できない* 状態にする考え方を学びます。

    [→ ① 概要から読む](case01_pseudonymized/01_case_summary.md) ・ [▶ Colab で動かす](https://colab.research.google.com/github/gghatano/pets-seminar-01/blob/main/notebooks/case01_pseudonymized.ipynb)

-   __case02 ・ 匿名加工情報__

    ---

    ID-POS 購買データを第三者へ提供するために **匿名加工**します。年代・カテゴリ・金額区分へ丸めるなど、*特定の個人を識別できず復元もできない* 状態にする考え方を学びます。

    [→ ① 概要から読む](case02_anonymized/01_case_summary.md) ・ [▶ Colab で動かす](https://colab.research.google.com/github/gghatano/pets-seminar-01/blob/main/notebooks/case02_anonymized.ipynb)

</div>

[1枚チートシート（印刷/PDF可）](cheatsheet.md){ .md-button }

## 各事例の進め方（① 検討 → ② 実装 → ③ 結果）

どちらの事例も、次の **3層（① 検討 → ② 実装 → ③ 結果）** で進みます。①〜⑤は「考え方の設計」（この HTML サイト）、⑥は Colab での実装、⑦は結果の確認です。各事例のページ先頭に「いま何ステップ目か」を示すステッパーがあるので、上から順にたどれます。

| 層 | 媒体 | やること |
|----|------|----------|
| **① 検討**（ステップ 1〜5） | この HTML サイト | 事例を理解し、なぜその加工にするのかを**設計する** |
| **② 実装**（ステップ 6） | Google Colaboratory | 設計にもとづいて、実際に**加工処理を実行する** |
| **③ 結果**（ステップ 7） | この HTML サイト | 加工前後を比べ、**目的の分析が成立するか確認する** |

!!! info "この教材について"
    - **学べること**: ① 個人データを「見て」性質を評価する目、② 利用目的から「必要な情報・粒度」を考える力、③ Python での具体的な加工方法。
    - **所要時間の目安**: 1事例あたり 読み 15〜20分＋Colab 実行 10分。前提知識は不要（Python を少し読めると理解が深まります）。
    - 難しい用語は [用語集](glossary.md) にまとめています。

!!! warning "扱うデータについて"
    データはすべて教材用の**合成データ（ダミーデータ）**で、実在の個人・値とは無関係です。実際の個人データに対する法令適合性を保証するものではありません。

!!! question "ご意見・質問・誤りの指摘"
    教材の分かりにくい点・誤り・改善案は **[GitHub Issues](https://github.com/gghatano/pets-seminar-01/issues)** へお寄せください。セミナー中の質問メモの投稿先としても使えます。

---

リポジトリ: [gghatano/pets-seminar-01](https://github.com/gghatano/pets-seminar-01) ／ ライセンス: 教材コンテンツ CC BY 4.0・コード MIT（[詳細](https://github.com/gghatano/pets-seminar-01/blob/main/LICENSE)）。
