"""
Minimal ADK test.
Purpose: verify that the ADK client + simple agent work before integrating task logic.
"""

#import asyncio
from dotenv import load_dotenv
import os
from google import genai

# Load environment variables from a .env file if present (including the API key)
# load_dotenv()
# print("API Key Loaded:", bool(os.getenv("GOOGLE_API_KEY")))

# Keep this simple; adjust model as used in codelabs
MODEL_NAME = "gemini-2.5-flash-lite"   # or whatever model matches your environment

# async def main():
#     client = genai.Client()   # Uses your default API key in environment

#     # Create a simple agent with only a system prompt
#     agent = client.agents.create(
#         model=MODEL_NAME,
#         display_name="hello-agent-test",
#         system_instruction="You are a friendly test agent. Respond briefly."
#     )

#     # Send a simple test message
#     user_text = "Hello agent, can you hear me?"
#     print(f"[User] {user_text}")

#     response = await client.agents.send_message(
#         agent_id=agent.name,
#         content=user_text
#     )

#     print("\n[Agent Response]")
#     print(response.text)

def main():
    # Load environment variables from .env (if present)
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    print("API Key Loaded:", bool(api_key))

    # Create the client (it will also pick up the env var automatically)
    client = genai.Client()  # or genai.Client(api_key=api_key)

    user_text = "Hello model, can you hear me?"
    print(f"[User] {user_text}")

    # Simple one-shot request
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_text,
    )

    print("\n[Model Response]")
    print(response.text)

if __name__ == "__main__":
    main()