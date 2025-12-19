import os
import json
import logging
from dotenv import load_dotenv
from groq import Groq
from moviepy import VideoFileClip

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)

# Target directories
TARGET_DIRS = ["kallaway", "jeffnippard", "rourkeheath"]

# Supported video extensions
VIDEO_EXTENSIONS = ('.mp4', '.mov', '.avi', '.mkv', '.webm')

def transcribe_video(video_path):
    """
    Extracts audio from video, transcribes it using Groq, and saves to JSON.
    """
    try:
        logging.info(f"Processing: {video_path}")
        
        # 1. Extract audio to temporary file
        temp_audio_path = "temp_audio.mp3"
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(temp_audio_path, logger=None)
        video.close()
        
        # 2. Transcribe using Groq
        logging.info("Transcribing...")
        with open(temp_audio_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(temp_audio_path, file.read()),
                model="whisper-large-v3",
                response_format="json",
                temperature=0.0
            )
        
        # 3. Save to JSON
        json_filename = os.path.splitext(video_path)[0] + ".json"
        
        # Prepare JSON content
        output_data = {
            "filename": os.path.basename(video_path),
            "text": transcription.text
        }
        
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(output_data, json_file, ensure_ascii=False, indent=4)
        
        logging.info(f"Saved transcription to: {json_filename}")
        
        # 4. Cleanup temporary audio
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            
    except Exception as e:
        logging.error(f"Failed to process {video_path}: {e}")
        # Clean up in case of error
        if os.path.exists("temp_audio.mp3"):
            os.remove("temp_audio.mp3")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for folder in TARGET_DIRS:
        dir_path = os.path.join(base_dir, folder)
        
        if not os.path.exists(dir_path):
            logging.warning(f"Directory not found: {dir_path}")
            continue
            
        logging.info(f"Scanning directory: {folder}")
        
        for filename in os.listdir(dir_path):
            if filename.lower().endswith(VIDEO_EXTENSIONS):
                video_full_path = os.path.join(dir_path, filename)
                
                # Check if JSON already exists (optional optimization, but good practice)
                json_check_path = os.path.splitext(video_full_path)[0] + ".json"
                if os.path.exists(json_check_path):
                    logging.info(f"Skipping {filename}, JSON already exists.")
                    continue
                
                transcribe_video(video_full_path)

if __name__ == "__main__":
    main()
