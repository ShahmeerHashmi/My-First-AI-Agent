from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
import os

class FolderInput(BaseModel):
    folder_path: str = Field(..., description="Path of the folder to create")

class FolderTool(BaseTool):
    name: str = "create_folder"
    description: str = "Create a new folder at the specified path"
    args_schema: Type[BaseModel] = FolderInput

    async def _arun(self, folder_path: str) -> str:
        try:
            # Convert relative path to absolute path if necessary
            if folder_path.startswith('./') or folder_path.startswith('.\\'):
                folder_path = os.path.abspath(folder_path)
            
            os.makedirs(folder_path, exist_ok=True)
            return f"Successfully created folder: {folder_path}"
        except Exception as e:
            return f"Error creating folder: {str(e)}"

    def _run(self, folder_path: str) -> str:
        try:
            # Convert relative path to absolute path if necessary
            if folder_path.startswith('./') or folder_path.startswith('.\\'):
                folder_path = os.path.abspath(folder_path)
            
            os.makedirs(folder_path, exist_ok=True)
            return f"Successfully created folder: {folder_path}"
        except Exception as e:
            return f"Error creating folder: {str(e)}"
