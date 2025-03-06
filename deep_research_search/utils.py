"""Module used to query a LLM with OLlama or others solutions."""
from typing import Dict
import re
import json
from pydantic import BaseModel

import ollama

def query_ollama(prompt: str, model_name: str = "deepseek-r1:14b", output_format: BaseModel=None) -> Dict:

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
        response = ollama.generate(model=model_name, prompt=prompt)['response']
    else:
        response = ollama.generate(model=model_name, prompt=prompt, format=output_format.model_json_schema(),)['response']
    return response


#def extract_json_from_text(text: str) -> Dict:
    """
    Extract a json object from a string.

    Args:
        text (str): The prompt to be sent to the LLM.
        llama_server_url (str): The URL of the local OLlama server endpoint for generation.

    Returns:
        dict: A dictionary representing the LLM's response in JSON format, e.g.:
              {"action": "continue_search", "query": "additional question"} or {"action": "generate_answer"}.
    """
    # Remove the content between <think> and </think> and the '/n'
    #new_text = re.sub(r'<think>.*?</think>', '', text.replace('\n', ''), flags=re.DOTALL)

    # Extract the JSON object between { and }
    #match = re.search(r'(\{.*?\})', new_text, re.DOTALL)

    #if match:
        #json_str = match.group(1)  
        #try:
            #return json.loads(json_str)  # Convertir en dict Python
        #except json.JSONDecodeError as e:
            #raise TypeError("Error during the parsing of the JSON in the LLM response :", e)
            #return None 
    #else:
        #return None  
    

if __name__ == "__main__":
    from pydantic import BaseModel

    class Pet(BaseModel):
        name: str
        animal: str
        age: int
        color: str | None
        favorite_toy: str | None
    
    class PetList(BaseModel):
        pets: list[Pet]

    response = ollama.generate(
        prompt="I have one pet. A cat named Luna who is 5 years old and loves playing with yarn. She has grey fur.",
        model='deepseek-r1:1.5b',
        format=PetList.model_json_schema(),
    )
    print(response.response)
