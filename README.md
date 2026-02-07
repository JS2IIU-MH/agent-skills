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
 - `.github/skills/generate-blog-article/`
	- `SKILL.md`
 - `.github/skills/tech-blog-writer/`
	- `SKILL.md`
- `.github/skills/pptx/`
	- `html2pptx.md`
	- `ooxml.md`
	- `SKILL.md` / `SKILL_org.md`
	- `LICENSE.txt`
	- `ooxml/schemas/`
	- スクリプト: `scripts/html2pptx.js`, `scripts/inventory.py`, `scripts/rearrange.py`, `scripts/replace.py`, `scripts/thumbnail.py`

## スキル一覧

| スキル名 | 何ができるか（要約） | 主な出力／成果物 | 主要依存・ツール |
|---|---:|---|---|
| `tech-blog-writer` | 中級者向けの技術系ブログ記事を構成から執筆まで行う。PyTorch中心の実装例と詳細解説を含む。 | 3000–5000字程度のMarkdown記事（コード例、数式、図解） | Python（PyTorch）、Markdown出力ルール、数式表記 |
| `generate-blog-article` | Web検索に基づくテックブログ記事の調査→アウトライン提示→ユーザー承認→本文生成を行うワークフロー。 | 承認済みアウトライン、最終Markdown記事（コード＋図解） | Web検索ツール、Markdown出力、matplotlib（図生成）、Mermaid |
| `presentation-research` | WEB調査を行い、調査ログ付きでビジネス向けプレゼン資料（.pptx）を作成する。要約・分析・提言を含む。 | 調査ログ（Markdown）、.pptx プレゼン資料、参考文献リスト | `web_search`/`web_fetch`、pptxgenjs / python-pptx、markitdown、LibreOffice（QA） |
| `pptx` | .pptx の作成・編集・解析（XMLレベルの操作含む）、テンプレート適用、スライドの入れ替え・置換ワークフローを提供。 | 生成/編集済み .pptx、テンプレート在庫（inventory）JSON、replacement JSON | `html2pptx.js`、`ooxml` スクリプト群（unpack/pack/validate）、`inventory.py`、`replace.py` |
| `paper-search` | Google Scholar/arXiv/PubMed 等で論文検索→抽出→要約・考察→レポート作成を行う。 | 論文リストCSV、Markdown調査レポート | `arxiv`、`biopython`（PubMed）、`pandas`、検索ツール（search_web） |
| `lecture-slides` | 与えられたテキスト／ファイル／URL から講演用スライドとスピーカーノートを生成。テンプレート適用対応。 | `slides.json`（構成）、出力 `.pptx`（スピーカーノート付き） | `python-pptx`、`scripts/generate_slides.py` |

## 利用方法（短）
- Python スクリプトは Python 3 を使用し、必要に応じて各 `requirements.txt` を参照して依存をインストールしてください。
- Node スクリプトは Node.js 環境で実行してください（例: `scripts/html2pptx.js`）。


