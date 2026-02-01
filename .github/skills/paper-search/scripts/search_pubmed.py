
import argparse
import json
from Bio import Entrez

def search_pubmed(query, max_results=10, email="example@example.com"):
    Entrez.email = email
    
    # Search for IDs
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)
        handle.close()
        
        id_list = record["IdList"]
        
        if not id_list:
            return []
            
        # Fetch details
        handle = Entrez.efetch(db="pubmed", id=id_list, rettype="medline", retmode="text")
        # We use medline format and parse somewhat manually or use 'xml' retmode
        # 'xml' is better for robust parsing
        handle.close()

        handle = Entrez.efetch(db="pubmed", id=id_list, retmode="xml")
        records = Entrez.read(handle)
        handle.close()
        
        results = []
        if 'PubmedArticle' in records:
            for article in records['PubmedArticle']:
                medline_citation = article['MedlineCitation']
                article_data = medline_citation['Article']
                
                title = article_data.get('ArticleTitle', 'No title')
                
                # Authors
                author_list = []
                if 'AuthorList' in article_data:
                    for a in article_data['AuthorList']:
                        if 'LastName' in a and 'ForeName' in a:
                            author_list.append(f"{a['LastName']} {a['ForeName']}")
                        elif 'LastName' in a:
                            author_list.append(a['LastName'])
                
                # Abstract
                abstract_text = ""
                if 'Abstract' in article_data and 'AbstractText' in article_data['Abstract']:
                    # AbstractText can be a list of strings or objects
                    abs_content = article_data['Abstract']['AbstractText']
                    if isinstance(abs_content, list):
                        abstract_text = " ".join([str(x) for x in abs_content])
                    else:
                        abstract_text = str(abs_content)
                
                # Year
                pub_date = article_data.get('Journal', {}).get('JournalIssue', {}).get('PubDate', {})
                year = pub_date.get('Year', '')
                
                # PMID for URL
                pmid = medline_citation['PMID']
                url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                
                results.append({
                    "title": title,
                    "authors": author_list,
                    "year": year,
                    "summary": abstract_text,
                    "url": url,
                    "journal": article_data.get('Journal', {}).get('Title', ''),
                    "source": "PubMed"
                })
                
        return results

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search PubMed for papers.")
    parser.add_argument("query", help="Search query string")
    parser.add_argument("--max-results", type=int, default=10, help="Max number of results")
    parser.add_argument("--email", default="tool@example.com", help="Email for NCBI Entrez")
    
    args = parser.parse_args()
    
    data = search_pubmed(args.query, args.max_results, args.email)
    print(json.dumps(data, indent=2, ensure_ascii=False))
