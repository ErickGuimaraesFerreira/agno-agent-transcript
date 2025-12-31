import json
import os

def get_transcriptions_file_path():
    """."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "gemini-transcripter", "transcriptions.json")

def get_data():
    """Ler o arquivo JSON."""
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
    Lista todos os criadores de conteúdos encontrados no database.
    Returns:
        str: .
    """
    data = get_data()
    creators = set(item.get('folder') for item in data if item.get('folder'))
    if not creators:
        return "No creators found."
    return ", ".join(sorted(list(creators)))

def get_creator_transcriptions(creator_name: str) -> str:
    """
    Busca todas as transcrições de um criador de conteúdo específico.
    
    Args:
        creator_name (str): nome do criador para filtrar.
        
    Returns:
        str: String contendo todos os títulos dos vídeos e suas transcrições.
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
        return f"sem transcrições encontradas do: {creator_name}"
        
    return "\n".join(results)

