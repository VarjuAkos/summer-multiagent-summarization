import base64
import os
import json
from datetime import datetime
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage
import requests
import re
import json
from typing import Dict, Any

def load_markdown_to_str(file_path):
	with open(file_path, 'r', encoding='utf-8') as md_file:
		markdown_content = md_file.read()
	return markdown_content

def load_latest_sprint_status(base_path):
    """
    Find the latest sprint directory and load the project-sprint-status.md file.
    
    Args:
    base_path (str): Path to the directory containing sprint folders.
    
    Returns:
    str: Content of the project-sprint-status.md file from the latest sprint.
    """
    try:
        # List all directories in the base path
        directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        
        # Filter and sort sprint directories
        sprint_dirs = sorted([d for d in directories if d.startswith('sprint') and d[6:].isdigit()],
                             key=lambda x: int(x[6:]),
                             reverse=True)
        
        if not sprint_dirs:
            return "No sprint directories found."
        
        # Get the latest sprint directory
        latest_sprint = sprint_dirs[0]
        sprint_path = os.path.join(base_path, latest_sprint)
        
        # Look for project-sprint-status.md in the latest sprint directory
        status_file = os.path.join(sprint_path, 'project-sprint-status.md')
        
        if os.path.exists(status_file):
            with open(status_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f"project-sprint-status.md not found in {latest_sprint}."
    
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
    
def load_latest_sprint_backlog(base_path):
    """
    Find the latest sprint directory and load the project-sprint-backlog.json file.
    
    Args:
    base_path (str): Path to the directory containing sprint folders.
    
    Returns:
    dict: Content of the project-sprint-backlog.json file from the latest sprint.
    """
    try:
        # List all directories in the base path
        directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        
        # Filter and sort sprint directories
        sprint_dirs = sorted([d for d in directories if d.startswith('sprint') and d[6:].isdigit()],
                             key=lambda x: int(x[6:]),
                             reverse=True)
        
        if not sprint_dirs:
            return {"error": "No sprint directories found."}
        
        # Get the latest sprint directory
        latest_sprint = sprint_dirs[0]
        sprint_path = os.path.join(base_path, latest_sprint)
        
        # Look for project-sprint-backlog.json in the latest sprint directory
        backlog_file = os.path.join(sprint_path, 'project-sprint-backlog.json')
        
        if os.path.exists(backlog_file):
            with open(backlog_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {"error": f"project-sprint-backlog.json not found in {latest_sprint}."}
    
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    
def export_transcript(state, folder_path):
    # Create the folder if it doesn't exist
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    id = len(files) + 1
    transcript = state["transcript"]
    
    filename = state["meeting_type"].replace(" ","_") + str(id) + ".txt"
    
    os.makedirs(os.path.join(folder_path), exist_ok=True)
    
    
    # Construct the full file path
    file_path = os.path.join(folder_path, filename)
    
    # Write the string to a text file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(transcript)

def export_state(state, folder_path, filename):
    # Create the folder if it doesn't exist
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    id = len(files) + 1
    
    filename = filename+str(id)+".json"
    
    os.makedirs(folder_path, exist_ok=True)
    
    # Construct the full file path
    file_path = os.path.join(folder_path, filename)
    
    # Write the state dict to a JSON file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=4)

def load_txt_to_str(file_path):
    with open(file_path, 'r', encoding='utf-8') as txt_file:
        text_content = txt_file.read()
    return text_content

def load_from_json(file_path):
    """
    Load data from a JSON file.
    
    Args:
    file_path (str): Path to the JSON file.
    
    Returns:
    dict: A dictionary containing the loaded JSON data.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file {file_path}")
        return {}
    
def render_mermaid_diagram(diagram_code: str) -> str:
    # Encode the Mermaid code
    encoded_diagram = base64.b64encode(diagram_code.encode('utf-8')).decode('utf-8')
    
    # Make a request to the Mermaid rendering service
    url = f"https://mermaid.ink/img/{encoded_diagram}"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Return the URL of the rendered image
        return url
    else:
        # If rendering failed, return the original Mermaid code
        return f"```mermaid\n{diagram_code}\n```"
    
def format_mermaid(input_string):
    # Step 1: Remove redundant "```mermaid" at the start and end
    cleaned_string = input_string.replace('```mermaid', '').replace('```', '')
    
    # Step 2: Replace escaped newlines with actual newlines
    formatted_string = cleaned_string.replace(r'\n', '\n')
    
    # Step 3: Strip any leading/trailing whitespace
    formatted_string = formatted_string.strip()

    return formatted_string	


def export_meeting_history(state, output_file='meeting_history.json'):
    """
    Export the meeting history to a JSON file.
    
    Args:
    state (dict): The state dictionary containing the meeting history.
    output_file (str): The name of the output file. Defaults to 'meeting_history.json'.
    
    Returns:
    None
    """
    meeting_history = state.get("meeting_history", [])
    
    # Ensure meeting_history is a list
    if not isinstance(meeting_history, list):
        meeting_history = [meeting_history]
    
    try:
        with open(output_file, 'w') as file:
            json.dump(meeting_history, file, indent=2)
        print(f"Meeting history exported successfully to {output_file}")
    except IOError:
        print(f"Error: Unable to write to file {output_file}")

    return state  # Return the state to maintain consistency with your workflow


def manage_sprint_folders(state, project_folder):
    """
    Manages sprint folders based on the meeting type.
    Creates a new sprint folder if necessary and adds required files.
    
    :param state: The current state dictionary
    :param project_folder: Path to the project folder
    :return: Updated state with new sprint information
    """
    if "planning" in state.get("meeting_type", "").lower() or "plan" in state.get("meeting_type", "").lower():
        # List all directories in the project folder
        directories = [d for d in os.listdir(project_folder) if os.path.isdir(os.path.join(project_folder, d))]
        
        # Filter and find the highest sprint number
        sprint_numbers = [int(re.findall(r'\d+', d)[0]) for d in directories if d.startswith("sprint") and re.findall(r'\d+', d)]
        
        if sprint_numbers:
            new_sprint_number = max(sprint_numbers) + 1
        else:
            new_sprint_number = 1
        
        # Create new sprint folder
        new_sprint_folder = os.path.join(project_folder, f"sprint{new_sprint_number}")
        os.makedirs(new_sprint_folder, exist_ok=True)
        
        # Create project_sprint_status.md
        status_file_path = os.path.join(new_sprint_folder, "project_sprint_status.md")
        with open(status_file_path, 'w') as status_file:
            status_file.write(f"# Sprint {new_sprint_number} Status\n\nStatus details will be updated here.")
        
        # Create project_sprint_backlog.json
        backlog_file_path = os.path.join(new_sprint_folder, "project_sprint_backlog.json")
        initial_backlog = {}
        with open(backlog_file_path, 'w') as backlog_file:
            json.dump(initial_backlog, backlog_file, indent=2)
        
        # Update state with new sprint information
        state["current_sprint_number"] = new_sprint_number
        state["current_sprint_folder"] = new_sprint_folder
        state["sprint_status_file"] = status_file_path
        state["sprint_backlog_file"] = backlog_file_path
        
        print(f"Created new sprint folder: {new_sprint_folder}")
    else:
        print("Meeting type does not indicate a planning session. No new sprint folder created.")
    
    return state


def load_json(file_path: str) -> Dict[str, Any]:
    """
    Reads a JSON file and returns its contents as a dictionary.

    :param file_path: The path to the JSON file to be read
    :return: A dictionary containing the data from the JSON file
    :raises FileNotFoundError: If the specified file does not exist
    :raises json.JSONDecodeError: If the file is not valid JSON
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(f"Successfully loaded JSON from {file_path}")
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        raise
    except json.JSONDecodeError as e:
        print(f"Error: The file {file_path} is not valid JSON. Error: {str(e)}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred while reading {file_path}: {str(e)}")
        raise


def get_latest_sprint_folder(project_folder: str) -> str:
    """
    Scans the project folder for sprint folders and returns the name of the latest sprint folder.

    :param project_folder: Path to the project folder (e.g., 'project1/')
    :return: Name of the latest sprint folder (e.g., 'sprint5'), or None if no sprint folders are found
    """
    # List all items in the project folder
    items = os.listdir(project_folder)

    # Filter for sprint folders and extract their numbers
    sprint_folders = []
    for item in items:
        if os.path.isdir(os.path.join(project_folder, item)):
            match = re.match(r'sprint(\d+)', item, re.IGNORECASE)
            if match:
                sprint_number = int(match.group(1))
                sprint_folders.append((item, sprint_number))

    # Sort sprint folders by number (descending) and return the latest
    if sprint_folders:
        latest_sprint = max(sprint_folders, key=lambda x: x[1])
        print(f"Latest sprint folder found: {latest_sprint[0]}")
        return latest_sprint[0]
    else:
        print("No sprint folders found.")
        return None


def export_markdown(content, file_path):
    """
    Export content to a Markdown file.
    
    Args:
    content (str): The content to be written to the file.
    file_path (str): The path where the file should be saved.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully exported Markdown to {file_path}")
    except Exception as e:
        print(f"Error exporting Markdown: {str(e)}")

def export_json(content, file_path):
    """
    Export content to a JSON file.
    
    Args:
    content (dict): The content to be written to the file.
    file_path (str): The path where the file should be saved.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2)
        print(f"Successfully exported JSON to {file_path}")
    except Exception as e:
        print(f"Error exporting JSON: {str(e)}")
        
def load_latest_json(folder_path: str) -> Dict[str, Any]:
    """
    Reads the latest JSON file from a given folder and returns its contents as a dictionary.

    :param folder_path: The path to the folder containing JSON files
    :return: A dictionary containing the data from the latest JSON file
    :raises FileNotFoundError: If no JSON files are found in the specified folder
    :raises json.JSONDecodeError: If the latest file is not valid JSON
    """
    try:
        # Get all JSON files in the folder
        json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
        
        if not json_files:
            raise FileNotFoundError(f"No JSON files found in {folder_path}")
        
        # Find the latest JSON file
        latest_file = max(json_files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
        latest_file_path = os.path.join(folder_path, latest_file)
        
        # Read and parse the latest JSON file
        with open(latest_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        print(f"Successfully loaded latest JSON from {latest_file_path}")
        return data
    
    except FileNotFoundError:
        print(f"Error: No JSON files found in {folder_path}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error: The file {latest_file_path} is not valid JSON. Error: {str(e)}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred while reading from {folder_path}: {str(e)}")
        raise