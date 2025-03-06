"""Decision-making module for the next action in DeepSearch."""
import json
from typing import Dict
import requests

from deep_research_search.utils import query_ollama
from deep_research_search.output_formats import ReasoningOutputFormat

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
    sections = []
    
    # System instruction.
    context = (
        "You are an advanced AI research agent specialized in multistep reasoning." 
        "Your goal is to find out what is the best action to do next (continue_search to gather more informations to later answer to the user query" 
        "or generate_answer to answer now to the user query if you think that you've gathered enough knowledge)." 
        f"The final goal of your work is to provide an answer to the following user query  : {memory['initial_query']}."
    )
    sections.append(context)
    
    # Knowledge section.
    knowledge = memory.get("knowledge", [])
    if knowledge:
        knowledge_texts = [item.get("text", "").strip() for item in knowledge if item.get("text", "").strip()]
        knowledge_content = "\n".join(knowledge_texts) if knowledge_texts else "No relevant knowledge gathered so far."
    else:
        knowledge_content = "No relevant knowledge gathered so far."
    
    sections.append("<knowledge>")
    sections.append(knowledge_content)
    sections.append("</knowledge>")
    
    # Diary context section.
    diary = memory.get("diaryContext", [])
    if diary:
        diary_content = "\n".join(diary)
        sections.append("<actions_taken>")
        sections.append(diary_content)
        sections.append("</actions_taken>")
    
    # Instruction section with explicit guidance.
    instruction = (
        "Instruction: Evaluate the above sections carefully and then choose the nex action to do. "
        "If the <knowledge> section contains little or no relevant information, you MUST choose the action 'continue_search'."
        "Only choose 'generate_answer' if there is sufficient and comprehensive knowledge present to provide a complete and precise answer to the user. "
        "Respond in valid JSON format that contains the \"action\" key. The value of this key can either be \"continue_search\" or \"generate_answer\" dependings on the action you chose to do."
    )
    sections.append(instruction)
    
    prompt = "\n\n".join(sections)
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