import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.call_function import available_functions
from functions.call_function import call_function

load_dotenv()
api_key=os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("API key not found")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--model", type=str, default="gemma-4-e4b", help="Model name")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

client = OpenAI(
    base_url="http://ai.bigdoh.org/api/v1",
    api_key=api_key,
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

response = client.chat.completions.create(
    model=args.model,
    messages=messages,
    tools=available_functions,
)

if args.verbose:
    print(f"\nUser prompt: {args.user_prompt}\nPrompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}\n")

message = response.choices[0].message

if message.tool_calls:
    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        result_message = call_function(tool_call, args.verbose)
        if result_message["content"] == "":
            raise Exception("Error: No result from tool call")
        if args.verbose:
            print(f"-> {result_message['content']}")
else:
    print(f"Response: \n{message.content}")
