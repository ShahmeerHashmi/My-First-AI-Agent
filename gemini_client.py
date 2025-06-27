import google.generativeai as genai
import os
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from folder_tool import FolderTool

class GeminiClient:
    def __init__(self, api_key: str = None, model: str = "gemini-1.5-flash"):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("API key must be provided or set in GEMINI_API_KEY environment variable")
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize LangChain components
        self.llm = ChatGoogleGenerativeAI(model=model, google_api_key=api_key)
        self.tools = [FolderTool()]
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    async def generate_response(self, prompt: str) -> Dict[str, Any]:
        """
        Generate a response using the Gemini API and LangChain.
        :param prompt: The text prompt to send to the agent
        :return: Response dictionary containing the generated text
        """
        try:
            # Run the agent with the prompt
            response = await self.agent.arun(prompt)
            return {
                "response": response,
                "status": "success"
            }
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }

    async def create_folder(self, folder_path: str) -> Dict[str, Any]:
        """
        Create a folder at the specified path.
        :param folder_path: The path where the folder should be created
        :return: Response dictionary indicating success or failure
        """
        try:
            # Send a folder creation command to the agent
            response = await self.agent.arun(f"Create a folder at path: {folder_path}")
            return {
                "response": response,
                "status": "success"
            }
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }
