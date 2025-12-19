import json
import os

def get_transcriptions_file_path():
    """Returns the absolute path to the transcriptions file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "gemini-transcripter", "transcriptions.json")

def get_data():
    """Reads the JSON data securely."""
    filepath = get_transcriptions_file_path()
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def list_available_creators() -> str:
    """
    Lists all content creators found in the transcriptions database.
    
    Returns:
        str: A comma-separated list of creator names.
    """
    data = get_data()
    creators = set(item.get('folder') for item in data if item.get('folder'))
    if not creators:
        return "No creators found."
    return ", ".join(sorted(list(creators)))

def get_creator_transcriptions(creator_name: str) -> str:
    """
    Retrieves all transcriptions for a specific content creator.
    
    Args:
        creator_name (str): The name of the creator (folder name) to filter by.
        
    Returns:
        str: A formatted string containing all video titles and their transcriptions.
    """
    data = get_data()
    # Normalize input for better matching
    creator_name = creator_name.lower().strip()
    
    results = [
        f"--- Video: {item.get('filename')} ---\n\n{item.get('text')}\n"
        for item in data 
        if item.get('folder', '').lower() == creator_name
    ]
    
    if not results:
        return f"No transcriptions found for creator: {creator_name}"
        
    return "\n".join(results)
