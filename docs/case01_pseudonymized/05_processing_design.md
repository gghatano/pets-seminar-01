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

[情報特性の評価](04_column_classification.md)（識別性・機微度・結合キー性）と、利用目的（地域 × 顧客層 × 商品関心の分析）から見た**分析上の必要性・必要粒度**を突き合わせ、**評価 → 方針**を1枚で決めます。色は加工の種類（緑＝置換/一般化・赤＝削除・無色＝加工なし）、**「加工の根拠」列**は加工する理由の区分です。

<p class="master-legend"><span class="lg"><span class="sw sw-chg"></span>置換・一般化</span><span class="lg"><span class="sw sw-del"></span>削除</span><span class="lg"><span class="sw sw-keep"></span>加工なし</span><span class="lg"><span class="sw sw-rule"></span>規則で必須</span><span class="lg"><span class="sw sw-vol"></span>自主的（予防的）</span></p>

<table class="master">
<thead><tr><th>項目</th><th>識別性</th><th>機微度</th><th>分析上の必要性</th><th>必要粒度</th><th>加工方針</th><th>加工の根拠</th><th>理由</th></tr></thead>
<tbody>
<tr><td>会員ID</td><td>低（単体）</td><td>低</td><td>結合に必要</td><td>―</td><td class="cell-chg">整理番号へ置換</td><td><span class="vol">自主的</span></td><td>個人単位の履歴をつなぐため置換。作成元との照合＝識別禁止義務のリスク低減</td></tr>
<tr class="is-required"><td>氏名</td><td>高（直接識別子）</td><td>中</td><td>不要</td><td>―</td><td class="cell-del">削除</td><td><span class="rule">規則で必須</span></td><td>特定の個人を識別できる記述</td></tr>
<tr><td>生年月日</td><td>準（組合せで高）</td><td>中</td><td>必要</td><td>10歳区切り</td><td class="cell-chg">年代へ一般化</td><td><span class="vol">自主的</span></td><td>詳細日付は不要。準識別子の組合せリスクを下げる予防的な一般化（解釈によっては不要とも）</td></tr>
<tr><td>性別</td><td>準（低）</td><td>低</td><td>必要</td><td>そのまま</td><td class="cell-keep">加工しない</td><td>―</td><td>生年月日・住所を加工済み</td></tr>
<tr><td>郵便番号</td><td>準（低）</td><td>低</td><td>不要</td><td>―</td><td class="cell-del">削除</td><td><span class="vol">自主的</span></td><td>加工後の住所で代替できるため不要</td></tr>
<tr><td>住所</td><td>準（組合せで高）</td><td>中</td><td>必要</td><td>市区町村</td><td class="cell-chg">市区町村へ一般化</td><td><span class="vol">自主的</span></td><td>準識別子リスク低減の予防的な一般化。商圏判定には市区町村で十分</td></tr>
<tr><td>携帯電話番号</td><td>高（本人到達性）</td><td>中</td><td>不要</td><td>―</td><td class="cell-del">削除</td><td><span class="vol">自主的</span></td><td>本人到達性・共用性を踏まえた予防的削除</td></tr>
<tr class="is-required"><td>電子メールアドレス</td><td>高（本人到達性）</td><td>中</td><td>不要</td><td>―</td><td class="cell-del">削除</td><td><span class="rule">規則で必須</span></td><td>本人到達性・共用性。氏名等を含み識別できる場合は削除対象</td></tr>
<tr class="is-required"><td>クレジットカード番号</td><td>高</td><td>高</td><td>不要</td><td>―</td><td class="cell-del">削除</td><td><span class="rule">規則で必須</span></td><td>不正利用で財産的被害のおそれ。<strong>分析に使いたくても削除が必須</strong></td></tr>
<tr><td>Cookie ID</td><td>中（本人到達性）</td><td>中</td><td>不要</td><td>―</td><td class="cell-del">削除</td><td><span class="vol">自主的</span></td><td>本人到達性。会員ID→整理番号を識別子に使うため不要</td></tr>
<tr><td>購入年月日・品目・数量・金額</td><td>低</td><td>低</td><td>必要</td><td>そのまま</td><td class="cell-keep">加工しない</td><td>―</td><td>購買動向分析に必要</td></tr>
<tr><td>アクセス日時・閲覧カテゴリ</td><td>低</td><td>低</td><td>必要</td><td>そのまま</td><td class="cell-keep">加工しない</td><td>―</td><td>閲覧→購入・反応分析に必要</td></tr>
</tbody>
</table>

??? note "加工の根拠：「規則で必須」と「自主的（予防的）」の違い"
    加工の要否は、**① 分析に必要か（設計判断）** と **② 加工の根拠** の掛け合わせで決まります。根拠は次の2種類があります。

    - **規則で必須（法令）**: 個人情報保護委員会規則（[個人情報の保護に関する法律施行規則](https://www.ppc.go.jp/personalinfo/legal/)）第31条＝仮名加工情報の作成基準。**クレジットカード番号は、たとえ分析に使いたくても、第31条第3号（財産的被害のおそれ）により削除が必須**。氏名など特定の個人を識別できる記述（第1号）も同様。
    - **自主的（予防的）**: 規則で必須とまでは言い切れないが、識別リスクを下げるために行う加工。**解釈によっては「そこまで不要」ともいえる**もの。たとえば**生年月日 → 年代の一般化**は、他の識別子を除いていれば必須とは限らないが、準識別子の組合せリスクを下げるために自主的に加工しています。

→ 具体的な Python 処理は [加工仕様](06_processing_spec.md)、加工後のスキーマは [加工後テーブル定義](07_table_definition_after.md)。
