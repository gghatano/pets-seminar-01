"""case02（匿名加工情報）ダミーデータ生成スクリプト。

事務局レポート事例編「2.1.1 購買履歴の事例1（ID-POS データ）」（pp.20〜27、
図表2-1〜2-5）の元データ構造を再現する教材用ダミーデータを生成する。

方針（spec.md 第8・15節 / .claude/skills/case-study）:
- 生成仕様は docs/case02_anonymized/02_dummy_data_spec.md を正本とする。
- 乱数 seed を固定し、同一データを再生成可能にする（バイト一致）。
- 3テーブル（顧客属性／取引情報／購買履歴）を会員IDで関連づける（図表2-2）。
- 匿名加工後に「基本属性（年代・性別・居住エリア）× 購買傾向」の分析が成立するよう、
  一様乱数ではなく人工的な傾向を持たせる（レポート未記載の設定は教材用の独自設定）。
- 施行規則第34条第4号「特異な記述等」を教材で体験できるよう、外れ値（超高齢者・
  希少/超高額商品・大量購入）を意図的に少数だけ仕込む。

出力: data/case02_anonymized/raw/{customers,transactions,purchases}.csv

注意: 生成される氏名・住所・電話番号・商品名・金額等はすべて教材用の架空データであり、
実在の個人・値・店舗とは無関係。
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

# ---- 再現性のための固定値 --------------------------------------------------
SEED = 20260719
REFERENCE_DATE = date(2026, 7, 1)  # 年齢計算・履歴期間の基準日（固定）
HISTORY_START = datetime(2025, 7, 1)  # 取引履歴の期間（1年間）
HISTORY_DAYS = 364
N_CUSTOMERS = 900

OUT_DIR = Path(__file__).resolve().parents[2] / "data" / "case02_anonymized" / "raw"

# ---- マスタ定義（すべて教材用の独自設定） ----------------------------------
# 首都圏のエリア（都道府県・市区郡・代表町名・出現重み）。
# 匿名加工では住所を「市区郡まで」に丸めるため、町名・丁目番地は加工で落とす想定。
AREAS = [
    ("東京都", "世田谷区", ["赤堤", "経堂", "上北沢"], 9),
    ("東京都", "杉並区", ["高円寺", "阿佐谷", "荻窪"], 7),
    ("東京都", "大田区", ["蒲田", "大森", "田園調布"], 6),
    ("東京都", "八王子市", ["南大沢", "北野", "めじろ台"], 4),
    ("神奈川県", "横浜市青葉区", ["美しが丘", "たまプラーザ", "市ケ尾"], 8),
    ("神奈川県", "川崎市宮前区", ["宮崎", "鷺沼", "有馬"], 6),
    ("神奈川県", "藤沢市", ["辻堂", "湘南台", "善行"], 4),
    ("埼玉県", "さいたま市浦和区", ["常盤", "岸町", "北浦和"], 6),
    ("埼玉県", "川口市", ["並木", "芝", "戸塚"], 5),
    ("千葉県", "船橋市", ["本町", "習志野台", "北習志野"], 5),
    ("千葉県", "市川市", ["八幡", "行徳", "国府台"], 4),
]

STORES = [
    ("S01", "PPCマート世田谷店", "東京都"),
    ("S02", "PPCマート杉並店", "東京都"),
    ("S03", "PPCマート大田店", "東京都"),
    ("S04", "PPCマート青葉店", "神奈川県"),
    ("S05", "PPCマート宮前店", "神奈川県"),
    ("S06", "PPCマート浦和店", "埼玉県"),
    ("S07", "PPCマート船橋店", "千葉県"),
    ("S08", "PPCマート霞が関店", "東京都"),
]

SURNAMES = [
    "佐藤",
    "鈴木",
    "高橋",
    "田中",
    "伊藤",
    "渡辺",
    "山本",
    "中村",
    "小林",
    "加藤",
    "吉田",
    "山田",
    "佐々木",
    "松本",
    "井上",
    "木村",
]
GIVEN_M = ["翔太", "大輔", "直樹", "健一", "拓也", "亮", "誠", "浩二", "隆", "聡"]
GIVEN_F = ["愛", "彩", "さくら", "美咲", "陽子", "麻衣", "由美", "恵", "遥", "杏"]

# 商品カタログ: (商品ID, 商品名, カテゴリー, 標準価格, 出現重み)
# ありふれた商品。年代×カテゴリーの嗜好差は後段の重みで表現する。
PRODUCTS = [
    ("G01", "トマト", "野菜", 250, 10),
    ("G02", "レタス", "野菜", 180, 9),
    ("G03", "りんご", "果物", 300, 8),
    ("G04", "バナナ", "果物", 200, 9),
    ("G05", "牛肉（国産）", "精肉", 900, 6),
    ("G06", "鶏むね肉", "精肉", 450, 8),
    ("G07", "さば", "鮮魚", 400, 6),
    ("G08", "まぐろ刺身", "鮮魚", 800, 5),
    ("G09", "こしひかり5kg", "米・穀物", 2600, 4),
    ("G10", "食パン", "惣菜・パン", 220, 9),
    ("G11", "からあげ弁当", "惣菜・パン", 550, 8),
    ("G12", "緑茶ペットボトル", "飲料", 130, 12),
    ("G13", "コーヒー豆", "飲料", 780, 4),
    ("G14", "ポテトチップス", "菓子", 160, 9),
    ("G15", "チョコレート", "菓子", 210, 8),
    ("G16", "しょうゆ", "調味料", 320, 5),
]

# 希少/超高額商品（＝施行規則第34条第4号「特異な記述等」の教材用に少数だけ登場させる）。
RARE_PRODUCTS = [
    ("G90", "超高級メロン（桐箱入）", "果物", 30000, 1),
    ("G91", "限定コラボ雑貨セット", "菓子", 18000, 1),
    ("G92", "本まぐろ大トロ（一本釣り）", "鮮魚", 12000, 1),
]

# 年代帯（内部の生成用。加工では「年代7区分」に丸める）
# カテゴリー嗜好の重み（若年ほど惣菜・飲料・菓子、高年ほど野菜・鮮魚・米に寄せる）
AGE_CATEGORY_BIAS = {
    "young": {"惣菜・パン": 1.8, "飲料": 1.6, "菓子": 1.7},
    "mid": {"精肉": 1.3, "果物": 1.2, "調味料": 1.2},
    "senior": {"野菜": 1.7, "鮮魚": 1.7, "米・穀物": 1.6},
}


def _age_band(age: int) -> str:
    if age < 35:
        return "young"
    if age < 60:
        return "mid"
    return "senior"


def _make_customers(rng: np.random.Generator) -> pd.DataFrame:
    area_w = np.array([a[3] for a in AREAS], dtype=float)
    area_w /= area_w.sum()

    rows = []
    for i in range(1, N_CUSTOMERS + 1):
        member_id = f"M{i:06d}"
        gender = "男性" if rng.random() < 0.48 else "女性"
        given = rng.choice(GIVEN_M if gender == "男性" else GIVEN_F)
        name = f"{rng.choice(SURNAMES)} {given}"

        # 年齢: 平均46・標準偏差15（20〜84歳に収める）
        age = int(np.clip(round(rng.normal(46, 15)), 20, 84))
        birth = date(REFERENCE_DATE.year - age, int(rng.integers(1, 13)), int(rng.integers(1, 29)))

        ai = rng.choice(len(AREAS), p=area_w)
        pref, city, machis, _ = AREAS[ai]
        machi = rng.choice(machis)
        addr = f"{pref}{city}{machi}{rng.integers(1, 6)}丁目{rng.integers(1, 30)}-{rng.integers(1, 20)}"

        phone = f"090-{rng.integers(1000, 10000)}-{rng.integers(1000, 10000)}"
        rows.append([member_id, name, birth.isoformat(), gender, phone, addr])

    df = pd.DataFrame(rows, columns=["会員ID", "氏名", "生年月日", "性別", "電話番号", "住所"])

    # --- 特異値（34条4号）: 超高齢者を2名だけ仕込む（生存者が極めて少ない生年月日） ---
    for idx, byear in [(0, 1922), (1, 1925)]:
        df.loc[idx, "生年月日"] = date(byear, 3, 3).isoformat()
    return df


def _category_weights(age_band: str) -> np.ndarray:
    bias = AGE_CATEGORY_BIAS[age_band]
    w = []
    for _, _, cat, _, base_w in PRODUCTS:
        w.append(base_w * bias.get(cat, 1.0))
    return np.array(w, dtype=float)


def _make_transactions_and_purchases(
    rng: np.random.Generator, customers: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    store_w = np.array([9, 7, 6, 8, 6, 6, 5, 3], dtype=float)
    store_w /= store_w.sum()

    tx_rows: list[list] = []
    pu_rows: list[list] = []
    tx_counter = 0
    line_counter = 0

    ages = {
        r["会員ID"]: REFERENCE_DATE.year - int(r["生年月日"][:4]) for _, r in customers.iterrows()
    }

    prod_names = [p[1] for p in PRODUCTS]
    prod_ids = [p[0] for p in PRODUCTS]
    prod_prices = {p[0]: p[3] for p in PRODUCTS}

    for member_id in customers["会員ID"]:
        band = _age_band(ages[member_id])
        cat_w = _category_weights(band)
        cat_w /= cat_w.sum()
        n_tx = int(rng.integers(2, 9))  # 2〜8回の来店
        for _ in range(n_tx):
            tx_counter += 1
            tx_id = f"T{tx_counter:07d}"
            offset = int(rng.integers(0, HISTORY_DAYS + 1))
            secs = int(rng.integers(9 * 3600, 21 * 3600))  # 9:00〜21:00
            dt = HISTORY_START + timedelta(days=offset, seconds=secs)
            si = rng.choice(len(STORES), p=store_w)
            store_id, store_name, _ = STORES[si]
            staff_id = f"E{rng.integers(1, 41):03d}"
            tx_rows.append(
                [tx_id, member_id, dt.strftime("%Y-%m-%d %H:%M:%S"), store_id, store_name, staff_id]
            )

            n_items = int(rng.integers(1, 6))  # 1〜5明細
            for _ in range(n_items):
                line_counter += 1
                gi = rng.choice(len(PRODUCTS), p=cat_w)
                gid, gname = prod_ids[gi], prod_names[gi]
                price = prod_prices[gid]
                qty = int(rng.integers(1, 4))
                amount = int(price * qty * rng.uniform(0.95, 1.15))
                pu_rows.append([f"D{line_counter:08d}", tx_id, gid, gname, qty, amount])

    tx = pd.DataFrame(
        tx_rows, columns=["取引ID", "会員ID", "利用日時", "店舗ID", "店舗名", "担当者ID"]
    )
    pu = pd.DataFrame(pu_rows, columns=["明細ID", "取引ID", "商品ID", "商品名", "数量", "金額"])

    # --- 特異値（34条4号）を購買履歴に少数だけ仕込む ---
    rare_tx = rng.choice(tx["取引ID"].to_numpy(), size=3, replace=False)
    for tx_id, (gid, gname, cat, price, _) in zip(rare_tx, RARE_PRODUCTS):
        line_counter += 1
        pu.loc[len(pu)] = [f"D{line_counter:08d}", tx_id, gid, gname, 1, price]
    # 大量購入（ありふれた商品を極端な個数で）
    bulk_tx = rng.choice(tx["取引ID"].to_numpy(), size=2, replace=False)
    for tx_id, qty in zip(bulk_tx, [48, 60]):
        line_counter += 1
        pu.loc[len(pu)] = [f"D{line_counter:08d}", tx_id, "G12", "緑茶ペットボトル", qty, 130 * qty]

    pu = pu.sort_values("明細ID").reset_index(drop=True)
    return tx, pu


def main() -> None:
    rng = np.random.default_rng(SEED)
    customers = _make_customers(rng)
    transactions, purchases = _make_transactions_and_purchases(rng, customers)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    customers.to_csv(OUT_DIR / "customers.csv", index=False, encoding="utf-8")
    transactions.to_csv(OUT_DIR / "transactions.csv", index=False, encoding="utf-8")
    purchases.to_csv(OUT_DIR / "purchases.csv", index=False, encoding="utf-8")

    print(f"customers:    {len(customers):>6} rows -> {OUT_DIR / 'customers.csv'}")
    print(f"transactions: {len(transactions):>6} rows -> {OUT_DIR / 'transactions.csv'}")
    print(f"purchases:    {len(purchases):>6} rows -> {OUT_DIR / 'purchases.csv'}")


if __name__ == "__main__":
    main()
