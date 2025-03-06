"""Main DeepSearch algorithm loop coordination with memory and budget management."""
import deep_research_search.search as search
import deep_research_search.read as read 
import deep_research_search.reason as reason
import deep_research_search.generate_answer as generate_answer
from deep_research_search.find_gap_questions import find_gap_questions

from deep_research_search.logger import logger

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

def deep_search(initial_query: str, token_budget: int=10000, max_bad_attempts: int=3, max_gap_questions: int=3):
    """
    Executes the DeepSearch algorithm loop.

    Args:
        initial_query (str): The initial query or question provided by the user.
        token_budget (int): Maximum allowed tokens for the DeepSearch execution.
        max_bad_attempts (int): Maximum allowed failed attempts before forcing beast mode.

    Returns:
        None

    Role:
        This function manages the main loop of the DeepSearch algorithm. It maintains an in-memory state,
        including a knowledge base, a diary of past actions, and a queue of gap questions. It alternates between
        the search, read, and reason steps. The reasoning module returns one of two actions: "generate_answer" 
        or "continue_search". When the token budget or the maximum number of failed attempts is reached, the system
        forces answer generation in "BEAST MODE".
    """
    # Initialize in-memory state.
    memory = {
        "knowledge": [],       # List of gathered knowledge items.
        "diaryContext": [],    # List of diary entries tracking actions and evaluations.
        "actionsHistory": [],   # Optionally, history of actions taken.
        "visited_urls": set(),     # Set of URLs that have been fully crawled/processed.
        "processed_queries": [],  # List of queries that have been processed
        "initial_query": initial_query
    }
    gaps = [initial_query]  # Queue of gap questions that need further investigation.
    gap_questions_count = 0 # Count the number of gap questions generated.
    token_usage = 0
    bad_attempts = 0
    step = 0
    total_step = 0

    # Identify gap questions from the updated memory.
    logger.debug(f"Find gap questions for the following question: {initial_query}")
    new_gaps = find_gap_questions(memory=memory, question_to_answer=initial_query) 
    new_added_gaps_count = 0
    if new_gaps:
        for new_gap in new_gaps:
            if gap_questions_count < max_gap_questions:
                gaps.append(new_gap)
                gap_questions_count += 1
                new_added_gaps_count += 1
            else:
                break
    add_to_diary(memory["diaryContext"], step, "gap_detection", initial_query,
                        f"Identified {new_added_gaps_count} new gap questions.")
            
    token_usage += 50  # Simulate token usage for the read step.

    # Main DeepSearch loop.
    while token_usage < token_budget and bad_attempts <= max_bad_attempts:
        step += 1
        total_step += 1

        # Select the current gap question and search the required knowledge to answer it.
        for current_question in gaps:
            next_action = "continue_search"

            if token_usage >= token_budget * 0.9 or bad_attempts >= max_bad_attempts: # Check if we are close to the budget or have too many failures.
                next_action = "generate_answer_immediately"
                logger.info(f"Generation of the answer with the beast mode because of the number of generated tokens is too high ({token_usage} tokens generated).")
                add_to_diary(memory["diaryContext"], step, "beast_mode", initial_query,
                            "Budget threshold reached.")
                final_answer = generate_answer.generate_answer(memory=memory, mode='beast_mode') # Generate immediately the final answer with the actual state (that's what's called beast_mode)
                return None
            else:
                # Decide the next action based on the current memory state.
                logger.debug(f"Reasoning to decide the next action for the following question: {current_question}")
                next_action = reason.decide_next_action(memory)
                logger.debug(f"Here is the chosen action: {next_action}")

            while next_action not in ["generate_answer", "continue_search"]: # Unrecognized action: count as a failed attempt.
                logger.debug(f"The next action chosen by the LLM for the \"{current_question}\" is not valid.")
                if bad_attempts == max_bad_attempts: # Too much bad attempts so we have to aswer immediately
                    next_action = "generate_answer_immediately"
                    logger.info(f"Generation of the answer with the beast mode after {max_bad_attempts} failed attempts.")
                    add_to_diary(memory["diaryContext"], step, "beast_mode", initial_query,
                                "Failure threshold reached.")
                    final_answer = generate_answer.generate_answer(memory=memory, mode='beast_mode') # Generate immediately the final answer with the actual state (that's what's called beast_mode)
                    return None
                else:
                    bad_attempts += 1
                    logger.debug(f"Reasoning to decide the next action for the following question: {current_question}")
                    add_to_diary(memory["diaryContext"], step, "error", current_question,
                                "Unknown action encountered.")
                    next_action = reason.decide_next_action(memory)
                    logger.debug(f"Here is the chosen action: {next_action}")

            if next_action == "generate_answer": # The actual gap question doesn't need any additional informations to be answered so we can focus onto the next one.
                pass

            elif next_action == "continue_search": # The actual gap question need more additional informations to be answered so we use internet search.
                # Perform the search action.
                logger.debug(f"Searching additional informations for the following question: {current_question}")
                results = search.search_web(current_question, search_history=memory['processed_queries'])
                token_usage += 100  # Simulate token usage for the search step.
                add_to_diary(memory["diaryContext"], step, "search", current_question,
                            f"Retrieved {len(results)} results.")

                # Process search results to update the knowledge memory.
                memory = read.process_results(results, memory)
                add_to_diary(memory["diaryContext"], step, "read", current_question,
                            "Processed search results and updated memory.")
            else:
                pass
                
        logger.info(f"Generation of the answer after having used {token_usage} tokens and failed {bad_attempts} times during the search and reasonning processus.")
        final_answer = generate_answer.generate_answer(memory=memory, mode='normal_generation')

        return None
