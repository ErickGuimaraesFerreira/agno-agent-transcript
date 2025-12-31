import os
import time
import json
import logging
import google.generativeai as genai
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY not found in .env file")

genai.configure(api_key=api_key)

TARGET_DIRS = ["kallaway", "jeffnippard", "rourkeheath"]
VIDEO_EXTENSIONS = ('.mp4', '.mov', '.avi', '.mkv', '.webm')
OUTPUT_FILE = "transcriptions.json"

safety_settings = [
    { "category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE" },
    { "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE" },
    { "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE" },
    { "category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE" },
]

def load_existing_transcriptions(filepath):
    """
    Loads existing transcriptions from the JSON file.
    Returns a list of dicts.
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        logging.warning(f"Could not decode {filepath}. Starting with empty list.")
        return []

def save_transcriptions(filepath, data):
    """
    Saves the list of transcriptions to the JSON file.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def transcribe_video_gemini(video_path, folder_name):
    """
    Uploads video to Gemini, transcribes it, and returns the data dict.
    """
    video_file = None
    try:
        logging.info(f"Processing with Gemini: {video_path}")
        
        logging.info("Uploading video to Gemini...")
        video_file = genai.upload_file(path=video_path)
        
        while video_file.state.name == "PROCESSING":
            logging.info("Waiting for video processing...")
            time.sleep(5)
            video_file = genai.get_file(video_file.name)
            
        if video_file.state.name == "FAILED":
            raise ValueError(f"Video processing failed: {video_file.state.name}")
            
        logging.info("Video processed. Generating transcription...")
        
        model = genai.GenerativeModel(model_name="gemini-2.5-pro")
        prompt = "Transcreva este vídeo. Retorne apenas o texto da transcrição, sem introduções ou conclusões."
        
        response = model.generate_content(
            [video_file, prompt],
            request_options={"timeout": 600},
            safety_settings=safety_settings
        )
        
        return {
            "folder": folder_name,
            "filename": os.path.basename(video_path),
            "text": response.text
        }

    except Exception as e:
        logging.error(f"Failed to process {video_path}: {e}")
        return None
        
    finally:
        if video_file:
            try:
                video_file.delete()
            except Exception:
                pass

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "gemini-transcripter")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Created output directory: {output_dir}")
        
    output_path = os.path.join(output_dir, OUTPUT_FILE)
    
    transcriptions = load_existing_transcriptions(output_path)
    
    processed_keys = set((item['folder'], item['filename']) for item in transcriptions if 'folder' in item and 'filename' in item)
    
    for folder in TARGET_DIRS:
        dir_path = os.path.join(base_dir, folder)
        
        if not os.path.exists(dir_path):
            logging.warning(f"Directory not found: {dir_path}")
            continue
            
        logging.info(f"Scanning directory: {folder}")
        
        for filename in os.listdir(dir_path):
            if filename.lower().endswith(VIDEO_EXTENSIONS):
                # Check if already processed
                if (folder, filename) in processed_keys:
                    logging.info(f"Skipping {filename} (already in {OUTPUT_FILE})")
                    continue
                
                video_full_path = os.path.join(dir_path, filename)
                
                result = transcribe_video_gemini(video_full_path, folder)
                
                if result:
                    transcriptions.append(result)
                    processed_keys.add((folder, filename))
                    # Save incrementally
                    save_transcriptions(output_path, transcriptions)
                    logging.info(f"Added {filename} to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

