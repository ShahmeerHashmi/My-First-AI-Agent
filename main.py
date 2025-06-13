import os
from dotenv import load_dotenv
import chainlit as cl
from gemini_client import GeminiClient

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini client with API key from environment variable
gemini_client = GeminiClient(model="gemini-1.5-flash")

@cl.on_message
async def main(message):
    # Access the content of the message
    content = message.content if hasattr(message, "content") else str(message)
    
    # Check if it's a folder creation command
    if content.lower().startswith("create folder"):
        # Extract the folder path from the command
        folder_path = content[13:].strip()  # Remove "create folder" and trim whitespace
        if folder_path:
            result = await gemini_client.create_folder(folder_path)
            if result["status"] == "success":
                await cl.Message(content=result["response"]).send()
            else:
                await cl.Message(content=f"Failed to create folder: {result['error']}").send()
        else:
            await cl.Message(content="Please specify a folder path. Example: create folder my_folder").send()
    else:
        # Handle other messages with Gemini API
        result = await gemini_client.generate_response(content)
        if "error" in result:
            await cl.Message(content=f"Failed to process request: {result['error']}").send()
        else:
            await cl.Message(content=result["response"]).send()
