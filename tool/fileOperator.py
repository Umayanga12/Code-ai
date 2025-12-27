"""
File Operator Tool for AI Agents
Provides comprehensive file operations including read, write, create, delete, list, and more.
"""

import os
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any
import json


def read_file(file_path: str) -> Dict[str, Any]:
    """
    Read the contents of a file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        Dictionary with status and content or error message
    """
    try:
        file_path = os.path.abspath(file_path)
        
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }
        
        if not os.path.isfile(file_path):
            return {
                "success": False,
                "error": f"Path is not a file: {file_path}"
            }
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "success": True,
            "file_path": file_path,
            "content": content,
            "size_bytes": os.path.getsize(file_path)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error reading file: {str(e)}"
        }


def write_file(file_path: str, content: str, mode: str = "w") -> Dict[str, Any]:
    """
    Write content to a file. Creates the file and parent directories if they don't exist.
    
    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        mode: Write mode ('w' for overwrite, 'a' for append)
        
    Returns:
        Dictionary with status and details or error message
    """
    try:
        file_path = os.path.abspath(file_path)
        
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, mode, encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "file_path": file_path,
            "message": f"File {'appended to' if mode == 'a' else 'written'} successfully",
            "size_bytes": os.path.getsize(file_path)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error writing file: {str(e)}"
        }


def create_file(file_path: str, content: str = "") -> Dict[str, Any]:
    """
    Create a new file with optional initial content.
    
    Args:
        file_path: Path to the file to create
        content: Initial content for the file (default: empty)
        
    Returns:
        Dictionary with status and details or error message
    """
    try:
        file_path = os.path.abspath(file_path)
        
        if os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File already exists: {file_path}"
            }
        
        return write_file(file_path, content, mode="w")
    except Exception as e:
        return {
            "success": False,
            "error": f"Error creating file: {str(e)}"
        }


def delete_file(file_path: str) -> Dict[str, Any]:
    """
    Delete a file.
    
    Args:
        file_path: Path to the file to delete
        
    Returns:
        Dictionary with status and details or error message
    """
    try:
        file_path = os.path.abspath(file_path)
        
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }
        
        if not os.path.isfile(file_path):
            return {
                "success": False,
                "error": f"Path is not a file: {file_path}"
            }
        
        os.remove(file_path)
        
        return {
            "success": True,
            "file_path": file_path,
            "message": "File deleted successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error deleting file: {str(e)}"
        }


def list_directory(directory_path: str, include_hidden: bool = False) -> Dict[str, Any]:
    """
    List contents of a directory.
    
    Args:
        directory_path: Path to the directory to list
        include_hidden: Whether to include hidden files (starting with .)
        
    Returns:
        Dictionary with status and list of files/directories or error message
    """
    try:
        directory_path = os.path.abspath(directory_path)
        
        if not os.path.exists(directory_path):
            return {
                "success": False,
                "error": f"Directory not found: {directory_path}"
            }
        
        if not os.path.isdir(directory_path):
            return {
                "success": False,
                "error": f"Path is not a directory: {directory_path}"
            }
        
        items = os.listdir(directory_path)
        
        if not include_hidden:
            items = [item for item in items if not item.startswith('.')]
        
        files = []
        directories = []
        
        for item in items:
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                files.append({
                    "name": item,
                    "size_bytes": os.path.getsize(item_path),
                    "path": item_path
                })
            elif os.path.isdir(item_path):
                directories.append({
                    "name": item,
                    "path": item_path
                })
        
        return {
            "success": True,
            "directory_path": directory_path,
            "files": files,
            "directories": directories,
            "total_files": len(files),
            "total_directories": len(directories)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error listing directory: {str(e)}"
        }


def create_directory(directory_path: str) -> Dict[str, Any]:
    """
    Create a new directory. Creates parent directories if they don't exist.
    
    Args:
        directory_path: Path to the directory to create
        
    Returns:
        Dictionary with status and details or error message
    """
    try:
        directory_path = os.path.abspath(directory_path)
        
        if os.path.exists(directory_path):
            return {
                "success": False,
                "error": f"Directory already exists: {directory_path}"
            }
        
        os.makedirs(directory_path, exist_ok=True)
        
        return {
            "success": True,
            "directory_path": directory_path,
            "message": "Directory created successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error creating directory: {str(e)}"
        }


def delete_directory(directory_path: str, recursive: bool = False) -> Dict[str, Any]:
    """
    Delete a directory.
    
    Args:
        directory_path: Path to the directory to delete
        recursive: Whether to delete non-empty directories
        
    Returns:
        Dictionary with status and details or error message
    """
    try:
        directory_path = os.path.abspath(directory_path)
        
        if not os.path.exists(directory_path):
            return {
                "success": False,
                "error": f"Directory not found: {directory_path}"
            }
        
        if not os.path.isdir(directory_path):
            return {
                "success": False,
                "error": f"Path is not a directory: {directory_path}"
            }
        
        if os.listdir(directory_path) and not recursive:
            return {
                "success": False,
                "error": "Directory is not empty. Set recursive=True to delete non-empty directories."
            }
        
        if recursive:
            shutil.rmtree(directory_path)
        else:
            os.rmdir(directory_path)
        
        return {
            "success": True,
            "directory_path": directory_path,
            "message": "Directory deleted successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error deleting directory: {str(e)}"
        }


