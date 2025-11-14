"""
FileOperator is a tool that provides file operations such as
creating, editing, deleting folders and files.
"""

import os

from langchain.tools import tool


class FolderOperations:
    # create folder
    @tool
    def CreateFolder(self, folder_path: str) -> str:
        try:
            os.makedirs(folder_path, exist_ok=True)
            return f"Folder '{folder_path}' created successfully."
        except Exception as e:
            return f"Error creating folder '{folder_path}': {str(e)}"

    # edit folder
    @tool
    def EditFolder(self, old_folder_path: str, new_folder_path: str) -> str:
        try:
            os.rename(old_folder_path, new_folder_path)
            return f"Folder renamed from '{old_folder_path}' to '{new_folder_path}' successfully."
        except Exception as e:
            return f"Error renaming folder '{old_folder_path}': {str(e)}"

    # delete folder
    @tool
    def DeleteFolder(self, folder_path: str) -> str:
        try:
            os.rmdir(folder_path)
            return f"Folder '{folder_path}' deleted successfully."
        except Exception as e:
            return f"Error deleting folder '{folder_path}': {str(e)}"


# create file
class FileOperations:
    @tool
    def CreateFile(self, file_path: str, content: str = "") -> str:
        try:
            with open(file_path, "w") as file:
                file.write(content)
            return f"File '{file_path}' created successfully."
        except Exception as e:
            return f"Error creating file '{file_path}': {str(e)}"

    # edit file
    @tool
    def EditFile(self, file_path: str, new_content: str) -> str:
        try:
            with open(file_path, "w") as file:
                file.write(new_content)
            return f"File '{file_path}' edited successfully."
        except Exception as e:
            return f"Error editing file '{file_path}': {str(e)}"

    # delete file
    @tool
    def DeleteFile(self, file_path: str) -> str:
        try:
            os.remove(file_path)
            return f"File '{file_path}' deleted successfully."
        except Exception as e:
            return f"Error deleting file '{file_path}': {str(e)}"
