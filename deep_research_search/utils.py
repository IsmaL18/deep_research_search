"""Module used to query a LLM with OLlama or others solutions."""
from typing import Dict, Generator
import re
import sys
import json
from pydantic import BaseModel

import ollama

from deep_research_search.logger import logger
from deep_research_search.config import global_config

def query_ollama(prompt: str, model_name: str = global_config.llm_model_name, output_format: BaseModel = None, stream: bool = False) -> Dict:
    """
    Sends the prompt to the local OLlama server and retrieves the LLM's decision.

    Args:
        prompt (str): The prompt to be sent to the LLM.
        model_name (str): The name of the OLlama model to use.
        output_format (BaseModel, optional): The required format of the output.
        stream (bool, optional): If True, enables streaming output.

    Returns:
        dict: A dictionary representing the LLM's response in required JSON format (if not streaming).
              If streaming, the response is logged token by token in real time.

    Role:
        This function interfaces with the OLlama server. It sends the prompt, receives the LLM output, 
        and either returns it as JSON or streams it in real time.
    """
    
    request_params = {
        "model": model_name,
        "prompt": prompt,
        "stream": stream
    }
    
    if output_format is not None:
        request_params["format"] = output_format.model_json_schema()

    # Gestion du streaming
    if stream:
        response_generator: Generator = ollama.generate(**request_params)
        
        logger.info("Generation of the response\n")

        full_response = ""
        sys.stdout.flush()
        for chunk in response_generator:
            token = chunk.get("response", "")
            sys.stdout.write(token)  
            sys.stdout.flush()  
            full_response += token
        sys.stdout.flush()
        
        logger.info("Generation done ✅\n")
        return full_response  

    else:
        response = ollama.generate(**request_params)
        return response['response']
    
def add_to_diary(diary_context, step, action, question, result):
    """
    Adds an entry to the diary context.

    Args:
        diary_context (list): The current diary context list.
        step (int): The current step number.
        action (str): The action taken at this step.
        question (str): The question associated with the action.
        result (str): Details of what was done and the obtained results.

    Returns:
        None: The diary context is updated in place.
    """
    entry = (
        f"At step {step}, you took **{action}** action for question: \"{question}\"\n"
        f"Details: {result}\n"
    )
    diary_context.append(entry)