def copy_file(source_path: str, destination_path: str) -> Dict[str, Any]:
    """
    Copy a file from source to destination.
    
    Args:
        source_path: Path to the source file
        destination_path: Path to the destination file
        
    Returns:
        Dictionary with status and details or error message
    """
    try:
        source_path = os.path.abspath(source_path)
        destination_path = os.path.abspath(destination_path)
        
        if not os.path.exists(source_path):
            return {
                "success": False,
                "error": f"Source file not found: {source_path}"
            }
        
        if not os.path.isfile(source_path):
            return {
                "success": False,
                "error": f"Source path is not a file: {source_path}"
            }
        
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        shutil.copy2(source_path, destination_path)
        
        return {
            "success": True,
            "source_path": source_path,
            "destination_path": destination_path,
            "message": "File copied successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error copying file: {str(e)}"
        }


def move_file(source_path: str, destination_path: str) -> Dict[str, Any]:
    """
    Move a file from source to destination.
    
    Args:
        source_path: Path to the source file
        destination_path: Path to the destination file
        
    Returns:
        Dictionary with status and details or error message
    """
    try:
        source_path = os.path.abspath(source_path)
        destination_path = os.path.abspath(destination_path)
        
        if not os.path.exists(source_path):
            return {
                "success": False,
                "error": f"Source file not found: {source_path}"
            }
        
        if not os.path.isfile(source_path):
            return {
                "success": False,
                "error": f"Source path is not a file: {source_path}"
            }
        
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        shutil.move(source_path, destination_path)
        
        return {
            "success": True,
            "source_path": source_path,
            "destination_path": destination_path,
            "message": "File moved successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error moving file: {str(e)}"
        }


def file_exists(file_path: str) -> Dict[str, Any]:
    """
    Check if a file or directory exists.
    
    Args:
        file_path: Path to check
        
    Returns:
        Dictionary with status and existence details
    """
    try:
        file_path = os.path.abspath(file_path)
        exists = os.path.exists(file_path)
        
        result = {
            "success": True,
            "file_path": file_path,
            "exists": exists
        }
        
        if exists:
            result["is_file"] = os.path.isfile(file_path)
            result["is_directory"] = os.path.isdir(file_path)
            if os.path.isfile(file_path):
                result["size_bytes"] = os.path.getsize(file_path)
        
        return result
    except Exception as e:
        return {
            "success": False,
            "error": f"Error checking file existence: {str(e)}"
        }


def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    Get detailed information about a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary with file information or error message
    """
    try:
        file_path = os.path.abspath(file_path)
        
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }
        
        stat_info = os.stat(file_path)
        
        return {
            "success": True,
            "file_path": file_path,
            "is_file": os.path.isfile(file_path),
            "is_directory": os.path.isdir(file_path),
            "size_bytes": stat_info.st_size,
            "created_time": stat_info.st_ctime,
            "modified_time": stat_info.st_mtime,
            "accessed_time": stat_info.st_atime
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error getting file info: {str(e)}"
        }


def search_files(directory_path: str, pattern: str, recursive: bool = True) -> Dict[str, Any]:
    """
    Search for files matching a pattern in a directory.
    
    Args:
        directory_path: Directory to search in
        pattern: Pattern to match (e.g., "*.py", "test_*", etc.)
        recursive: Whether to search recursively in subdirectories
        
    Returns:
        Dictionary with matching files or error message
    """
    try:
        directory_path = os.path.abspath(directory_path)
        
        if not os.path.exists(directory_path):
            return {
                "success": False,
                "error": f"Directory not found: {directory_path}"
            }
        
        if not os.path.isdir(directory_path):
            return {
                "success": False,
                "error": f"Path is not a directory: {directory_path}"
            }
        
        path_obj = Path(directory_path)
        
        if recursive:
            matches = list(path_obj.rglob(pattern))
        else:
            matches = list(path_obj.glob(pattern))
        
        files = []
        for match in matches:
            if match.is_file():
                files.append({
                    "name": match.name,
                    "path": str(match.absolute()),
                    "size_bytes": match.stat().st_size
                })
        
        return {
            "success": True,
            "directory_path": directory_path,
            "pattern": pattern,
            "files": files,
            "total_matches": len(files)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error searching files: {str(e)}"
        }


# Export all file operation functions as a list of tools
file_operator_tools = [
    read_file,
    write_file,
    create_file,
    delete_file,
    list_directory,
    create_directory,
    delete_directory,
    copy_file,
    move_file,
    file_exists,
    get_file_info,
    search_files
]
