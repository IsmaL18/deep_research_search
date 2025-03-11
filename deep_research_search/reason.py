"""Decision-making module for the next action in DeepSearch."""
import json
from typing import Dict
import requests

from deep_research_search.utils import query_ollama
from deep_research_search.output_formats import ReasoningOutputFormat
from deep_research_search.prompts import REASONING_PROMPT

def get_prompt(memory: Dict) -> str:
    """
    Constructs a prompt for the decision-making LLM to choose the next action.

    Args:
        memory (dict): A dictionary representing the current state of memory. It should include:
                       - "knowledge": a list of knowledge items (each with a "text" field),
                       - "diaryContext": a list of previous action entries.

    Returns:
        str: The constructed prompt instructing the LLM to decide the next action.
             It emphasizes that if the <knowledge> section contains little or no relevant content,
             the correct action is to "continue_search" rather than "generate_answer".
    """
    
    # Knowledge section.
    knowledge = memory.get("knowledge", [])
    if knowledge:
        knowledge_texts = [item.get("text", "").strip() for item in knowledge if item.get("text", "").strip()]
        knowledge_content = "\n".join(knowledge_texts) if knowledge_texts else "No relevant knowledge gathered so far."
    else:
        knowledge_content = "No relevant knowledge gathered so far."
    
    # Diary context section.
    diary = memory.get("diaryContext", [])
    if diary:
        diary_content = "\n".join(diary)
    else: 
        diary_content = "No actions taken so far."
    
    prompt = REASONING_PROMPT.format(question_to_answer=memory['initial_query'], knowledge_content=knowledge_content, diary_content=diary_content)
    
    return prompt


def decide_next_action(memory: Dict) -> str:
    """
    Decides what the DeepSearch algorithm should do next based on current knowledge.

    Args:
        memory (dict): The current memory containing all information gathered so far.

    Returns:
        str: A string describing the next action. The string can be either "generate_answer" or "continue_search"

    Role:
        This function uses the current state of knowledge to determine the next step in the search process.
        It creates a prompt using the memory, sends it to the local OLlama LLM, and parses the result to
        decide on the next action.
    """
    prompt = get_prompt(memory)

    try:
        response = query_ollama(prompt=prompt, output_format=ReasoningOutputFormat)
        # The response is expected to be a JSON array of strings.
        if isinstance(response, str):
            decision = json.loads(response).get("action", "continue_search")
        else:
            decision = "continue_search"
    except Exception as e:
        print(f"Error querying decision to do: {e}")
        decision = "continue_search"
    
    return decision