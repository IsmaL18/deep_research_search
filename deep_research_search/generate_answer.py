"""Answer generation module for DeepSearch."""

import json

from deep_research_search.utils import query_ollama
from deep_research_search.prompts import GENERATING_FINAL_ANSWER_PROMPT, BEAST_MODE_PROMPT

def generate_answer(memory, mode):
    """
    Generates a final answer from the accumulated knowledge if possible.

    Args:
        memory (dict): The memory containing all information gathered that is relevant to answer the query.
                       Expected keys include "knowledge", "diaryContext", and "processed_queries".
        mode (str): The answer generation mode. It can be either 'normal_generation' or 'beast_mode'.

    Returns:
        str: The final answer to the original query, formulated in natural language.

    Role:
        This function composes the answer for the user by synthesizing the information stored in memory.
        It uses a language model (via a local OLlama LLM) to construct a coherent and comprehensive response.
        In "beast_mode", it uses an aggressive prompt to force maximum information retrieval.
    """
    # Extract the initial query, aggregated knowledge, and diary context from memory.
    initial_query = memory["initial_query"]
    knowledge_text = "\n".join([item["text"] for item in memory.get("knowledge", [])])
    diary_context = "\n".join(memory.get("diaryContext", []))
    
    # Compose the prompt based on the selected mode.
    if mode == "beast_mode":
        prompt = BEAST_MODE_PROMPT.format(initial_query=initial_query, knowledge_text=knowledge_text, diary_context=diary_context)
    elif mode == 'normal_generation':
        # Normal generation mode uses a standard, coherent prompt.
        prompt = GENERATING_FINAL_ANSWER_PROMPT.format(initial_query=initial_query, knowledge_text=knowledge_text, diary_context=diary_context)
    else:
        raise ValueError(f"{mode} isn't a valide mode to generate the final answer. Please use 'beast_mode' or 'normal_generation'.")

    try:
        # Query the local OLlama server using the composed prompt.
        response = query_ollama(prompt, stream=True)
        # Assume that the response returned is a string with the final answer.
        answer = response
    except Exception as e:
        answer = "Error generating answer: " + str(e)
    
    return answer
