# CLAUDE.md

仮名加工情報・匿名加工情報の事例再現デモ（教材）。設計・実装の正本は [`docs/spec.md`](docs/spec.md)。
事例ごとの標準手順は skill [`case-study`](.claude/skills/case-study/SKILL.md) を使う。

## このプロジェクトの芯

- 中心的価値は「加工コード」ではなく **データ加工設計の思考プロセス**（spec §24）。
- 位置づけは「事務局レポートを**参考に**作成した、加工の考え方のデモ」。
  - 受講者向けの本文に出典区分ラベル（〔報告〕〔独自〕等）は **付けない**。出典は各ページ末に簡潔に示す。
  - デモ都合の設定（乱数 seed・分布・人工的傾向など）を受講者向け本文でわざわざ言及しない。開発者向けメモ（`02_dummy_data_spec.md` 等）に隔離する。
  - ただし **一次情報を確認せずに事例の事実（事例番号・データ項目・加工方法）を書かない**（正確性は維持）。
- 配信は3層（spec §25）: ① 検討=HTML（`docs/`）/ ② 実装=Colab（`notebooks/`）/ ③ 結果=HTML。
  - `docs/` を単一の正本とし、サイトはそこから生成。③の結果は②Notebookの実行出力から作る（ロジックを二重実装しない）。

## 開発コマンド（uv）

```bash
uv sync
uv run python src/dummy_data/case01_pseudonymized.py   # ダミーデータ生成（seed固定）
uv run pytest                                          # テスト
uv run mkdocs serve                                    # サイトをローカル確認
```

## CI ゲート（PR で全て実行。ローカルで先に通すこと）

```bash
uv run ruff check .
uv run ruff format --check .    # ← Notebook の code cell も対象。ipynb 編集後は下記に注意
uv run pytest -q
uv run mkdocs build --strict    # orphan/警告ゼロ
```

- **Notebook を編集したら** `uv run ruff format notebooks/xxx.ipynb` を実行し、**実行し直して壊れていないか確認**する。
- Python は `.python-version`（3.11）に固定。

## ダミーデータの原則

- 乱数 seed と基準日（`REFERENCE_DATE`）を固定し、再生成がバイト一致すること。
- 生成済み CSV は `data/<case>/raw/` にコミットし、Notebook はそれを取得（Colab の raw URL）。
- 一様乱数にせず、加工後分析が成立する人工傾向を持たせる（〔独自〕と明示）。作った傾向は `groupby` の簡易チェックで検証する。

## 環境のハマりどころ（このリポジトリで確認済み）

- **外向き通信はプロキシで多くのホストが 403**（`api.github.com` / `raw.githubusercontent.com` / `*.github.io` / `ppc.go.jp` など）。
  一次情報 PDF や raw データを**環境内から取得できない**。→ ユーザーにファイル提供を依頼する。`WebSearch` は通る。
- **一次情報 PDF（PPC）は AES 暗号化**。`Read` の PDF 描画は poppler 依存で不可。テキスト抽出は:
  ```bash
  uv run --with pypdf --with cryptography python -c "from pypdf import PdfReader; r=PdfReader('x.pdf'); r.decrypt(''); print(r.pages[0].extract_text())"
  ```
- **Colab は pandas 2 系**、ローカル uv はより新しい pandas に解決されうる。Notebook のコードは **pandas 2 系互換**で書く（生成済み CSV を配布するので生成器のバージョン差は結果に無影響）。
- **Notebook の実行検証**は raw URL がプロキシで届かないため、`DATA_BASE` をローカルの `data/<case>/raw` に置換したコピーを作り `jupyter nbconvert --to notebook --execute` で 0 エラー＋assert セル合格を確認する。

## ディレクトリ

- `docs/references/` 一次資料（原本PDFは出典明記のうえ格納可。ガイドラインは改正が入るのでURL参照）
- `docs/<case>/` 設計文書（00 要件整理 → 01 事例整理 → 02〜08）
- `src/dummy_data/` 生成器 / `data/<case>/raw/` 生成済みデータ / `notebooks/` Colab / `tests/`
- `.claude/skills/` 合成データ生成スキル（vendored）＋ `case-study`（事例再現の標準手順）
