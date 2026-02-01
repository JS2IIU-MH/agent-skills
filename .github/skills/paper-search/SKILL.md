---
name: paper-search
description: "Web上の論文を検索し、関連語句の抽出、要約、考察を行い、レポートを作成するスキル。Google Scholar, arXiv, PubMedなどを対象とする。"
license: Proprietary
---

# 論文検索・調査スキル (Paper Search)

## 概要

このスキルは、ユーザーが指定したキーワードやトピックに基づいて、関連する学術論文を検索・収集し、その内容を要約・考察してレポートを作成するためのものです。
対象となる主要な情報源は **Google Scholar**, **arXiv**, **PubMed** です。日本語および英語の論文を対象とします。

## ワークフロー

論文調査は以下の4つのステップで進めます。

1. **検索戦略の策定**: ユーザーの入力から適切なキーワード（日本語・英語）を選定する。
2. **論文検索**: 各プラットフォームで検索を実行し、候補となる論文をリストアップする。
3. **内容の抽出と考察**: タイトル、要約（Abstract）を読み、トピックとの関連性を評価・考察する。
4. **成果物の作成**: 指定された形式（Markdownレポート、CSVリスト）で出力する。

---

## ステップ詳細

### 1. 検索戦略の策定

*   ユーザーの要求からメインテーマを特定する。
*   検索用キーワードを日本語と英語の両方で用意する。
    *   例: 「生成AI」 -> "Generative AI", "LLM", "Large Language Models"
*   特定の年代や分野の指定があるか確認する。

### 2. 論文検索

検索には以下のツール・手法を使い分けること。

#### A. arXiv (スクリプト利用)

情報の速報性が高いコンピュータサイエンス、物理学などの分野に有効。
付属のスクリプト `scripts/search_arxiv.py` を使用する。

```bash
# 依存ライブラリのインストール (初回のみ)
pip install arxiv

# 検索の実行 (英語キーワード推奨)
python .github/skills/paper-search/scripts/search_arxiv.py "generative ai" --max-results 10
```

#### B. PubMed (スクリプト利用)

医学、生物学、ライフサイエンス分野に有効。
付属のスクリプト `scripts/search_pubmed.py` を使用する。

```bash
# 依存ライブラリのインストール (初回のみ)
pip install biopython

# 検索の実行
python .github/skills/paper-search/scripts/search_pubmed.py "cancer immunotherapy" --max-results 10
```

#### C. Google Scholar (search_web利用)

全分野を網羅するが、API制限が厳しいため、エージェントの標準ツール `search_web` を使用する。

*   検索クエリの例: `site:scholar.google.com "generative ai" 2024`
*   **注意**: 直接 `scholar.google.com` をスクレイピングするスクリプトはこれを使用せず、`search_web` ツールで得られた検索結果（スニペット機能）を活用するか、必要に応じて `browser_subagent` で内容を確認すること。

---

### 3. 内容の抽出と考察

集めた論文リスト（タイトル、著者、発行年、URL、要約）をもとに、以下の点を分析する。

*   **関連性**: ユーザーの関心事項にどれだけ合致しているか。
*   **主要な貢献**: その論文の新規性や発見は何か。
*   **トレンド**: 検索された論文群から読み取れる最近の傾向。

### 4. 成果物の作成

以下の2つのファイルを作成する。ファイル名はトピックと日付を含めること（例: `paper_report_genai_20240201.md`）。

#### A. 論文リスト (CSV)

以下のカラムを持つCSVファイルを作成する: `paper_list_YYYYMMDD.csv`
*   Title (タイトル)
*   Authors (著者)
*   Year (発行年)
*   Venue/Journal (掲載誌/会議)
*   URL (リンク)
*   Summary (要約 - 短いもの)
*   Relevance (関連度スコア 1-5など)

#### B. Markdownレポート

以下の構成でレポートを作成する: `report_YYYYMMDD.md`

```markdown
# [トピック] に関する論文調査レポート

## 概要
調査結果の全体的な要約。トレンドや特筆すべき発見。

## 主な論文の解説
特に重要性の高い3-5本の論文について詳細に解説。
### 1. [論文タイトル]
*   **著者/年**: ...
*   **概要**: ...
*   **考察**: なぜこの論文が重要か、ユーザーの課題にどう関わるか。

## 考察・まとめ
全体の調査を通じた知見。

## 参考文献リスト
(CSVの内容を簡潔にリスト化)
```

---

## 依存関係

スクリプト実行に必要なPythonパッケージ:
*   `arxiv`
*   `biopython` (PubMed用)
*   `pandas` (CSV処理用、任意)

```bash
pip install arxiv biopython pandas
```
