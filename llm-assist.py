#!/usr/bin/python3
from openai import OpenAI
import os
import sys
import subprocess

GPT3_MODEL="gpt-3.5-turbo"
GPT3_CTX_WINDOW_LEN=16*1024
GPT3_MAX_COMPLETION_TOKENS=4096 # This is the max value you can put for max_tokens: the max size of a response, https://platform.openai.com/docs/models/gpt-4-turbo-and-gpt-4 and search for output tokens

GPT4_MODEL="gpt-4-turbo"
GPT4_CTX_WINDOW_LEN=128*1024
GPT4_MAX_COMPLETION_TOKENS=4096 

def send_openai_request(request):

    if os.environ.get('OPENAI_KEY') is None:
        print("Please set environment variable OPENAI_KEY")
        sys.exit(-1)

    client = OpenAI(api_key=os.environ.get('OPENAI_KEY'))

    completion = client.chat.completions.create(
            model=GPT3_MODEL,
            messages=[
                {"role": "system", "content": "You are a computer science expert"},
                {"role": "user", "content": request}], 
            max_tokens = GPT3_MAX_COMPLETION_TOKENS,
            temperature = 0.2,
            top_p = 0.1,
            seed = 1000) # keeping seed same is supposed to improve determinism

    response = completion.choices[0].message.content
    print(response)
    finish_reason = completion.choices[0].finish_reason
    while finish_reason == "length":
        continuation_prompt = "continue"
        completion = client.chat.completions.create(
            model=GPT3_MODEL,
            messages=[
                {"role": "system", "content": "You are a computer science expert"},
                {"role": "user", "content": continuation_prompt}], 
            max_tokens = GPT3_MAX_COMPLETION_TOKENS,
            temperature = 0.2,
            top_p = 0.1,
            seed = 1000) # keeping seed same is supposed to improve determinism
        response = completion.choices[0].message.content
        print(response)
        finish_reason = completion.choices[0].finish_reason


'''
This python script can be used from the command-line for OpenAI to help 
with various command-line specific tasks. By default it uses GPT-3. 

You need to set an environment variable OPENAI_KEY to contain your Open AI key.

Cool things / WATCH OUT
    1. Run llm-assist @ "message" 
    2. If you run llm-assist <bash command> it will try to execute it first.
    Then, it will collect any error message and send both the bash command and 
    error message to LLM to fix it. 
'''

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: llm-assist [optional]@ <MESSAGE>")
        sys.exit(0)

    # Try to check if you're asking for help about a bash command

    check_bash_cmd = "type " + sys.argv[1]
    result = subprocess.run(check_bash_cmd, shell = True, text = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if result.returncode != 0: 
        # Not a bash command
        send_openai_request(" ".join(sys.argv[1:]))
    else:
        # Execute the bash command and get the response
        cmd_result = subprocess.run(" ".join(sys.argv[1:]), shell = True, text = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

        send_openai_request(" ".join(sys.argv[1:]) + "\nError: " + cmd_result.stderr)
