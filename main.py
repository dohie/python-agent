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

sys.exit(call_agent(client, messages, args))
