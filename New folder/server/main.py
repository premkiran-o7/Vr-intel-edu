# main.py
import streamlit as st
import requests
import json

# --- Configuration ---
API_URL = "http://127.0.0.1:8000"  # FastAPI server URL

st.set_page_config(
    page_title="Story Agent Test Console",
    page_icon="🧠",
    layout="centered",
)

st.title("🧠 Story Agent — Test Console")
st.markdown("Interact with your **FastAPI + LangChain (Groq LLaMA3)** backend here.")

# --- Status Section ---
st.subheader("Server Status")
if st.button("Check Server"):
    try:
        resp = requests.get(f"{API_URL}/status", timeout=5)
        if resp.status_code == 200:
            st.success(resp.json().get("message", "Server is up ✅"))
        else:
            st.error(f"Error: {resp.status_code}")
    except Exception as e:
        st.error(f"Server not reachable: {e}")

st.divider()

# --- Chat Section ---
st.subheader("💬 Chat with Agent")

user_input = st.text_area("Type something to the agent:", height=120)

if st.button("Send Message"):
    if not user_input.strip():
        st.warning("Please enter a message first.")
    else:
        with st.spinner("Talking to the agent..."):
            try:
                resp = requests.post(f"{API_URL}/chat", json={"user_input": user_input})
                if resp:
                    st.success("Agent reply:")
                    st.info(resp.json()["agent_reply"])
                else:
                    st.error(f"Error: {resp.status_code}")
            except Exception as e:
                st.error(f"Request failed: {e}")

st.divider()

# --- Event Section ---
st.subheader("🎭 Request Scene Event")

col1, col2 = st.columns(2)
with col1:
    evt_id = st.text_input("Event ID", value="evt-test-001")
with col2:
    dlg = st.text_input("Dialogue", value="We’re still working on connecting with Godot scenes!")

if st.button("Generate Scene Event"):
    with st.spinner("Building event JSON..."):
        try:
            resp = requests.post(
                f"{API_URL}/event",
                json={"event_id": evt_id, "dialogue": dlg},
            )
            if resp.status_code == 200:
                event_json = resp.json()
                st.success("Event JSON:")
                st.json(event_json)
            else:
                st.error(f"Error: {resp.status_code}")
        except Exception as e:
            st.error(f"Request failed: {e}")

st.caption("💡 Use this to simulate what the Godot client will receive and apply in scenes.")
