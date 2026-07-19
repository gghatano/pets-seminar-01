"""③ 結果ページ（docs/.../09_results.md）の数値が、コミット済みデータに対する
Notebook の加工・分析処理の出力と一致することを保証する（spec §25.2「サイト上の
結果 = 実際の実行結果」）。

09_results.md の表はサイトに手書きで載っているため、生成器・seed・加工ロジックを
変えると静かに乖離しうる。ここで再計算して照合し、乖離を CI で検出する。

注: 加工ロジック（to_decade / to_city / id_map）は notebooks/case01_pseudonymized.ipynb
と一致させること。Notebook を変更したら本テストの期待値も見直す。
実行済み Notebook のサイト埋め込み（単一実行ソース化）は issue #17 で追跡。
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data" / "case01_pseudonymized" / "raw"
REFERENCE_YEAR = 2026


def _to_decade(birth: str) -> str:
    age = REFERENCE_YEAR - int(str(birth)[:4])
    decade = min(age // 10 * 10, 80)
    return "80代以上" if decade == 80 else f"{decade}代"


def _to_city(addr: str) -> str:
    return re.sub(r"\d.*$", "", addr)


def _processed():
    customers = pd.read_csv(RAW / "customers.csv")
    purchases = pd.read_csv(RAW / "purchases.csv")
    web_access = pd.read_csv(RAW / "web_access.csv")
    id_map = {mid: f"R{i + 1:06d}" for i, mid in enumerate(sorted(customers["会員ID"]))}
    customers_p = pd.DataFrame(
        {
            "整理番号": customers["会員ID"].map(id_map),
            "性別": customers["性別"],
            "年代": customers["生年月日"].map(_to_decade),
            "市区町村": customers["住所"].map(_to_city),
        }
    )
    purchases_p = purchases.assign(整理番号=purchases["会員ID"].map(id_map))
    return customers, purchases, web_access, customers_p, purchases_p


def test_record_counts_match_results_doc():
    """09_results.md「レコード数」: customers 800 / purchases 4,789 / web_access 7,959。"""
    customers, purchases, web_access, _, _ = _processed()
    assert len(customers) == 800
    assert len(purchases) == 4789
    assert len(web_access) == 7959


def test_mean_amount_by_decade_matches_results_doc():
    """09_results.md「年代別 平均購入金額」の表と一致する。"""
    _, _, _, customers_p, purchases_p = _processed()
    m = purchases_p.merge(customers_p, on="整理番号")
    got = m.groupby("年代")["購入金額"].mean().round(0).astype(int).to_dict()
    expected = {
        "10代": 3877,
        "20代": 3064,
        "30代": 3430,
        "40代": 3662,
        "50代": 3682,
        "60代": 4045,
        "70代": 4115,
        "80代以上": 4243,
    }
    assert got == expected


def test_top5_cities_by_mean_amount_matches_results_doc():
    """09_results.md「市区町村別 平均購入金額（上位5）」と一致する。"""
    _, _, _, customers_p, purchases_p = _processed()
    m = purchases_p.merge(customers_p, on="整理番号")
    top5 = (
        m.groupby("市区町村")["購入金額"]
        .mean()
        .round(0)
        .astype(int)
        .sort_values(ascending=False)
        .head(5)
    )
    assert list(top5.index) == [
        "東京都大田区",
        "東京都八王子市",
        "東京都世田谷区",
        "東京都練馬区",
        "東京都江戸川区",
    ]
    assert top5.to_list() == [4401, 4315, 3870, 3818, 3796]


def test_top_categories_by_decade_matches_results_doc():
    """09_results.md「年代別 購入品目トップ3」（20代 / 70代）と一致する。"""
    _, _, _, customers_p, purchases_p = _processed()
    m = purchases_p.merge(customers_p, on="整理番号")

    def top3(decade: str) -> list[str]:
        return list(m[m["年代"] == decade]["購入品目"].value_counts(normalize=True).head(3).index)

    assert top3("20代") == ["飲料", "惣菜", "菓子"]
    assert top3("70代") == ["米・穀物", "精肉", "野菜"]
