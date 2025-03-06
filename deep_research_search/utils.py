"""Module used to query a LLM with OLlama or others solutions."""
from typing import Dict, Generator
import re
import sys
import json
from pydantic import BaseModel

import ollama

from deep_research_search.logger import logger
from deep_research_search.config import global_config

def query_ollama(prompt: str, model_name: str = global_config.llm_model_name, output_format: BaseModel=None, stream: bool=False) -> Dict:

    """
    Sends the prompt to the local OLlama server and retrieves the LLM's decision.

    Args:
        prompt (str): The prompt to be sent to the LLM.
        llama_server_url (str): The URL of the local OLlama server endpoint for generation.
        output_format (BaseModel): The required format of the output.

    Returns:
        dict: A dictionary representing the LLM's response in required JSON format.

    Role:
        This function is responsible for interfacing with the OLlama server. It sends the generated prompt,
        receives the LLM output, and returns the output as a JSON-like dictionary.
    """
    # Use OLlama's model to generate a response
    if output_format is None:
        response = ollama.generate(model=model_name, prompt=prompt, stream=stream)['response']
    else:
        response = ollama.generate(model=model_name, prompt=prompt, format=output_format.model_json_schema(), stream=stream)['response']
    return response


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
        response = ollama.generate(**request_params)['response']
        return response
    

if __name__ == "__main__":
    query_ollama(prompt="How many r in strawberry ?", stream=True)