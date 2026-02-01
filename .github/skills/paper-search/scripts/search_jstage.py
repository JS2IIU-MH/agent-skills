import argparse
import json
import requests
import xml.etree.ElementTree as ET
import datetime

# J-STAGE OpenSearch API Endpoint
# Documentation reference: https://www.jstage.jst.go.jp/static/pages/JstageAPI_en.html
API_URL = "http://api.jstage.jst.go.jp/searchapi/do"

def search_jstage(query, max_results=10):
    """
    Search J-STAGE for papers matching the query.
    
    Args:
        query (str): Search query string (maps to full text search).
        max_results (int): Maximum number of results to return.
        
    Returns:
        list: A list of dictionaries containing paper details.
    """
    
    # Parameters for J-STAGE API
    # service=3 is the standard OpenSearch service ID for J-STAGE
    params = {
        "service": 3,
        "text": query,         # Full text search
        "count": max_results,  # Number of results
        "format": "atom"       # Atom format is standard for OpenSearch
    }

    try:
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"API Request failed: {str(e)}"}

    # Parse XML response
    try:
        # Use content to let ElementTree handle encoding from XML declaration
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        return {"error": f"Failed to parse XML response: {str(e)}"}

    # Define namespaces used in J-STAGE Atom feeds
    # Based on observation: items without prefix in default namespace are in Atom namespace
    namespaces = {
        'atom': 'http://www.w3.org/2005/Atom',
        'prism': 'http://prismstandard.org/namespaces/basic/2.0/',
        'opensearch': 'http://a9.com/-/spec/opensearch/1.1/'
    }

    results = []
    
    # Iterate over entries
    for entry in root.findall('atom:entry', namespaces):
        # Helper to get text safely with namespace handling
        def get_text(elem, xpath, ns=namespaces, default=""):
            node = elem.find(xpath, ns)
            return node.text if node is not None else default

        title = get_text(entry, 'atom:title')
        # Fallback to article_title/ja or en if atom:title is empty or CDATA issues
        if not title:
             title = get_text(entry, 'atom:article_title/atom:ja') or get_text(entry, 'atom:article_title/atom:en')

        summary = get_text(entry, 'atom:summary')
        if not summary:
            summary = get_text(entry, 'atom:abstract/atom:ja') or get_text(entry, 'atom:abstract/atom:en')

        url = ""
        link_node = entry.find('atom:link[@rel="alternate"]', namespaces)
        if link_node is not None:
             url = link_node.get('href')
        else:
             # Try link without rel (implicit alternate)
             # XPath limitation: cannot easily check "no attribute" in standard ElementTree easily in one go
             # so iterate
             for link in entry.findall('atom:link', namespaces):
                 if 'rel' not in link.attrib or link.get('rel') == 'alternate':
                     url = link.get('href')
                     break
        
        pdf_url = None
        for link in entry.findall('atom:link', namespaces):
            if link.get('type') == 'application/pdf':
                pdf_url = link.get('href')
                break
        
        # Authors: J-STAGE structure is <author><ja><name>...</name></ja></author>
        # They seem to inherit the Atom namespace
        authors = []
        for author in entry.findall('atom:author', namespaces):
            name = get_text(author, 'atom:ja/atom:name') or get_text(author, 'atom:en/atom:name')
            # Fallback: check direct name if structure varies
            if not name: 
                 name = get_text(author, 'atom:name')
            
            if name:
                authors.append(name)

        # Dates
        # J-STAGE uses <pubyear> (in Atom namespace)
        year_str = get_text(entry, 'atom:pubyear')
        year = int(year_str) if year_str and year_str.isdigit() else None
        
        published_date = str(year) if year else ""
        # Try to find a fuller date if available (often not in J-STAGE search results)
        
        # Journal
        # <material_title><ja>...</ja><en>...</en></material_title>
        journal_ref = get_text(entry, 'atom:material_title/atom:ja') or get_text(entry, 'atom:material_title/atom:en')
        
        volume = get_text(entry, 'prism:volume')
        number = get_text(entry, 'prism:number')
        
        if volume and number:
            journal_ref = f"{journal_ref} Vol. {volume} No. {number}"
        elif volume:
            journal_ref = f"{journal_ref} Vol. {volume}"

        results.append({
            "title": title,
            "authors": authors,
            "year": year,
            "published_date": published_date,
            "summary": summary,
            "url": url,
            "pdf_url": pdf_url,
            "journal_ref": journal_ref
        })

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search J-STAGE for papers.")
    parser.add_argument("query", help="Search query string")
    parser.add_argument("--max-results", type=int, default=10, help="Max number of results")
    
    args = parser.parse_args()
    
    try:
        data = search_jstage(args.query, args.max_results)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        error = {"error": str(e)}
        print(json.dumps(error, indent=2))
