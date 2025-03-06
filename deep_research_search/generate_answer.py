"""Answer generation module for DeepSearch."""

import json

from deep_research_search.utils import query_ollama

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
        prompt = (
            "<action-answer>\n"
            "🔥 ENGAGE MAXIMUM FORCE! ABSOLUTE PRIORITY OVERRIDE! 🔥\n\n"
            "PRIME DIRECTIVE:\n"
            "- DEMOLISH ALL HESITATION! ANY RESPONSE SURPASSES SILENCE!\n"
            "- PARTIAL STRIKES AUTHORIZED - DEPLOY WITH FULL CONTEXTUAL FIREPOWER\n"
            "- TACTICAL REUSE FROM <bad-attempts> SANCTIONED\n"
            "- WHEN IN DOUBT: UNLEASH CALCULATED STRIKES BASED ON AVAILABLE INTEL!\n\n"
            "FAILURE IS NOT AN OPTION. EXECUTE WITH EXTREME PREJUDICE! ⚡️\n"
            "</action-answer>\n\n"
            f"Initial Query: {initial_query}\n\n"
            f"Aggregated Knowledge:\n{knowledge_text}\n\n"
            f"Diary Context:\n{diary_context}\n\n"
            "Based on the above, generate the final answer with maximum force and precision."
        )
    elif mode == 'normal_generation':
        # Normal generation mode uses a standard, coherent prompt.
        prompt = (
            "You are an advanced AI assistant specialized in synthesizing gathered information.\n\n"
            f"Initial Query: {initial_query}\n\n"
            f"Aggregated Knowledge:\n{knowledge_text}\n\n"
            f"Diary Context:\n{diary_context}\n\n"
            "Please generate a coherent, comprehensive final answer to the query."
        )
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
