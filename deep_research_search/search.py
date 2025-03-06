"""Web search management module for DeepSearch."""
import re
from urllib.parse import urlsplit, urlunsplit

import requests
from duckduckgo_search import DDGS

# REVOIR UTILITE DE crawl_urls ET OU L UTILISER


def search_web(query, search_history):
    """
    Perform a web search for the given query (if not searched before) using DuckDuckGo.
    
    Args:
        query (str): The search query string.
        search_history (list): List of queries that have been searched already (to avoid duplicates).
    
    Returns:
        list: A list of search result entries. Each entry is a tuple (title, url, snippet).
              Returns an empty list if the query was already searched.
    """
    # Check if query has already been searched to avoid duplicate searches
    if query in search_history:
        print(f"Query '{query}' already searched. Skipping duplicate search.")
        return []
    
    # Simple query rewrite: optimize wording for web search (remove common stop words)
    # Remove punctuation and split into words
    query_clean = re.sub(r'[^\w\s]', ' ', query)
    words = query_clean.lower().split()
    # Define a basic set of stop words in English and French to remove from query
    stop_words = {"the", "is", "of", "to", "and", "a", "an",
                  "le", "la", "les", "de", "des", "du", "et",
                  "que", "qui", "quoi", "où", "comment", "pourquoi",
                  "what", "who", "where", "when", "how", "why"}
    # Filter out stop words
    keywords = [w for w in words if w not in stop_words]
    rewritten_query = " ".join(keywords) if keywords else query
    
    results = []
    
    # Search with DuckDuckGo search and get up to 10 results 
    with DDGS() as ddgs:
        for result in ddgs.text(keywords=rewritten_query, max_results=10):
                # Each result is a dictionary with keys like 'title', 'href', 'body'
                title = result.get("title") or ""
                url = result.get("href") or result.get("url") or ""
                snippet = result.get("body") or result.get("snippet") or ""
                results.append((title, url, snippet))
    
    # Add the original query to search history to prevent future duplicates
    search_history.append(query)
    return results


#def crawl_urls(urls, memory):
    """
    Crawl the given URLs using the Jina Reader API and store content snippets in memory.
    
    Args:
        urls (list): A list of webpage URLs to crawl for content.
        memory (dict): A dictionary acting as memory storage for crawled content. 
                       Already visited URLs are used as keys to avoid re-crawling.
    
    Returns:
        None: The function updates the memory dict in place with new content excerpts.
    """
    """count = 0  # Number of URLs crawled
    for url in urls:
        if count >= 3:
            break  # limit to 3 URLs per query
        
        # Normalize URL (lowercase domain, remove fragment, remove trailing slash)
        parsed = urlsplit(url)
        norm_netloc = parsed.netloc.lower()
        norm_path = parsed.path.rstrip('/')  # remove trailing slash from path
        norm_parsed = parsed._replace(netloc=norm_netloc, path=norm_path, fragment="")
        norm_url = urlunsplit(norm_parsed)
        
        # Skip if this URL (normalized) was already visited
        if norm_url in memory:
            continue
        
        # Use Jina Reader API to get main content of the page
        try:
            response = requests.get(f"https://r.jina.ai/{norm_url}", timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to crawl {url}: {e}")
            continue
        
        content_text = response.text
        # Extract an excerpt (for example, first 500 characters) for memory storage
        excerpt = content_text[:500]
        memory[norm_url] = excerpt
        count += 1"""


if __name__ == "__main__":
    search_web("Who is Lionel Messi", [])
