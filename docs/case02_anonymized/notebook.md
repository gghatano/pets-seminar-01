# ② 実装（Google Colaboratory） — 6/7

<div class="wizard" markdown="1">
加工プロセス
{ .wizard-cap }

1. [全体概要](01_case_summary.md)
2. [データ概要理解](03_table_definition_before.md)
3. [データ詳細理解](04_column_classification.md)
4. [加工設計](05_processing_design.md)
5. [加工仕様](06_processing_spec.md)
6. **実装**
7. [結果確認](09_results.md)
</div>

加工設計（[① 検討](05_processing_design.md)）にもとづく **匿名加工処理の実行** は、Google Colaboratory 上の Notebook で行います。ブラウザだけで上から順に実行できます。

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gghatano/pets-seminar-01/blob/main/notebooks/case02_anonymized.ipynb){ .md-button }

## Notebook で行うこと

- GitHub 上の生成済みデータ（顧客属性・取引情報・購買履歴）の取得
- 匿名加工の段階実行（仮IDへ置換 → 直接識別子の削除 → 生年月日・住所・利用日時の丸め → 商品名のカテゴリ化 → 数量・金額の特異値処理 → 不要IDの削除）
- 各ステップで「何を・なぜ加工するか」「Python コード」「加工結果」を確認
- **匿名性の確認**（元IDに戻せない／特異な個人が浮かない＝準識別子の組合せの群の大きさ）と、**属性 × 購買傾向**の分析が加工後も成立することを確認

コードは、読めば何をしているか分かる粒度で書いています。実行結果は [③ 結果](09_results.md) にまとめています。
