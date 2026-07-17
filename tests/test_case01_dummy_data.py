"""case01 ダミーデータ生成の自動テスト（プレースホルダ）。

spec.md 第15節に基づき、生成データが以下を満たすことを確認する:
- 固定 seed による再現性
- テーブル定義書・想定件数との整合
- 主キー/外部キー制約の整合
- 設計したデータ分布の再現
"""

import pytest


@pytest.mark.skip(reason="ダミーデータ生成スクリプト実装後に有効化する")
def test_placeholder() -> None:
    pass
