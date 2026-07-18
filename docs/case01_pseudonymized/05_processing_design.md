# case01（仮名加工情報）: 加工の設計 — 4/7

<div class="wizard" markdown="1">
加工プロセス
{ .wizard-cap }

1. [全体概要](01_case_summary.md)
2. [データ概要理解](03_table_definition_before.md)
3. [データ詳細理解](04_column_classification.md)
4. **加工設計**
5. [加工仕様](06_processing_spec.md)
6. [実装](notebook.md)
7. [結果確認](09_results.md)
</div>

> 各項目を「削除する／置き換える／粗くする／そのまま残す」のどれにするか、そしてその理由。判断は **識別性 × 機微度 × 利用目的上の必要性 × 必要粒度** の掛け合わせで決めます。

## 加工方針の全体像

<div class="proc-head"><span>加工方針</span><span>加工の様子（加工前 → 加工後）</span></div>
<div class="proc">
<div class="proc-row"><div class="proc-policy is-chg">置換</div><div class="proc-flows">
<div class="proc-flow"><span class="proc-chip">会員ID</span><span class="proc-arrow">→</span><span class="proc-chip is-chg">整理番号</span></div>
</div></div>
<div class="proc-row"><div class="proc-policy is-chg">一般化</div><div class="proc-flows">
<div class="proc-flow"><span class="proc-chip">生年月日</span><span class="proc-arrow">→</span><span class="proc-chip is-chg">年代</span></div>
<div class="proc-flow"><span class="proc-chip">住所</span><span class="proc-arrow">→</span><span class="proc-chip is-chg">市区町村</span></div>
</div></div>
<div class="proc-row"><div class="proc-policy is-del">削除</div><div class="proc-flows">
<div class="proc-flow"><span class="proc-chip">氏名</span><span class="proc-arrow">→</span><span class="proc-chip is-del">***</span></div>
<div class="proc-flow"><span class="proc-chip">郵便番号</span><span class="proc-arrow">→</span><span class="proc-chip is-del">***</span></div>
<div class="proc-flow"><span class="proc-chip">携帯電話番号</span><span class="proc-arrow">→</span><span class="proc-chip is-del">***</span></div>
<div class="proc-flow"><span class="proc-chip">電子メールアドレス</span><span class="proc-arrow">→</span><span class="proc-chip is-del">***</span></div>
<div class="proc-flow"><span class="proc-chip">クレジットカード番号</span><span class="proc-arrow">→</span><span class="proc-chip is-del">***</span></div>
<div class="proc-flow"><span class="proc-chip">Cookie ID</span><span class="proc-arrow">→</span><span class="proc-chip is-del">***</span></div>
</div></div>
<div class="proc-row"><div class="proc-policy is-keep">加工なし</div><div class="proc-flows">
<div class="proc-flow"><span class="proc-chip">性別</span><span class="proc-arrow">→</span><span class="proc-chip is-keep">性別</span></div>
<div class="proc-flow"><span class="proc-chip">購入年月日/品目/数量/金額</span><span class="proc-arrow">→</span><span class="proc-chip is-keep">購入年月日/品目/数量/金額</span></div>
<div class="proc-flow"><span class="proc-chip">アクセス履歴</span><span class="proc-arrow">→</span><span class="proc-chip is-keep">アクセス履歴</span></div>
</div></div>
</div>

<small>削除した項目は加工後データに残りません（表では <code>***</code>）。「加工なし」は前後で同じ＝分析に必要なので手を付けません。</small>

考え方はシンプルです。**分析に要らず特定につながる項目は削る。特定はしたくないが分析には要る項目は、必要な粗さまで一般化して残す。個人単位の履歴は整理番号でつなぐ。**

