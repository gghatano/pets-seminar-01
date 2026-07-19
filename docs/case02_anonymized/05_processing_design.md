# case02（匿名加工情報）: 加工の設計 — 4/7

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

> 各項目を「削除する／置き換える／粗くする／そのまま残す」のどれにするか、そしてその根拠。匿名加工では **施行規則第34条（匿名加工情報の作成基準）** の枠組みに沿って決めます。

## 加工方針の全体像

<div class="proc-head"><span>加工方針</span><span>加工の様子（加工前 → 加工後）</span></div>
<div class="proc">
<div class="proc-row"><div class="proc-policy is-chg">置換</div><div class="proc-flows">
<div class="proc-flow"><span class="proc-chip">会員ID</span><span class="proc-arrow">→</span><span class="proc-chip is-chg">仮ID</span></div>
</div></div>
<div class="proc-row"><div class="proc-policy is-chg">一般化<br>（丸め）</div><div class="proc-flows">
<div class="proc-flow"><span class="proc-chip">生年月日</span><span class="proc-arrow">→</span><span class="proc-chip is-chg">年代（7区分）</span></div>
<div class="proc-flow"><span class="proc-chip">住所</span><span class="proc-arrow">→</span><span class="proc-chip is-chg">市区郡</span></div>
<div class="proc-flow"><span class="proc-chip">利用日時</span><span class="proc-arrow">→</span><span class="proc-chip is-chg">分単位</span></div>
<div class="proc-flow"><span class="proc-chip">商品名（希少品）</span><span class="proc-arrow">→</span><span class="proc-chip is-chg">カテゴリ／削除</span></div>
<div class="proc-flow"><span class="proc-chip">数量（大量）</span><span class="proc-arrow">→</span><span class="proc-chip is-chg">上限で丸め</span></div>
<div class="proc-flow"><span class="proc-chip">金額（超高額）</span><span class="proc-arrow">→</span><span class="proc-chip is-chg">区分へ丸め</span></div>
</div></div>
<div class="proc-row"><div class="proc-policy is-del">削除</div><div class="proc-flows">
<div class="proc-flow"><span class="proc-chip">氏名</span><span class="proc-arrow">→</span><span class="proc-chip is-del">***</span></div>
<div class="proc-flow"><span class="proc-chip">電話番号</span><span class="proc-arrow">→</span><span class="proc-chip is-del">***</span></div>
<div class="proc-flow"><span class="proc-chip">店舗ID・取引ID・担当者ID・商品ID</span><span class="proc-arrow">→</span><span class="proc-chip is-del">***</span></div>
</div></div>
<div class="proc-row"><div class="proc-policy is-keep">加工なし</div><div class="proc-flows">
<div class="proc-flow"><span class="proc-chip">性別</span><span class="proc-arrow">→</span><span class="proc-chip is-keep">性別</span></div>
<div class="proc-flow"><span class="proc-chip">店舗名</span><span class="proc-arrow">→</span><span class="proc-chip is-keep">店舗名</span></div>
</div></div>
</div>

<small>匿名加工の目的は **再識別・復元を断つ**こと。個人を特定できる記述・連結符号・特異な記述を落とし、準識別子は「同じ属性の人が十分いる」粒度まで丸めます。性別・店舗名は他項目の加工で特定性が下がるため残します。</small>

!!! question "なぜ会員IDを「仮ID」に置き換えるの？（case01 の整理番号と何が違う？）"
    > レコードをつなぐIDが要るなら、case01 の整理番号と同じでは？——ここが仮名と匿名の分かれ目です。

    - **共通点**: 加工後も、顧客属性テーブルと購買履歴テーブルを **仮ID でつないで**「属性 × 購買傾向」を分析できます。
    - **違い**: 匿名加工では、元の会員IDと仮IDを**つなぎ直せる対応表を残しません**（施行規則34条3号＝連結符号の削除）。case01（仮名）は照合すれば元をたどれる余地を残し**識別禁止義務で運用**しますが、匿名は**そもそも元に戻せない**ようにします。
    - さらに、**特異な記述（34条4号）を消し、準識別子を丸める**ことで、「1人しかいない組合せ」から個人が浮かないようにします。

!!! tip "なぜ丸めるのか — 該当者の人数に応じて"
    生年月日・住所などの**準識別子を細かく残すと、「その組合せに該当する人が少ない」個人が特定されやすく**なります。レポートは、**該当者の人数・データセットの大きさ・人口の多寡に応じて丸めの度合を（可変に）判断**する、としています（年代7区分・市区郡・分単位）。該当者が少ない値は、**丸めをさらに粗くする・削除する**などで対応します。
    加えて、**超高齢・限定品・大量購入・超高額**のような**特異な記述**（34条4号）は、丸めても浮くため**削除・カテゴリ化・上限丸め**で対処します。

## 項目ごとの評価と加工方針（一覧）

