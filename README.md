# agent-skills

簡潔なリポジトリ概要と主要ファイル・スクリプト一覧。

## 概要
このリポジトリは複数の「スキル」関連ワークフロー（講義資料生成、論文検索、PPTX 操作など）の実装やメモをまとめたものです。

## 構成
- `.github/skills/lecture-slides/`
	- `SKILL.md`
	- `requirements.txt`
	- `scripts/generate_slides.py`
- `.github/skills/paper-search/`
	- `SKILL.md`
	- `scripts/search_arxiv.py`
	- `scripts/search_jstage.py`
	- `scripts/search_pubmed.py`
- `.github/skills/pptx/`
	- `html2pptx.md`
	- `ooxml.md`
	- `SKILL.md` / `SKILL_org.md`
	- `LICENSE.txt`
	- `ooxml/schemas/`
	- スクリプト: `scripts/html2pptx.js`, `scripts/inventory.py`, `scripts/rearrange.py`, `scripts/replace.py`, `scripts/thumbnail.py`

## 利用方法（短）
- Python スクリプトは Python 3 を使用し、必要に応じて各 `requirements.txt` を参照して依存をインストールしてください。
- Node スクリプトは Node.js 環境で実行してください（例: `scripts/html2pptx.js`）。

## 参照
- この README: README.md
