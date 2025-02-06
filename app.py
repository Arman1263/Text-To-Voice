import streamlit as st
import pyttsx3
from gtts import gTTS
import os
import librosa
import soundfile as sf
import time
import numpy as np
from io import BytesIO

# Function to Convert Text to Speech
def text_to_speech(text, engine='offline', gender='male'):
    filename = f"audio_{int(time.time())}.wav"
    if engine == 'offline':
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('rate', 160)  # Adjust speed
        tts_engine.setProperty('volume', 2.0)  # Max volume
        voices = tts_engine.getProperty('voices')
        
        if gender == 'male':
            tts_engine.setProperty('voice', voices[0].id)  # Male voice
        else:
            tts_engine.setProperty('voice', voices[1].id)  # Female voice
        
        tts_engine.save_to_file(text, filename)
        tts_engine.runAndWait()
    elif engine == 'online':
        tts = gTTS(text=text, lang='en', slow=False)
        filename = f"audio_{int(time.time())}.mp3"
        tts.save(filename)
    return filename

# Function to Modify Voice Pitch
def change_voice(input_file, gender="male"):
    y, sr = librosa.load(input_file, sr=44100)
    pitch_factor = -3 if gender == "male" else 5  # Adjust pitch naturally
    y_shifted = librosa.effects.pitch_shift(y, n_steps=pitch_factor, sr=sr)
    output_file = f"modified_{int(time.time())}.wav"
    sf.write(output_file, y_shifted, sr)
    return output_file

# Streamlit UI
st.set_page_config(page_title="🎤 Voice Generator App", layout="centered")
st.title("🎤 AI-Powered Voice Generator")
st.markdown("**Convert your text into speech with natural, clear voices!** 🎶")
st.divider()

st.subheader("Enter Your Text")
text = st.text_area("📝 Type or paste your text below:")

st.subheader("Choose Voice Engine")
engine = st.radio("⚙️ Select a Text-to-Speech Engine:", 
                  ["Offline (Fast, Customizable)", "Online (Natural, Requires Internet)"])
engine_mode = "offline" if "Offline" in engine else "online"

st.subheader("Select Voice Type")
gender = st.radio("🎭 Choose Voice Gender:", ["Male", "Female"])

if st.button("🎙️ Generate Voice"):
    if text:
        st.info("⏳ Processing your request... Please wait.")
        audio_file = text_to_speech(text, engine_mode, gender.lower())
        modified_audio = change_voice(audio_file, gender.lower())
        
        st.success("✅ Voice generated successfully!")
        st.audio(modified_audio, format='audio/wav')
        
        with open(modified_audio, "rb") as file:
            audio_bytes = file.read()
        
        st.download_button(label="⬇️ Download Audio", data=audio_bytes, 
                           file_name=modified_audio, mime="audio/wav")
    else:
        st.warning("⚠️ Please enter text to generate voice.")

st.markdown("---")
st.caption("🔹 **Offline Mode** uses your system's built-in voices and works without the internet.")
st.caption("🔹 **Online Mode** uses Google TTS for a more natural voice but requires an internet connection.")
st.divider()
st.caption("👻 So called Arman.")