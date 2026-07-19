"""case02（匿名加工情報 / ID-POS）ダミーデータ生成の自動テスト（spec.md 第15節）。

- 固定 seed による再現性（同一 seed → 同一データ）
- スキーマ・主キーの一意性・参照整合性・値域
- 施行規則第34条第4号の教材用に仕込んだ特異値（超高齢者・超高額商品・大量購入）の存在
- コミット済み CSV とスキーマの整合
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from dummy_data import case02_anonymized as gen

RAW = Path(__file__).resolve().parents[1] / "data" / "case02_anonymized" / "raw"

CUSTOMER_COLS = ["会員ID", "氏名", "生年月日", "性別", "電話番号", "住所"]
TRANSACTION_COLS = ["取引ID", "会員ID", "利用日時", "店舗ID", "店舗名", "担当者ID"]
PURCHASE_COLS = ["明細ID", "取引ID", "商品ID", "商品名", "数量", "金額"]

PRODUCT_NAMES = {p[1] for p in gen.PRODUCTS} | {p[1] for p in gen.RARE_PRODUCTS}


def _generate():
    rng = np.random.default_rng(gen.SEED)
    customers = gen._make_customers(rng)
    transactions, purchases = gen._make_transactions_and_purchases(rng, customers)
    return customers, transactions, purchases


def test_reproducible_with_fixed_seed():
    a = gen._make_customers(np.random.default_rng(gen.SEED))
    b = gen._make_customers(np.random.default_rng(gen.SEED))
    pd.testing.assert_frame_equal(a, b)


def test_schema():
    customers, transactions, purchases = _generate()
    assert list(customers.columns) == CUSTOMER_COLS
    assert list(transactions.columns) == TRANSACTION_COLS
    assert list(purchases.columns) == PURCHASE_COLS


def test_primary_keys_unique():
    customers, transactions, purchases = _generate()
    assert customers["会員ID"].is_unique
    assert transactions["取引ID"].is_unique
    assert purchases["明細ID"].is_unique
    assert len(customers) == gen.N_CUSTOMERS


def test_referential_integrity():
    customers, transactions, purchases = _generate()
    assert set(transactions["会員ID"]).issubset(set(customers["会員ID"]))
    assert set(purchases["取引ID"]).issubset(set(transactions["取引ID"]))


def test_value_domains():
    customers, transactions, purchases = _generate()
    assert set(customers["性別"]).issubset({"男性", "女性"})
    assert set(purchases["商品名"]).issubset(PRODUCT_NAMES)
    assert (purchases["数量"] >= 1).all()
    assert (purchases["金額"] > 0).all()


def test_planted_outliers_for_article34_item4():
    """施行規則第34条第4号（特異な記述等）を体験するための外れ値が存在する。"""
    customers, transactions, purchases = _generate()
    ages = gen.REFERENCE_DATE.year - customers["生年月日"].str[:4].astype(int)
    assert ages.max() >= 100  # 超高齢者（生存者が極めて少ない生年月日）
    assert (purchases["金額"] >= 10000).any()  # 超高額商品
    assert (purchases["数量"] >= 40).any()  # 大量購入


def test_committed_csv_matches_schema():
    customers = pd.read_csv(RAW / "customers.csv")
    transactions = pd.read_csv(RAW / "transactions.csv")
    purchases = pd.read_csv(RAW / "purchases.csv")
    assert list(customers.columns) == CUSTOMER_COLS
    assert list(transactions.columns) == TRANSACTION_COLS
    assert list(purchases.columns) == PURCHASE_COLS
    assert len(customers) == gen.N_CUSTOMERS
    assert set(purchases["取引ID"]).issubset(set(transactions["取引ID"]))
