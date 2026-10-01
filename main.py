import os
import sys
import argparse
import json
import datetime
from agent import call_agent
from dotenv import load_dotenv
from openai import OpenAI
from config import *
from logger import agent_log

load_dotenv()
base_url = os.environ.get("OPENAI_BASE_URL")
if not base_url:
    raise RuntimeError("API URL not found")

api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("API key not found")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("-s", "--system", type=str, default=system_prompt, help="System prompt, defaults to value set in config file")
parser.add_argument("-m", "--model", type=str, default=model_name, help="Model name, defaults to value set in config file")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
parser.add_argument("-l", "--log", action="store_true", help="Enable logging")
args = parser.parse_args()

client = OpenAI(
    base_url=base_url,
    api_key=api_key,
)

def get_user_prompt() -> str:
    print("Enter prompt below (or /exit):")
    prompt = ""
    while prompt == "":
        prompt = str(input()).strip()
    return prompt

messages = [
    {"role": "system", "content": args.system},
]

while True:
    try:
        user_prompt = get_user_prompt()
        if user_prompt == "/exit":
            sys.exit()
        messages.append({"role": "user", "content": user_prompt})
        agent_turn = call_agent(client, messages, args, user_prompt)
        print(f"\nResponse:\n{agent_turn}")
        if args.log:
            agent_log(agent_turn, True)
    except Exception as e:
        print(f"Error: {e}")
