import os
import sys
import argparse
import json
from agent import call_agent
from dotenv import load_dotenv
from openai import OpenAI
from config import system_prompt


load_dotenv()
api_key=os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("API key not found")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("--system", type=str, default=system_prompt, help="System prompt")
parser.add_argument("--model", type=str, default="gemma-4-e4b", help="Model name")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

client = OpenAI(
    base_url="http://ai.bigdoh.org/api/v1",
    api_key=api_key,
)

def get_user_prompt() -> str:
    print("Enter prompt below:")
    return str(input())

messages = [
    {"role": "system", "content": args.system},
]

while True:
    try:
        user_prompt = get_user_prompt()
        if user_prompt == "/exit":
            sys.exit()
        messages.append({"role": "user", "content": user_prompt})
        print(f"\nResponse:\n{call_agent(client, messages, args, user_prompt)}")
    except Exception as e:
        sys.exit(e)
