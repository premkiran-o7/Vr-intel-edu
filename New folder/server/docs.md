## 🧠 VR Story Agent — Local Testing Guide

This guide explains how to **set up and test** the Story Agent backend (`FastAPI + LangChain + Groq`)
and its **Streamlit Test UI** for the VR-Intel-Edu project.

---

### 📂 Folder Overview

```
Vr-intel-edu/
├── Godot/
├── nature_kit/
├── server/
│   ├── agent.py
│   ├── app.py
│   ├── main.py
│   ├── secrets.py
│   ├── .env
│   ├── pyproject.toml / requirements.txt
│   └── README.md   ← (this file)
```

---

### ⚙️ 1. Environment Setup

#### a. Move into the server folder

```bash
cd server
```

#### b. Create and activate a virtual environment

```bash
# Using uv (recommended)
uv venv
source .venv/Scripts/activate    # (Windows)
# or
source .venv/bin/activate        # (macOS/Linux)
```

> 💡 If `uv` isn’t installed, run:
> `pip install uv`

---

### 📦 2. Install Dependencies

If you have a `pyproject.toml`:

```bash
uv sync
```

Or, if you’re using a `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### 🔑 3. Add Your Groq API Key

Create a `.env` file inside `server/` and add:

```
GROQ_API_KEY=your_groq_api_key_here
```

This is automatically loaded via `secrets.py`.

---

### 🚀 4. Run the FastAPI Server

Start the backend server:

```bash
uvicorn app:app --reload
```

**Expected output:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

Now test the endpoints in your browser or Postman:

* ✅ Status → [http://127.0.0.1:8000/status](http://127.0.0.1:8000/status)
* 💬 Chat → POST `http://127.0.0.1:8000/chat`
* 🎭 Event → POST `http://127.0.0.1:8000/event`

---

### 🧩 5. Run the Streamlit Test UI

Open a **new terminal** (keep the FastAPI server running) and run:

```bash
streamlit run main.py
```

This launches the Streamlit dashboard at:

👉 [http://localhost:8501](http://localhost:8501)

---

### 🧪 6. Testing Workflow

| Step | Action                          | Endpoint         |
| ---- | ------------------------------- | ---------------- |
| 1    | Check server status             | `/status`        |
| 2    | Chat with the Story Agent       | `/chat`          |
| 3    | Generate story event JSON       | `/event`         |
| 4    | (Optional) Connect Godot client | `/ws` *(future)* |

---

### 🧰 7. Useful Commands

| Purpose                | Command                    |
| ---------------------- | -------------------------- |
| Reinstall dependencies | `uv sync --reinstall`      |
| Start FastAPI server   | `uvicorn app:app --reload` |
| Start Streamlit UI     | `streamlit run main.py`    |
| Deactivate environment | `deactivate`               |

---

### ✅ Example Run

```bash
# Open terminal 1
cd server
uvicorn app:app --reload

# Open terminal 2
cd server
streamlit run main.py
```

**Now visit** →
🔹 FastAPI: [http://127.0.0.1:8000](http://127.0.0.1:8000)
🔹 Streamlit UI: [http://localhost:8501](http://localhost:8501)

---

### 💡 Notes

* You can edit `agent.py` to change dialogue templates or event payloads.
* Streamlit UI is for developers only — Godot integration will use the API directly.
* All environment variables are handled via `secrets.py → load_env()`.

---

**Author:** `VR Storytelling — Backend Test Suite`
**Version:** `v0.1.0`
**License:** MIT (for internal testing)

Perfect ✅ — here’s your **final version of `README.md`**
This version adds **cURL test commands** for `/status`, `/chat`, and `/event` endpoints — so you can verify everything directly from the terminal (without Streamlit or Postman).

You can copy and drop this entire file into your `/server/README.md`.

---

# 🧠 VR Story Agent — Local Testing Guide

This document explains how to **set up, test, and run** the Story Agent backend (`FastAPI + LangChain + Groq`)
and its **Streamlit Test UI** for the **VR-Intel-Edu** project.

---
## 🧪 5. Test Endpoints with cURL

These quick commands help you verify that the backend is running correctly.

### ✅ Check Server Status

```bash
curl -X GET http://127.0.0.1:8000/status
```

**Expected Response:**

```json
{
  "status": "ok",
  "message": "We’re still working on the story server. Soon this agent will send JSON scene events directly to Godot to control scenes and narration."
}
```

---

### 💬 Chat with the Story Agent

```bash
curl -X POST http://127.0.0.1:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"user_input":"Hey agent, what are you working on?"}'
```

**Expected Response:**

```json
{
  "agent_reply": "We’re still working on this. Soon the story agent will connect directly with Godot scenes!"
}
```

---

### 🎭 Generate a Scene Event (JSON for Godot)

```bash
curl -X POST http://127.0.0.1:8000/event \
     -H "Content-Type: application/json" \
     -d '{
          "event_id": "evt-001",
          "dialogue": "The turtle looked up at the bright morning sky.",
          "choices": [{"id": "c1", "text": "Start walking"}, {"id": "c2", "text": "Look around"}]
        }'
```

**Expected Response:**

```json
{
  "id": "evt-001",
  "type": "scene_update",
  "bg": "forest_day.png",
  "left": {"sprite": "tortoise_idle.png", "pos": [120, 250], "emotion": "calm"},
  "right": {"sprite": "hare_idle.png", "pos": [420, 250], "emotion": "arrogant"},
  "dialogue": "The turtle looked up at the bright morning sky.",
  "tts": {"voice": "sara-child", "rate": 0.95},
  "choices": [{"id": "c1", "text": "Start walking"}, {"id": "c2", "text": "Look around"}],
  "delay": 2.5,
  "metadata": {"emotion_tag": "neutral", "difficulty": "easy"}
}
```

---

## 🧩 6. Run the Streamlit Test UI

In a **new terminal** (keep FastAPI running), execute:

```bash
streamlit run main.py
```

Streamlit will launch at:
👉 [http://localhost:8501](http://localhost:8501)

### Features:

* Check backend health (`/status`)
* Chat with the agent (`/chat`)
* Generate and inspect event JSONs (`/event`)

---

## 🧰 7. Common Commands

| Purpose        | Command                    |
| -------------- | -------------------------- |
| Create venv    | `uv venv`                  |
| Install deps   | `uv sync`                  |
| Run FastAPI    | `uvicorn app:app --reload` |
| Run Streamlit  | `streamlit run main.py`    |
| Deactivate env | `deactivate`               |
| Reinstall deps | `uv sync --reinstall`      |

