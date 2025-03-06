"""Search result processing and memory management module."""
import re
import json

def add_knowledge_item(memory, text, source):
    """
    Adds a new piece of knowledge to the memory if it is not already present.

    Args:
        memory (dict): The in-memory knowledge base, with key "knowledge".
        text (str): The knowledge content (e.g., a snippet or excerpt) to add.
        source (str): The source identifier (e.g., URL) of the knowledge.

    Returns:
        bool: True if the knowledge item was added, False if it was a duplicate.
    """
    # Check for duplicates based on text equality.
    for item in memory.get("knowledge", []):
        if item["text"].strip() == text.strip():
            return False
    memory.setdefault("knowledge", []).append({"source": source, "text": text})
    return True

def process_results(results, memory):
    """
    Processes the search results and updates the in-memory knowledge base.

    Args:
        results (list): A list of search result entries. Each entry is expected to be a tuple 
                        (title, url, snippet) containing the title, URL, and a brief snippet.
        memory (dict): The current in-memory knowledge state.

    Returns:
        dict: The updated memory after incorporating new knowledge from the search results.

    Role:
        This function extracts relevant snippets from search results, filters out entries 
        that are too short or redundant, and adds them to the memory as new knowledge items.
        It avoids adding results from URLs that have already been visited.
    """
    added_results_to_memory = 0

    for result in results:
        # Expect each result as a tuple: (title, url, snippet)
        if not isinstance(result, (list, tuple)) or len(result) < 3:
            continue
        title, url, snippet = result[0], result[1], result[2]
        # Skip if snippet is missing or too short.
        if not snippet or len(snippet) < 30:
            continue
        # If the URL has been visited (i.e. crawled) already, skip adding its snippet.
        if url in memory.get("visited_urls", set()):
            continue
        # Add the snippet to memory as a knowledge item only if the url hasn't been visited yet and if we didn't add more than 3 items during this iteration
        if added_results_to_memory < 3 and url not in memory["visited_urls"]: 
            add_knowledge_item(memory, snippet, source=url)
            added_results_to_memory += 1
    return memory
