import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("Missing OPENROUTER_API_KEY environment variable")

    # print(len(api_key))

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    # prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    prompt = args.user_prompt
    isVerbose = args.verbose

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    if response.usage == None:
        raise RuntimeError("Missing response usage section")

    if isVerbose:
        print("User prompt: " + prompt)
        print("Prompt tokens: " + str(response.usage.prompt_tokens))
        print("Response tokens: " + str(response.usage.completion_tokens))
    print("Response: " + response.choices[0].message.content)


if __name__ == "__main__":
    main()
