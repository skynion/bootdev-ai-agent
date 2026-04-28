import os
import sys
import argparse
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("user_prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(20):
        # retry logic (kept from before, but shorter is fine too)
        timeout_seconds = 300
        start_time = time.time()
        delay = 2
        response = None

        while time.time() - start_time < timeout_seconds:
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=messages,
                    config=types.GenerateContentConfig(
                        tools=[available_functions],
                        system_instruction=system_prompt,
                        temperature=0,
                    ),
                )
                break
            except Exception:
                time.sleep(delay)
                delay = min(delay * 2, 30)

        if response is None:
            sys.exit(1)

        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if not response.function_calls:
            print("Final response:")
            print(response.text)
            return

        function_responses = []
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, args.verbose)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
                or not function_call_result.parts[0].function_response.response
            ):
                raise Exception("empty function call result")
            function_responses.extend(function_call_result.parts)

        messages.append(types.Content(role="user", parts=function_responses))

    print("Error: reached maximum iterations without a final response")
    sys.exit(1)


if __name__ == "__main__":
    main()
