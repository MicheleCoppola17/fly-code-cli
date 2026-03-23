import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    # Create parser
    parser = argparse.ArgumentParser(prog="Fly Code CLI", description="AI Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Create list of types.Content
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Load API key from .env
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("couldn't find the Gemini API key.")

    # Create a new instance of a Gemini client
    client = genai.Client(api_key=api_key)  

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, args.verbose)  
    

def generate_content(client, messages, verbose):
    # Get response from Gemini after giving a text prompt
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
            )
    )

    # Get usage metadata (input and output tokens)
    if not response.usage_metadata:
        raise RuntimeError("failed to send Gemini API request.")
    # If user adds --verbose as args
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        print("Response:")
        print(response.text)
        return
    
    # List to hold function result parts
    function_response_parts = []

    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose=verbose)

        # 1. Check that .parts exists and is non‑empty
        if not function_call_result.parts:
            raise RuntimeError("function_call_result.parts is empty")
        
        # 2. Get the first part and check .function_response
        part = function_call_result.parts[0]
        if not part.function_response:
            raise RuntimeError("function_response is None")
        
        # 3. Check .response inside the FunctionResponse
        resp_dict = part.function_response.response
        if resp_dict is None:
            raise RuntimeError("function_response.response is None")
        
        # 4. Append the part to the list of function results
        function_response_parts.append(part)

        # 5. Print the result in verbose mode
        if verbose:
            print(f"-> {resp_dict}")




if __name__ == "__main__":
    main()
