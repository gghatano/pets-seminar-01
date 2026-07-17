"""case01（仮名加工情報）ダミーデータ生成スクリプト。

事務局レポート事例編「1.1 事例1」（食品オンライン通販の事業者A）の元データ構造
（図表1-1）を再現する教材用ダミーデータを生成する。

方針（spec.md 第8・15節）:
- 生成仕様は docs/case01_pseudonymized/02_dummy_data_spec.md を正本とする。
- 乱数 seed を固定し、同一データを再生成可能にする。
- 3テーブル（顧客マスタ／購買履歴／Webアクセス履歴）を会員IDで関連づける。
- 加工後に「地域×年代・性別×商品カテゴリ／購入金額」の傾向分析が成立するよう、
  一様乱数ではなく人工的な傾向を持たせる（レポート未記載の設定は教材用の独自設定）。

出力: data/case01_pseudonymized/raw/{customers,purchases,web_access}.csv

注意: 生成される氏名・住所・電話番号・メール・クレジットカード番号等はすべて
教材用の架空データであり、実在の個人・値とは無関係。
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

# ---- 再現性のための固定値 --------------------------------------------------
SEED = 20260717
REFERENCE_DATE = date(2026, 7, 1)  # 年齢計算・履歴期間の基準日（固定）
N_CUSTOMERS = 800

OUT_DIR = Path(__file__).resolve().parents[2] / "data" / "case01_pseudonymized" / "raw"

# ---- マスタ定義（すべて教材用の独自設定） ----------------------------------
# 首都圏の市区町村（都道府県・代表郵便番号・出現重み・実店舗商圏フラグ）
CITIES = [
    # (都道府県, 市区町村, 郵便番号, 重み, 商圏)
    ("東京都", "世田谷区", "154-0000", 9, True),
    ("東京都", "杉並区", "166-0000", 7, True),
    ("東京都", "練馬区", "176-0000", 7, True),
    ("東京都", "大田区", "144-0000", 6, True),
    ("東京都", "江戸川区", "132-0000", 5, False),
    ("東京都", "八王子市", "192-0000", 5, False),
    ("神奈川県", "横浜市青葉区", "225-0000", 8, True),
    ("神奈川県", "川崎市宮前区", "216-0000", 6, True),
    ("神奈川県", "藤沢市", "251-0000", 4, False),
    ("埼玉県", "さいたま市浦和区", "330-0000", 6, True),
    ("埼玉県", "川口市", "332-0000", 5, False),
    ("埼玉県", "所沢市", "359-0000", 3, False),
    ("千葉県", "船橋市", "273-0000", 5, False),
    ("千葉県", "市川市", "272-0000", 4, True),
    ("千葉県", "柏市", "277-0000", 3, False),
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
    "山口",
    "松本",
    "井上",
]
GIVEN_MALE = ["翔太", "健一", "大輔", "拓也", "直樹", "亮", "誠", "洋平", "隆", "和也"]
GIVEN_FEMALE = ["美咲", "陽子", "彩", "由美", "麻衣", "さくら", "香織", "恵", "愛", "千夏"]

# 食品カテゴリ（食品オンライン通販の想定）
CATEGORIES = [
    "野菜",
    "果物",
    "精肉",
    "鮮魚",
    "米・穀物",
    "惣菜",
    "飲料",
    "菓子",
    "調味料",
    "有機食品セット",
]

# カテゴリ別の基準単価（円、独自設定）
BASE_PRICE = {
    "野菜": 500,
    "果物": 800,
    "精肉": 1200,
    "鮮魚": 1500,
    "米・穀物": 2500,
    "惣菜": 600,
    "飲料": 400,
    "菓子": 500,
    "調味料": 450,
    "有機食品セット": 3500,
}


def _category_weights(decade_index: int) -> np.ndarray:
    """年代帯（0=10代 ... 7=80代以上）ごとのカテゴリ選好（独自設定の人工傾向）。

    若年層は惣菜・菓子・飲料寄り、高年層は野菜・鮮魚・米・有機寄り。
    """
    base = np.array([6, 5, 5, 5, 5, 6, 6, 6, 4, 4], dtype=float)  # 野菜..有機
    youth = np.array([2, 3, 2, 1, 1, 7, 8, 8, 2, 1], dtype=float)
    senior = np.array([9, 6, 7, 8, 8, 4, 3, 2, 6, 8], dtype=float)
    t = np.clip(decade_index / 7.0, 0.0, 1.0)  # 0(若)→1(高)
    return (1 - t) * (0.4 * base + 0.6 * youth) + t * (0.4 * base + 0.6 * senior)


def _age_to_decade_index(age: int) -> int:
    """年齢→年代帯インデックス（10代=0 ... 80代以上=7）。"""
    return int(min(max(age // 10 - 1, 0), 7))


def generate_customers(rng: np.random.Generator) -> pd.DataFrame:
    n = N_CUSTOMERS
    weights = np.array([c[3] for c in CITIES], dtype=float)
    city_idx = rng.choice(len(CITIES), size=n, p=weights / weights.sum())
    # 年齢: 30-50代を厚めに、18〜84歳
    ages = np.clip(rng.normal(45, 15, size=n).round().astype(int), 18, 84)
    genders = rng.choice(["男性", "女性"], size=n, p=[0.48, 0.52])

    rows = []
    for i in range(n):
        pref, city, zipcode, _, _ = CITIES[city_idx[i]]
        age = int(ages[i])
        gender = genders[i]
        # 生年月日（基準日から逆算。月日はランダム）
        birth = date(REFERENCE_DATE.year - age, 1, 1) + timedelta(days=int(rng.integers(0, 365)))
        surname = SURNAMES[rng.integers(0, len(SURNAMES))]
        given = (GIVEN_MALE if gender == "男性" else GIVEN_FEMALE)[rng.integers(0, 10)]
        member_id = f"M{i + 1:06d}"
        rows.append(
            {
                "会員ID": member_id,
                "氏名": f"{surname} {given}",
                "生年月日": birth.isoformat(),
                "性別": gender,
                "郵便番号": zipcode,
                "住所": f"{pref}{city}{rng.integers(1, 6)}丁目{rng.integers(1, 30)}-{rng.integers(1, 20)}",
                "携帯電話番号": f"0{rng.choice([80, 90])}-{rng.integers(1000, 9999)}-{rng.integers(1000, 9999)}",
                "電子メールアドレス": f"{member_id.lower()}@example.com",
                "クレジットカード番号": f"4{rng.integers(0, 10**15):015d}",
            }
        )
    return pd.DataFrame(rows)


def generate_purchases(rng: np.random.Generator, customers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    pid = 0
    start = REFERENCE_DATE - timedelta(days=365)
    for _, cust in customers.iterrows():
        age = REFERENCE_DATE.year - int(cust["生年月日"][:4])
        weights = _category_weights(_age_to_decade_index(age))
        weights = weights / weights.sum()
        pref = cust["住所"][:3]
        # 地域×購入金額: 東京はやや高単価（独自設定）
        region_factor = 1.15 if pref == "東京都" else (1.05 if pref == "神奈川" else 1.0)
        for _ in range(int(rng.poisson(5) + 1)):  # 1件以上
            pid += 1
            category = CATEGORIES[rng.choice(len(CATEGORIES), p=weights)]
            qty = int(rng.integers(1, 6))
            unit = BASE_PRICE[category] * rng.normal(1.0, 0.2) * region_factor
            amount = int(max(unit, 100)) * qty
            pdate = start + timedelta(days=int(rng.integers(0, 365)))
            rows.append(
                {
                    "購買ID": f"P{pid:07d}",
                    "会員ID": cust["会員ID"],
                    "購入年月日": pdate.isoformat(),
                    "購入品目": category,
                    "購入数量": qty,
                    "購入金額": amount,
                }
            )
    return pd.DataFrame(rows)


def generate_web_access(rng: np.random.Generator, customers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    aid = 0
    start = REFERENCE_DATE - timedelta(days=365)
    for _, cust in customers.iterrows():
        age = REFERENCE_DATE.year - int(cust["生年月日"][:4])
        weights = _category_weights(_age_to_decade_index(age))
        weights = weights / weights.sum()
        # Cookie ID は顧客の端末に紐づく想定（1顧客1〜2個）
        cookies = [rng.bytes(8).hex() for _ in range(int(rng.integers(1, 3)))]
        for _ in range(int(rng.poisson(9) + 1)):
            aid += 1
            category = CATEGORIES[rng.choice(len(CATEGORIES), p=weights)]
            adate = start + timedelta(days=int(rng.integers(0, 365)))
            rows.append(
                {
                    "アクセスID": f"A{aid:08d}",
                    "会員ID": cust["会員ID"],
                    "Cookie_ID": cookies[rng.integers(0, len(cookies))],
                    "アクセス日時": f"{adate.isoformat()}T{rng.integers(0, 24):02d}:{rng.integers(0, 60):02d}:00",
                    "閲覧カテゴリ": category,
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    rng = np.random.default_rng(SEED)
    customers = generate_customers(rng)
    purchases = generate_purchases(rng, customers)
    web_access = generate_web_access(rng, customers)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    customers.to_csv(OUT_DIR / "customers.csv", index=False, encoding="utf-8")
    purchases.to_csv(OUT_DIR / "purchases.csv", index=False, encoding="utf-8")
    web_access.to_csv(OUT_DIR / "web_access.csv", index=False, encoding="utf-8")

    print(f"customers : {len(customers):>6} rows -> {OUT_DIR / 'customers.csv'}")
    print(f"purchases : {len(purchases):>6} rows -> {OUT_DIR / 'purchases.csv'}")
    print(f"web_access: {len(web_access):>6} rows -> {OUT_DIR / 'web_access.csv'}")


if __name__ == "__main__":
    main()
