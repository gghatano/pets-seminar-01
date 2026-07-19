"""case01 ダミーデータ生成の自動テスト（spec.md 第15節）。

- 固定 seed による再現性（同一 seed → 同一データ）
- スキーマ・主キーの一意性・参照整合性
- 想定件数（1顧客に1件以上の購買/アクセス履歴）
- コミット済み CSV とスキーマの整合
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from dummy_data import case01_pseudonymized as gen

RAW = Path(__file__).resolve().parents[1] / "data" / "case01_pseudonymized" / "raw"

CUSTOMER_COLS = [
    "会員ID",
    "氏名",
    "生年月日",
    "性別",
    "郵便番号",
    "住所",
    "携帯電話番号",
    "電子メールアドレス",
    "クレジットカード番号",
]
PURCHASE_COLS = ["購買ID", "会員ID", "購入年月日", "購入品目", "購入数量", "購入金額"]
ACCESS_COLS = ["アクセスID", "会員ID", "Cookie_ID", "アクセス日時", "閲覧カテゴリ"]


@pytest.fixture(scope="module")
def generated():
    rng = np.random.default_rng(gen.SEED)
    customers = gen.generate_customers(rng)
    purchases = gen.generate_purchases(rng, customers)
    web_access = gen.generate_web_access(rng, customers)
    return customers, purchases, web_access


def test_reproducible_with_fixed_seed():
    a = gen.generate_customers(np.random.default_rng(gen.SEED))
    b = gen.generate_customers(np.random.default_rng(gen.SEED))
    pd.testing.assert_frame_equal(a, b)


def test_schema(generated):
    customers, purchases, web_access = generated
    assert list(customers.columns) == CUSTOMER_COLS
    assert list(purchases.columns) == PURCHASE_COLS
    assert list(web_access.columns) == ACCESS_COLS


def test_primary_keys_unique(generated):
    customers, purchases, web_access = generated
    assert customers["会員ID"].is_unique
    assert purchases["購買ID"].is_unique
    assert web_access["アクセスID"].is_unique
    assert len(customers) == gen.N_CUSTOMERS


def test_referential_integrity(generated):
    customers, purchases, web_access = generated
    ids = set(customers["会員ID"])
    assert set(purchases["会員ID"]).issubset(ids)
    assert set(web_access["会員ID"]).issubset(ids)


def test_every_customer_has_history(generated):
    customers, purchases, web_access = generated
    assert set(customers["会員ID"]) == set(purchases["会員ID"])
    assert set(customers["会員ID"]) == set(web_access["会員ID"])


def test_value_domains(generated):
    customers, purchases, web_access = generated
    assert set(customers["性別"]).issubset({"男性", "女性"})
    assert set(purchases["購入品目"]).issubset(set(gen.CATEGORIES))
    assert (purchases["購入数量"] >= 1).all()
    assert (purchases["購入金額"] > 0).all()


def test_committed_csv_matches_schema():
    """コミット済みの生成データが存在し、スキーマが一致する。"""
    customers = pd.read_csv(RAW / "customers.csv")
    purchases = pd.read_csv(RAW / "purchases.csv")
    web_access = pd.read_csv(RAW / "web_access.csv")
    assert list(customers.columns) == CUSTOMER_COLS
    assert list(purchases.columns) == PURCHASE_COLS
    assert list(web_access.columns) == ACCESS_COLS
    assert len(customers) == gen.N_CUSTOMERS
    assert set(purchases["会員ID"]).issubset(set(customers["会員ID"]))


def test_committed_csv_is_byte_identical_to_regeneration(tmp_path):
    """コミット済み CSV が、生成器の再生成結果と**バイト一致**する。

    CLAUDE.md / spec §15 の「再生成はバイト一致」を CI で保証する。生成器を
    変更してコミット済み CSV を更新し忘れると、このテストが失敗する。
    書き出しは main() と同じ引数（index=False, encoding=utf-8）で行う。
    """
    rng = np.random.default_rng(gen.SEED)
    customers = gen.generate_customers(rng)
    purchases = gen.generate_purchases(rng, customers)
    web_access = gen.generate_web_access(rng, customers)

    for name, df in [
        ("customers.csv", customers),
        ("purchases.csv", purchases),
        ("web_access.csv", web_access),
    ]:
        out = tmp_path / name
        df.to_csv(out, index=False, encoding="utf-8")
        assert out.read_bytes() == (RAW / name).read_bytes(), (
            f"{name} がコミット済みデータと一致しません。"
            " 生成器を変更したら CSV を再生成してコミットしてください:"
            " uv run python src/dummy_data/case01_pseudonymized.py"
        )
