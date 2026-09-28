import json
from openai import OpenAI
from functions.call_function import available_functions
from functions.call_function import call_function

def call_agent(client, messages, args, user_prompt):
    for _ in range(50):
        response = client.chat.completions.create(
            model=args.model,
            messages=messages,
            tools=available_functions,
        )

        message = response.choices[0].message

        if args.verbose:
            print(f"\nUser prompt: {user_prompt}\nPrompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}")
            print(f"\nReasoning: {message.reasoning_content}\n====================================================================================================")

        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                result_message = call_function(tool_call, args.verbose)
                if result_message["content"] == "":
                    raise Exception("Error: No result from tool call")
                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        elif not message.content:
            raise Exception("Error: tool call limit exceeded")
        else:
            return message.content