色は加工の種類（緑＝置換/一般化・赤＝削除・無色＝加工なし）、**「加工の根拠」列**は施行規則第34条のどの号にあたるかです。

<p class="master-legend"><span class="lg"><span class="sw sw-chg"></span>置換・一般化</span><span class="lg"><span class="sw sw-del"></span>削除</span><span class="lg"><span class="sw sw-keep"></span>加工なし</span><span class="lg"><span class="sw sw-rule"></span>34条（1/3/4号）で必須</span><span class="lg"><span class="sw sw-vol"></span>34条5号の措置（水準は判断）</span></p>

<table class="master">
<thead><tr><th>項目</th><th>識別性</th><th>特異性</th><th>提供先の有用性</th><th>加工方針</th><th>加工の根拠</th><th>理由</th></tr></thead>
<tbody>
<tr class="is-required"><td>会員ID</td><td>低（単体）</td><td>―</td><td>連結に必要</td><td class="cell-chg">仮IDへ置換</td><td><span class="rule">34条3号</span></td><td>元データと連結できる符号を断つ（対応表は残さない）</td></tr>
<tr class="is-required"><td>氏名</td><td>高</td><td>―</td><td>不要</td><td class="cell-del">削除</td><td><span class="rule">34条1号</span></td><td>単体で個人を特定できる記述</td></tr>
<tr class="is-required"><td>電話番号</td><td>高</td><td>―</td><td>不要</td><td class="cell-del">削除</td><td><span class="rule">34条1号</span></td><td>本人到達性。照合で特定につながる</td></tr>
<tr><td>生年月日</td><td>中</td><td>超高齢は高</td><td>年代で有用</td><td class="cell-chg">年代7区分へ丸め</td><td><span class="vol">5号措置</span> <span class="rule">4号</span></td><td>準識別子を丸めて該当者を増やす。超高齢は特異値として対処</td></tr>
<tr><td>住所</td><td>中</td><td>―</td><td>エリアで有用</td><td class="cell-chg">市区郡へ丸め</td><td><span class="vol">5号措置</span></td><td>詳細エリアを落とし特定性を下げる</td></tr>
<tr><td>性別</td><td>低</td><td>―</td><td>有用</td><td class="cell-keep">加工しない</td><td>―</td><td>生年月日・住所の加工で対応、有用性が高い</td></tr>
<tr><td>利用日時</td><td>中</td><td>―</td><td>時間帯で有用</td><td class="cell-chg">分単位へ丸め</td><td><span class="vol">5号措置</span></td><td>店舗（位置）× 秒精度の照合を防ぐ</td></tr>
<tr><td>店舗名</td><td>中</td><td>―</td><td>有用</td><td class="cell-keep">加工しない</td><td>―</td><td>利用日時の加工で対応、有用性が高い</td></tr>
<tr><td>店舗ID・取引ID・担当者ID・商品ID</td><td>低</td><td>―</td><td>不要</td><td class="cell-del">削除</td><td><span class="vol">5号措置</span></td><td>提供先に不要。想定外の再識別リスクを下げる</td></tr>
<tr class="is-required"><td>商品名</td><td>低</td><td>希少品は高</td><td>カテゴリで有用</td><td class="cell-chg">希少品はカテゴリ化／削除</td><td><span class="rule">34条4号</span></td><td>限定品・超高級品は特異な記述</td></tr>
<tr class="is-required"><td>数量</td><td>低</td><td>大量は高</td><td>有用</td><td class="cell-chg">特異な数量は丸め／削除</td><td><span class="rule">34条4号</span></td><td>大量購入は特異な記述</td></tr>
<tr class="is-required"><td>金額</td><td>低</td><td>超高額は高</td><td>有用</td><td class="cell-chg">超高額は区分へ丸め</td><td><span class="rule">34条4号</span></td><td>超高額は特異な記述（トップコーディング）</td></tr>
</tbody>
</table>

??? note "匿名加工の根拠：施行規則34条（作成基準）の各号"
    匿名加工情報には、仮名加工情報と違って**一律の作成基準**があります（[施行規則第34条](https://www.ppc.go.jp/personalinfo/legal/)）。

    - **1号**: 特定の個人を識別できる記述等の削除（氏名・電話番号 等）
    - **2号**: 個人識別符号の削除（本事例では該当なし）
    - **3号**: 情報を相互に連結する符号の削除（会員ID → 仮ID）
    - **4号**: 特異な記述等の削除（超高齢・希少品・大量・超高額）
    - **5号**: データベースの性質を踏まえたその他の措置（丸めの水準は **該当者の人数・データセットの大きさ**に応じて判断）

    加えて、作成時には**匿名加工情報に含まれる情報の項目を公表**し、識別行為の禁止などの取り扱いを守ります（詳細は最新のガイドラインで確認）。

→ 具体的な Python 処理は [加工仕様](06_processing_spec.md)、加工後のスキーマは [加工後テーブル定義](07_table_definition_after.md)。
