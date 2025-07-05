import streamlit as st
import asyncio
import websockets
import base64
import sounddevice as sd
import numpy as np
import queue
import json
import socket
from utils import handle_transcription_message, format_timestamp, save_txt
import os
from dotenv import load_dotenv

load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

DEVICE_INDEX = 1

audio_queue = queue.Queue()
stop_flag = False  

if "transcripts" not in st.session_state:
    st.session_state.transcripts = []

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

if "mic_status" not in st.session_state:
    st.session_state.mic_status = False

if "listening" not in st.session_state:
    st.session_state.listening = False

def audio_callback(indata, frames, time, status):
    global stop_flag
    if stop_flag:
        return
    print("🎧 audio_callback() triggered")
    volume = np.linalg.norm(indata) / len(indata)
    print(f"🔊 Volume: {volume:.5f}")
    st.session_state.listening = True
    audio_queue.put(bytes(indata))


async def send_audio(ws):
    global stop_flag
    try:
        with sd.InputStream(device=DEVICE_INDEX, samplerate=16000, channels=1, dtype='int16', callback=audio_callback):
            print("🎤 Mic stream opened.")
            while not stop_flag:
                await asyncio.sleep(0.01)
                if not audio_queue.empty():
                    data = audio_queue.get()
                    encoded_data = base64.b64encode(data).decode('utf-8')
                    await ws.send(json.dumps({"audio_data": encoded_data}))
                    print("📤 Sent audio chunk.")
    except Exception as e:
        print("Error in send_audio:", e)
    finally:
        print("send_audio stopped.")
        st.session_state.mic_status = False
        st.session_state.listening = False

async def receive_transcriptions(ws):
    global stop_flag
    print("Receiving transcription...")
    while not stop_flag:
        try:
            message = await ws.recv()
            print("Received:", message)
            transcript, suggestion = handle_transcription_message(message)
            if transcript and suggestion:
                timestamp = format_timestamp()
                st.session_state.transcripts.append({
                    "timestamp": timestamp,
                    "text": transcript
                })
                st.session_state.suggestions.append({
                    "timestamp": timestamp,
                    "text": suggestion
                })
                print("Stored transcript + suggestion.")
        except Exception as e:
            print(" Error in receive_transcriptions:", e)
            break
    st.session_state.mic_status = False
    st.session_state.listening = False
    print("receive_transcriptions stopped.")


async def connect_deepgram():
    global stop_flag
    stop_flag = False
    st.session_state.mic_status = True
    uri = "wss://api.deepgram.com/v1/listen?punctuate=true"
    headers = {"Authorization": f"Token {DEEPGRAM_API_KEY}"}
    try:
        async with websockets.connect(uri, extra_headers=headers) as ws:
            await asyncio.gather(
                send_audio(ws),
                receive_transcriptions(ws)
            )
    except Exception as e:
        print(" Error connecting to Deepgram:", e)
        st.session_state.mic_status = False


st.title("Real-Time Sales Assistant")

mic_status = st.session_state.mic_status
listening = st.session_state.listening

status_text = "Mic OFF"
if mic_status and listening:
    status_text = " Mic ON -  Listening..."
elif mic_status:
    status_text = " Mic ON - Waiting for speech..."

st.markdown(f"### {status_text}")

# Start button (async-compatible)
if st.button(" Start Listening"):
    asyncio.run(connect_deepgram())

# Stop button
if st.button(" Stop Listening"):
    stop_flag = True
    st.session_state.mic_status = False
    st.session_state.listening = False
    st.warning(" Listening stopped.")

# Output
st.subheader(" Transcripts and Suggestions")
for t, s in zip(st.session_state.transcripts, st.session_state.suggestions):
    st.markdown(f"** [{t['timestamp']}]**")
    st.markdown(f"** You said:** {t['text']}")
    st.markdown(f"** Assistant:** {s['text']}")
    st.markdown("---")

# Export button
if st.button("📤 Export to .txt"):
    filename = save_txt(st.session_state.transcripts, st.session_state.suggestions)
    st.success(f"Saved to {filename}")
