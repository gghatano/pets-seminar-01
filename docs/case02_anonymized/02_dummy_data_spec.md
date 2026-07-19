# デモデータについて（case02）

> このデモで使う架空データ（合成データ）の作り方をまとめた**開発者向けメモ**です。学習の本筋は [① 事例概要](01_case_summary.md) から読んでください。

デモは実在データを使わず、生成した合成データで匿名加工処理を再現します。データは決定的に生成され、誰が実行しても同じ結果になります。

## データモデル

[テーブル定義](03_table_definition_before.md) のとおり、`customers`（顧客属性）／`transactions`（取引情報）／`purchases`（購買履歴）の3テーブルを会員ID・取引IDで関連づけます（図表2-2）。

| 項目 | 値 |
|------|----|
| 顧客数 | 900 |
| transactions 総件数 | 約4,600 |
| purchases 総件数 | 約14,000 |

地域は首都圏の市区郡、商品は食品カテゴリを用います。匿名加工後に「基本属性（年代・性別・エリア）× 購買傾向」の分析が成立するよう、年代×カテゴリ・エリアの傾向を持たせています。

## 特異値（施行規則第34条第4号の教材用）

「特異な記述等」の加工を体験できるよう、外れ値を**少数だけ**意図的に仕込んでいます。

- 超高齢者（生存者が極めて少ない生年月日）2名
- 希少/超高額商品（超高級メロン・限定コラボ雑貨・本まぐろ大トロ）3種
- 大量購入（同一商品を48・60個）2件

## 再現性

- 乱数 seed（`SEED = 20260719`）と基準日（`REFERENCE_DATE = 2026-07-01`）を固定。再生成はバイト一致します。
- 生成結果は `data/case02_anonymized/raw/` にコミットし、Notebook はそれを取得します。
- 生成器: [`src/dummy_data/case02_anonymized.py`](https://github.com/gghatano/pets-seminar-01/blob/main/src/dummy_data/case02_anonymized.py)

## 出力ファイル

- `data/case02_anonymized/raw/customers.csv`
- `data/case02_anonymized/raw/transactions.csv`
- `data/case02_anonymized/raw/purchases.csv`
