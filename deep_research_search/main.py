"""Main module for the DeepSearch engine CLI interface."""
from deep_research_search.deepsearch import deep_search 

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
    user_query = input("What is your query ? ")
    final_answer = deep_search(user_query)
    print("Final Answer:")
    print(final_answer)

if __name__ == "__main__":
    main()
