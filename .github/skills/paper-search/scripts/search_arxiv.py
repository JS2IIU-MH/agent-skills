
import argparse
import json
import arxiv

def search_arxiv(query, max_results=10):
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    results = []
    for r in client.results(search):
        # Authors list to string
        authors = [a.name for a in r.authors]
        
        results.append({
            "title": r.title,
            "authors": authors,
            "year": r.published.year,
            "published_date": r.published.strftime("%Y-%m-%d"),
            "summary": r.summary,
            "url": r.entry_id,
            "pdf_url": r.pdf_url,
            "journal_ref": r.journal_ref or "arXiv"
        })
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search arXiv for papers.")
    parser.add_argument("query", help="Search query string")
    parser.add_argument("--max-results", type=int, default=10, help="Max number of results")
    
    args = parser.parse_args()
    
    try:
        data = search_arxiv(args.query, args.max_results)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        error = {"error": str(e)}
        print(json.dumps(error, indent=2))
