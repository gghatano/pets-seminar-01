"""case01（仮名加工情報）ダミーデータ生成スクリプト。

ステータス: 未実装（プレースホルダ）

方針（spec.md 第8・15節）:
- 生成仕様は docs/case01_pseudonymized/02_dummy_data_spec.md を正本とする。
- 乱数 seed を固定し、同一データを再生成可能にする。
- テーブル定義書・想定件数・主キー/外部キー制約・設計した分布と整合させる。
- 生成結果を data/case01_pseudonymized/raw/ に保存する。
- 原則として Python 標準ライブラリ・pandas・numpy を使用する。

実装時は .claude/skills/ の合成データ生成パイプライン（synthesize）を活用できる。
"""

from __future__ import annotations

SEED = 20260717


def main() -> None:
    raise NotImplementedError("docs/case01_pseudonymized/02_dummy_data_spec.md 確定後に実装する。")


if __name__ == "__main__":
    main()
