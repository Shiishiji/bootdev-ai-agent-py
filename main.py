import os
import json
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("Missing OPENROUTER_API_KEY environment variable")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    prompt = args.user_prompt
    isVerbose = args.verbose

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )

    if response.usage == None:
        raise RuntimeError("Missing response usage section")

    if isVerbose:
        # --verbose behavior
        # Prints useful diagnostics
        print("User prompt: " + prompt)
        print("Prompt tokens: " + str(response.usage.prompt_tokens))
        print("Response tokens: " + str(response.usage.completion_tokens))

    message = response.choices[0].message

    if message.tool_calls != None:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
            result_msg = call_function(tool_call, function_args)
            if result_msg["content"] == None:
                raise Exception("Content of tool call response must not be empty")
            if isVerbose:
                print(f"-> {result_msg['content']}")
    else:
        print("Response: " + message.content)


if __name__ == "__main__":
    main()