!!! question "なぜ会員IDを「削除」ではなく「整理番号に置換」するの？"
    > 整理番号は会員IDを振り直しただけ。しかも対応表を持っていれば元に戻せるのでは？——最初に引っかかるのはここです。

    ポイントは3つです。

    1. **完全には消せない**: 出店計画の分析には「同じ人の購買履歴をまとめて見る」ことが必要です。識別子を全部消すと 3 テーブルをつなげず、個人単位の分析ができません。だから **消すのではなく、意味のない通し番号に置き換えて履歴だけをつなぎます**。
    2. **対応表を切り離す**: 会員ID ↔ 整理番号の対応表は、**加工後データとは別に安全管理**します（削除情報等の安全管理措置）。加工後データ単体を見ても、そこから元の人物へはたどれません。
    3. **照合が禁止されている**: そもそも、加工後データを作成元の個人情報と突き合わせて本人を特定する行為は、**識別行為の禁止（識別禁止義務）** で禁じられています。

    この「① 履歴はつなぐ ／ ② 対応表は分離 ／ ③ 照合は禁止」がそろって、はじめて置換に意味が生まれます。

## 項目ごとの評価と加工方針（一覧）

[情報特性の評価](04_column_classification.md)（識別性・機微度・結合キー性）と、利用目的（地域 × 顧客層 × 商品関心の分析）から見た**分析上の必要性・必要粒度**を突き合わせ、**評価 → 方針**を1枚で決めます。

| 項目 | 識別性 | 機微度 | 結合キー | 分析上の必要性 | 必要粒度 | 加工方針 | 理由 |
|------|--------|--------|---------|----------------|----------|----------|------|
| 会員ID | 低（単体） | 低 | 高 | 履歴結合に必要 | ― | **整理番号へ置換** | 分析に不要＋識別禁止義務の抵触リスク低減 |
| 氏名 | 高（直接識別子） | 中 | ― | 不要 | ― | **削除** | 単体で個人を特定できる |
| 生年月日 | 準（組合せで高） | 中 | ― | 必要 | 10歳区切り | **年代へ一般化** | 詳細日付は不要、識別リスク低減 |
| 性別 | 準（低） | 低 | ― | 必要 | そのまま | **加工しない** | 生年月日・住所を加工済み |
| 郵便番号 | 準（低） | 低 | ― | 不要 | ― | **削除** | 加工後の住所で代替 |
| 住所 | 準（組合せで高） | 中 | ― | 必要 | 市区町村 | **市区町村へ一般化** | 商圏判定に十分な粒度 |
| 携帯電話番号 | 高（本人到達性） | 中 | ― | 不要 | ― | **削除** | 本人到達性・共用性 |
| 電子メールアドレス | 高（本人到達性） | 中 | ― | 不要 | ― | **削除** | 本人到達性・共用性 |
| クレジットカード番号 | 高 | 高 | ― | 不要 | ― | **削除** | 不正利用で財産的被害のおそれ |
| Cookie ID | 中（本人到達性） | 中 | 中 | 不要 | ― | **削除** | 本人到達性、会員IDを識別子に使用 |
| 購入年月日・品目・数量・金額 | 低 | 低 | ― | 必要 | そのまま | **加工しない** | 購買動向分析に必要 |
| アクセス日時・閲覧カテゴリ | 低 | 低 | ― | 必要 | そのまま | **加工しない** | 閲覧→購入・反応分析に必要 |

??? note "利用目的と必要粒度の対応（この表の「必要性・必要粒度」列の根拠）"
    利用目的: 地域ごとに、どの顧客層（年代・性別）がどの商品に関心を持つかを分析し、実店舗の出店計画を検討する。

    | 分析 | 必要な情報 | 必要な粒度 |
    |------|-----------|-----------|
    | 地域別の顧客層分析 | 居住地域 | 市区町村単位（商圏判定） |
    | 顧客層（年齢）別分析 | 年齢 | 10歳区切りの年代 |
    | 顧客層（性別）別分析 | 性別 | そのまま |
    | 商品関心の分析 | 購入品目・年月日・金額 | できる限り加工しない |
    | 閲覧→購入・反応の分析 | アクセス履歴 | そのまま |

→ 具体的な Python 処理は [加工仕様](06_processing_spec.md)、加工後のスキーマは [加工後テーブル定義](07_table_definition_after.md)。
