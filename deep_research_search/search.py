"""Web search management module for DeepSearch."""
import json

from duckduckgo_search import DDGS
from exa_py import Exa

from deep_research_search.logger import logger
from deep_research_search.utils import query_ollama
from deep_research_search.output_formats import RewriteQueryGenerationOutputFormat
from deep_research_search.prompts import REWRITE_QUERY_PROMPT
from deep_research_search.config import global_config

def ddgs_search_web(query, search_history, num_results):
    """
    Perform a web search for the given query (if not searched before) using DuckDuckGo.
    
    Args:
        query (str): The search query string.
        search_history (list): List of queries that have been searched already (to avoid duplicates).
        num_results (int): The number of results of the web search.
    
    Returns:
        list: A list of search result entries. Each entry is a tuple (title, url, snippet).
              Returns an empty list if the query was already searched.
    """
    # Check if query has already been searched to avoid duplicate searches
    if query in search_history:
        logger.debug(f"Query '{query}' already searched. Skipping duplicate search.\n")
        return []
    
    # Query rewrite to maximize the effectivenes of the web search
    prompt = REWRITE_QUERY_PROMPT.format(question=query)
    rewritten_query = json.loads(query_ollama(prompt=prompt, output_format=RewriteQueryGenerationOutputFormat)).get("query", "")
    if not isinstance(rewritten_query, str) or len(rewritten_query) < 5:
        rewritten_query = json.loads(query_ollama(prompt=prompt, output_format=RewriteQueryGenerationOutputFormat)).get("query", "")
    else:
         pass
    logger.debug(f"Here is te rewritten query used for web search: {rewritten_query}\n")
    
    results = []
    
    # Search with DuckDuckGo search and get up to 10 results 
    with DDGS() as ddgs:
        for result in ddgs.text(keywords=rewritten_query, max_results=num_results):
                # Each result is a dictionary with keys like 'title', 'href', 'body'
                title = result.get("title") or ""
                url = result.get("href") or result.get("url") or ""
                snippet = result.get("body") or result.get("snippet") or ""
                results.append((title, url, snippet))
    
    # Add the original query to search history to prevent future duplicates
    search_history.append(query)
    return results

def exa_search_web(query, search_history, num_results):
    """
    Perform a web search for the given query (if not searched before) using Exa Search.
    
    Args:
        query (str): The search query string.
        search_history (list): List of queries that have been searched already (to avoid duplicates).
        num_results (int): The number of results of the web search.
    
    Returns:
        list: A list of search result entries. Each entry is a tuple (title, url, snippet).
              Returns an empty list if the query was already searched.
    """
    # Check if query has already been searched to avoid duplicate searches
    if query in search_history:
        logger.debug(f"Query '{query}' already searched. Skipping duplicate search.\n")
        return []
    
    # Query rewrite to maximize the effectivenes of the web search
    prompt = REWRITE_QUERY_PROMPT.format(question=query)
    rewritten_query = json.loads(query_ollama(prompt=prompt, output_format=RewriteQueryGenerationOutputFormat)).get("query", "")
    if not isinstance(rewritten_query, str) or len(rewritten_query) < 5:
        rewritten_query = json.loads(query_ollama(prompt=prompt, output_format=RewriteQueryGenerationOutputFormat)).get("query", "")
    else:
         pass
    logger.debug(f"Here is te rewritten query used for web search: {rewritten_query}\n")
    
    results = []

    # Search with ExaSearch and get up to 10 results 
    exa = Exa(api_key = global_config.exa_search_api_key.get_secret_value()) 
    for result in exa.search_and_contents(query, num_results = num_results, text = True).results:
        title = result.title or ""
        url = result.url or ""
        snippet = result.text or ""
        results.append((title, url, snippet))
    
    # Add the original query to search history to prevent future duplicates
    search_history.append(query)
    return results
