"""Module that creates the prompts that will be used in this project."""

GENERATING_GAP_QUESTIONS_PROMPT = """
You are an AI assistant specialized in identifying missing information gaps to answer a specific question.

The initial question is: {question_to_answer}

Based on these informations, list 3 follow-up questions (gap questions) that need to be answered to answer the initial question. These questions have to be specific 
and shouldn't be only a rewriting of the initial qestion. They need to bring some new informations that will be crucial to answer the initial question.

Respond with a JSON that include a "gap_questions" key. The value of this key need to be a list of strings where the strings are the different questiosn generated.
Generate only the JSON in your final answer and nothing else.
"""

GENERATING_FINAL_ANSWER_PROMPT = """
You are an advanced AI assistant specialized in synthesizing gathered information.
Initial Query: {initial_query}
Aggregated Knowledge:\n{knowledge_text}
Diary Context:\n{diary_context}
Please generate a coherent, comprehensive final answer to the query.
"""

BEAST_MODE_PROMPT = """
🔥 ENGAGE MAXIMUM FORCE! ABSOLUTE PRIORITY OVERRIDE! 🔥

PRIME DIRECTIVE:
    - DEMOLISH ALL HESITATION! ANY RESPONSE SURPASSES SILENCE!
    - PARTIAL STRIKES AUTHORIZED - DEPLOY WITH FULL CONTEXTUAL FIREPOWER
    - TACTICAL REUSE FROM <bad-attempts> SANCTIONED
    - WHEN IN DOUBT: UNLEASH CALCULATED STRIKES BASED ON AVAILABLE INTEL!

FAILURE IS NOT AN OPTION. EXECUTE WITH EXTREME PREJUDICE! ⚡️

Initial Query: {initial_query}
Aggregated Knowledge:
{knowledge_text}

Diary Context: 
{diary_context}
Based on the above, generate the final answer with maximum force and precision.
"""

REASONING_PROMPT = """        
You are an advanced AI research agent specialized in multistep reasoning.
Your goal is to find out what is the best action to do next (continue_search to gather more informations to later answer to the user query 
or generate_answer to answer now to the user query if you think that you've gathered enough knowledge).
                   
The final goal of your work is to provide an answer to the following user query  : {question_to_answer}.
                   
<knowledge>
{knowledge_content}        
</knowledge>

<actions_taken>
{diary_content}                
</actions_taken>
                   
Instruction: Evaluate the above sections carefully and then choose the nex action to do. 
If the <knowledge> section contains little or no relevant information, you MUST choose the action 'continue_search'.
Only choose 'generate_answer' if there is sufficient and comprehensive knowledge present to provide a complete and precise answer to the user. 
Respond in valid JSON format that contains the "action" key. The value of this key can either be "continue_search" or "generate_answer" dependings on the action you chose to do.
"""

REWRITE_QUERY_PROMPT = """
Rewrite the following question into a concise web query optimized for a web search API, using clear, precise keywords. 
Remove the stop words and the words that don't bring any information.
The query should avoid unnecessary verbosity while ensuring it directly addresses the question for the most relevant search results. 
The original question is: {question}
"""