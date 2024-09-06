This python script can be used from the command-line for OpenAI to help 
with various command-line specific tasks. By default it uses GPT-3. 

You need to set an environment variable OPENAI_KEY to contain your Open AI key.

Cool things / WATCH OUT
    1. Run llm-assist @ "message" 
    2. If you run llm-assist <bash command> it will try to execute it first.
    Then, it will collect any error message and send both the bash command and 
    error message to LLM to fix it. 

