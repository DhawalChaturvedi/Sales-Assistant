from datetime import datetime
import json
from llm_model import generate_llm_response


def format_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def save_txt(transcripts, suggestions, filename="transcript_export.txt"):
    content = "TRANSCRIPTS\n\n"
    for t in transcripts:
        content += f"[{t['timestamp']}] {t['text']}\n"

    content += "\n\n SUGGESTIONS\n\n"
    for s in suggestions:
        content += f"[{s['timestamp']}] {s['text']}\n"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    return filename


def process_transcription_response(message: str):
    try:
        data = json.loads(message)
        if data.get("type") != "Results":
            return None

        alternatives = data.get("channel", {}).get("alternatives", [])
        if not alternatives:
            return None

        transcript = alternatives[0].get("transcript", "").strip()
        if transcript:
            print(f" Transcript: {transcript}")
            return transcript
        else:
            print(" Skipping empty transcript.")
            return None
    except Exception as e:
        print(" Error parsing Deepgram response:", e)
        return None


def handle_transcription_message(message: str):
    
    transcript = process_transcription_response(message)
    if transcript:
        response = generate_llm_response(transcript)
        print(f" LLM Response: {response}")
        return transcript, response
    return None, None
