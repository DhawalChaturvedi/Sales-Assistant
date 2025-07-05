# 🧠 Real-Time Sales Assistant (Prototype)

A lightweight Streamlit-based app that listens to live microphone input, transcribes it in real time, and generates intelligent suggestions using an LLM (e.g., LLaMA 3 via Together AI or Ollama). Built to assist sales representatives during live calls or meetings.

---

## 🚀 Features

- 🎤 **Live Microphone Transcription**  
  Real-time transcription from mic input using a WebSocket-based transcription service.

- 🧠 **LLM-Based Suggestions**  
  Sends transcribed speech to an LLM (like LLaMA 3) for intelligent sales suggestions.

- 📂 **Export Transcripts and Suggestions**  
  Download the full transcript and AI-generated prompts as `.txt` files.

- ✅ **Mic Status Indicator**  
  UI clearly shows if mic is currently ON or OFF.

- ⚡ **Low-Latency Response Loop**  
  Runs transcription and LLM generation concurrently with threading + async.

---

## 🛠️ Tech Stack

| Layer         | Technology                        |
|---------------|-----------------------------------|
| Frontend      | Streamlit                         |
| Audio Input   | `sounddevice`, `websockets`       |
| Transcription | Manual WebSocket (Deepgram-like)  |
| LLM Backend   | LLaMA 3 via Together AI / Ollama  |
| Language      | Python                            |

---

## 📁 File Structure

```
📦 sales-assistant/
├── app.py                  # Main Streamlit app (UI + control)
├── llm_model.py            # Handles LLM API requests/responses
├── utils.py                # Utilities for mic state, transcript, etc.
├── audio_processor.py      # (Optional) Handles mic recording and streaming
└── README.md               # This file
```

---

## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
pip install streamlit sounddevice websockets requests python-dotenv
```

### 2. Configure `.env` (for TogetherAI or Ollama)

Create a `.env` file in the root directory:

```
TOGETHER_API_KEY=your_key_here
OLLAMA_BASE_URL=http://localhost:11434
```

> ⚠️ Use either **TogetherAI** or **Ollama**, not both simultaneously.

### 3. Run the App

```bash
streamlit run app.py
```

---

## 🧪 Sample Input/Output

### 🎤 Input:
> *"We have a client interested in a bulk deal, how should I pitch?"*

### 🧠 LLM Response:
> *"Highlight the exclusive discount for bulk orders and offer limited-time perks like free shipping or onboarding support."*

---

## 📌 Notes

- Ensure microphone permissions are enabled.
- Ollama must be running locally with `llama3` model pulled if using locally.
- Avoid long silences—this app works best with active speech input.

---

## 📜 License

This project is open-source and intended for educational or prototyping use. No warranties for production use.

---

## ✍️ Author

**Dhawal Chaturevdi**  
BTech Final Year | Python & AI Developer
