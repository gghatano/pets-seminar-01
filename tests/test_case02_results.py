"""③ 結果ページ（docs/case02_anonymized/09_results.md）の数値が、コミット済み
データに対する Notebook の匿名加工・分析処理の出力と一致することを保証する
（spec §25.2「サイト上の結果 = 実際の実行結果」）。

09_results.md の表はサイトに手書きで載っているため、生成器・seed・加工ロジックを
変えると静かに乖離しうる。ここで再計算して照合し、乖離を CI で検出する。

注: 加工ロジックは notebooks/case02_anonymized.ipynb と一致させること。Notebook を
変更したら本テストの期待値も見直す。case01 の test_case01_results.py と対称。
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data" / "case02_anonymized" / "raw"
REFERENCE_YEAR = 2026

CATEGORY = {
    "G01": "野菜",
    "G02": "野菜",
    "G03": "果物",
    "G04": "果物",
    "G05": "精肉",
    "G06": "精肉",
    "G07": "鮮魚",
    "G08": "鮮魚",
    "G09": "米・穀物",
    "G10": "惣菜・パン",
    "G11": "惣菜・パン",
    "G12": "飲料",
    "G13": "飲料",
    "G14": "菓子",
    "G15": "菓子",
    "G16": "調味料",
    "G90": "果物",
    "G91": "菓子",
    "G92": "鮮魚",
}


def _processed():
    customers = pd.read_csv(RAW / "customers.csv")
    transactions = pd.read_csv(RAW / "transactions.csv")
    purchases = pd.read_csv(RAW / "purchases.csv")

    # 会員ID → 仮ID（1対1。集計結果はラベルに依らないが Notebook と同じ seed で再現）
    rng = np.random.default_rng(20260719)
    members = customers["会員ID"].tolist()
    order = rng.permutation(len(members))
    id_map = {members[o]: f"A{i + 1:06d}" for i, o in enumerate(order)}
    customers["仮ID"] = customers["会員ID"].map(id_map)
    transactions["仮ID"] = transactions["会員ID"].map(id_map)

    # 年代7区分 / 市区郡
    age = REFERENCE_YEAR - customers["生年月日"].str[:4].astype(int)
    bins = [0, 20, 30, 40, 50, 60, 70, 200]
    labels = ["20歳未満", "20代", "30代", "40代", "50代", "60代", "70歳以上"]
    customers_anon = pd.DataFrame({"仮ID": customers["仮ID"]})
    customers_anon["年代"] = pd.cut(age, bins=bins, right=False, labels=labels)
    customers_anon["性別"] = customers["性別"]
    pat = r"^(\D+?[都道府県](?:\D+?市\D+?区|\D+?[市区郡]))"
    customers_anon["市区郡"] = customers["住所"].str.extract(pat)
    customers_anon = customers_anon[["仮ID", "年代", "性別", "市区郡"]]

    # 購買履歴の匿名加工
    pu = purchases.merge(transactions[["取引ID", "仮ID"]], on="取引ID", how="left")
    pu["商品カテゴリ"] = pu["商品ID"].map(CATEGORY)
    pu["数量"] = pu["数量"].clip(upper=5)
    amt_bins = [0, 500, 1000, 2000, 5000, np.inf]
    amt_labels = ["〜499", "500〜999", "1,000〜1,999", "2,000〜4,999", "5,000円以上"]
    pu["金額区分"] = pd.cut(pu["金額"], bins=amt_bins, right=False, labels=amt_labels)
    purchases_anon = pu[["仮ID", "商品カテゴリ", "数量", "金額区分"]]

    return customers, transactions, purchases, customers_anon, purchases_anon


def test_record_counts_match_results_doc():
    """09_results.md「レコード数」: customers 900 / transactions 4,600 / purchases 13,984。"""
    customers, transactions, purchases, _, _ = _processed()
    assert len(customers) == 900
    assert len(transactions) == 4600
    assert len(purchases) == 13984


def test_pseudonymous_id_unique():
    """仮IDが一意（900件）。"""
    _, _, _, customers_anon, _ = _processed()
    assert customers_anon["仮ID"].is_unique
    assert len(customers_anon) == 900


def test_no_category_or_area_dropped_by_processing():
    """商品カテゴリ・市区郡の取りこぼし（NaN）が無い（09 の集計が全件に成立する前提）。"""
    _, _, _, customers_anon, purchases_anon = _processed()
    assert purchases_anon["商品カテゴリ"].notna().all()
    assert customers_anon["市区郡"].notna().all()


def test_qid_combination_counts_match_results_doc():
    """09_results.md「該当者の人数」: 組合せ 129 / 最小 1 / 5名未満 37組合せ(107名)。"""
    _, _, _, customers_anon, _ = _processed()
    grp = customers_anon.groupby(["年代", "性別", "市区郡"], observed=True).size()
    assert len(grp) == 129
    assert int(grp.min()) == 1
    assert int((grp < 5).sum()) == 37
    assert int(grp[grp < 5].sum()) == 107


def test_top_categories_by_decade_match_results_doc():
    """09_results.md「年代別 購入カテゴリ トップ3」（20代 / 40代 / 70歳以上）と一致する。"""
    _, _, _, customers_anon, purchases_anon = _processed()
    m = purchases_anon.merge(customers_anon, on="仮ID", how="left")

    def top3(band: str) -> list[str]:
        return m[m["年代"] == band]["商品カテゴリ"].value_counts().head(3).index.tolist()

    assert top3("20代") == ["惣菜・パン", "菓子", "飲料"]
    assert top3("40代") == ["果物", "野菜", "精肉"]
    assert top3("70歳以上") == ["野菜", "菓子", "鮮魚"]


def test_amount_bucket_ratios_by_decade_match_results_doc():
    """09_results.md「年代別 金額区分の構成（割合）」の 20代/40代/70歳以上 行と一致する。"""
    _, _, _, customers_anon, purchases_anon = _processed()
    m = purchases_anon.merge(customers_anon, on="仮ID", how="left")
    tab = pd.crosstab(m["年代"], m["金額区分"], normalize="index").round(2)
    cols = ["〜499", "500〜999", "1,000〜1,999", "2,000〜4,999", "5,000円以上"]
    assert tab.loc["20代", cols].to_list() == [0.50, 0.29, 0.14, 0.06, 0.02]
    assert tab.loc["40代", cols].to_list() == [0.45, 0.33, 0.14, 0.05, 0.03]
    assert tab.loc["70歳以上", cols].to_list() == [0.41, 0.34, 0.15, 0.06, 0.03]
