import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

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

def main():
    # Get response from Gemini after giving a text prompt
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages
    )

    # Get usage metadata (input and output tokens)
    usage = response.usage_metadata
    if usage is None:
        raise RuntimeError("failed to send Gemini API request.")
    if args.verbose == True:
        print(f"User prompt: {messages[0].parts[0].text}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")

    print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
