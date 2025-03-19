# Deep Research Search

This project provides an implementation of the Deep Search algorithm in Python, leveraging web search and LLM (Large Language Model) capabilities through Ollama. The algorithm follows the 'search-read-reason' pattern to systematically query, process, and interpret information.

## Prerequisites
Before starting, ensure you have:

### Ollama Setup

#### Install Ollama:
Visit [Ollama](https://ollama.com/) for installation instructions.

#### Pull LLM Model:
Example:
`ollama pull deepseek-r1:14b`

#### Run Ollama server:
`ollama serve`

### Web Search API
This project supports two web search APIs:
- [DuckDuckGo](https://duckduckgo.com/) (default) - No API key required but have some rate limits.
- [ExaSearch](https://exa.ai/search) - Requires an API key that you can create [here](https://dashboard.exa.ai/api-keys).

Configure your choice in the .env file (see .env.example).

### Python
Ensure you have Python installed on your machine.

### Poetry
Ensure you have [Poetry](https://python-poetry.org/) installed on your machine.

## Project Structure

### Key components:
- **deep_research_search/main.py**: Entry point of the project.
- **deep_research_search/deepsearch.py**: Implements the Deep Search algorithm logic.
- **deep_research_search/utils.py**: Utility functions used across modules.
- **deep_research_search/prompts.py**: Contains prompts for the Deep Search algorithm.
- **deep_research_search/read.py**: Implements the "Read" step of the algorithm.
- **deep_research_search/reason.py**: Implements the "Reason" step of the algorithm.
- **deep_research_search/search.py**: Implements the "Search" step of the algorithm.
- **deep_research_search/find_gap_questions.py**: Generates gap questions used by the Deep Search algorithm.
- **deep_research_search/output_formats.py**: Defines output formats for LLM responses.

## Environment Variables
Create a .env file based on .env.example:
```
LLM_PROVIDER="ollama"
LLM_MODEL_NAME="deepseek-r1:14b"
LOG_LEVEL="DEBUG"
WEB_SEARCH_ENGINE="ddg"
EXA_SEARCH_API_KEY="your_exasearch_api_key_here"
```

## How to Run
Ensure your environment is correctly set up as described in prerequisites. Then, run:
`poetry install`  
`poetry run python deep_research_search/main.py`  
The main function in main.py orchestrates the Deep Search algorithm execution.

## Logging
Logging is configured via the `LOG_LEVEL` environment variable, allowing debugging and tracing the execution flow.

Happy searching!