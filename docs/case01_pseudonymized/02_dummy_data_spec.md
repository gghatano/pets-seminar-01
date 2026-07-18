# デモデータについて（case01）

> このデモで使う架空データ（合成データ）の作り方をまとめた**開発者向けメモ**です。学習の本筋は [① 事例概要](01_case_summary.md) から読んでください。

デモは実在データを使わず、生成した合成データで加工処理を再現します。データは決定的に生成され、誰が実行しても同じ結果になります。

## データモデル

[テーブル定義](03_table_definition_before.md) のとおり、`customers`（顧客）／`purchases`（購買履歴）／`web_access`（Webアクセス履歴）の3テーブルを会員IDで関連づけます。

| 項目 | 値 |
|------|----|
| 顧客数 | 800 |
| purchases 総件数 | 約4,800 |
| web_access 総件数 | 約8,000 |

Colab で短時間に実行できる規模です。地域は首都圏（東京・神奈川・埼玉・千葉）の市区町村、商品は食品カテゴリ10種を用います。

## 再現性

- 乱数 seed（`SEED = 20260717`）と基準日（`REFERENCE_DATE = 2026-07-01`）を固定。再生成はバイト一致します。
- 生成結果は `data/case01_pseudonymized/raw/` にコミットし、Notebook はそれを取得します。
- 生成器: [`src/dummy_data/case01_pseudonymized.py`](https://github.com/gghatano/pets-seminar-01/blob/main/src/dummy_data/case01_pseudonymized.py)

## 出力ファイル

- `data/case01_pseudonymized/raw/customers.csv`
- `data/case01_pseudonymized/raw/purchases.csv`
- `data/case01_pseudonymized/raw/web_access.csv`
