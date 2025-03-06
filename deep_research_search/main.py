"""Main module for the DeepSearch engine CLI interface."""
import time

from deep_research_search.deepsearch import deep_search 
from deep_research_search.logger import logger

def main():
    """
    Parses command-line input and runs the DeepSearch main loop.

    Args:
        None: This function reads the user's query from the command line or input prompt.

    Returns:
        None: This function does not return a value but will output the final answer to the user.

    Role:
        This function serves as the entry point for the CLI. It retrieves the user's query,
        calls the DeepSearch algorithm (in the deepsearch module), and outputs the final answer.
    """
    logger.info("----- START OF THE SEARCH ENGINE -----\n")

    user_query = input("What is your query ? (type STOP to end the search engine) ")

    while user_query != "STOP":
        start_time = time.time()
        deep_search(user_query)
        end_time = time.time()

        execution_time = end_time - start_time
        logger.debug(f"Execution time: {execution_time:.6f} seconds")

        user_query = input("What is your query ? (type STOP to end the search engine) ")

    logger.info("----- END OF THE SEARCH ENGINE -----")

if __name__ == "__main__":
    main()
