import streamlit as st
import os
import whisper

# Cache Whisper model (prevents reloading on every Streamlit refresh)
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

model = load_whisper_model()

def save_uploaded_file(uploaded_file, save_path="uploads"):
    # Create folder if not exists
    os.makedirs(save_path, exist_ok=True)

    filepath = os.path.join(save_path, uploaded_file.name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return filepath

def transcribe_audio(filepath):
    result = model.transcribe(filepath)
    transcription = result["text"].strip()
    return transcription
