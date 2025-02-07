import streamlit as st
import edge_tts
import asyncio
import librosa
import soundfile as sf
import time
import numpy as np
from io import BytesIO

# Function to Convert Text to Speech with More Voice Options
async def text_to_speech(text, voice="en-US-GuyNeural"):
    filename = f"audio_{int(time.time())}.mp3"
    
    # Use Edge TTS to generate speech
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)
    
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

# User Input for Text
st.subheader("Enter Your Text")
text = st.text_area("📝 Type or paste your text below:")

# Select Voice Type
st.subheader("Select Voice Type")
voice_options = {
    "Male (US)": "en-US-GuyNeural",
    "Male (UK)": "en-GB-RyanNeural",
    "Female (US)": "en-US-JennyNeural",
    "Female (UK)": "en-GB-SoniaNeural"
}
selected_voice = st.selectbox("🎭 Choose a Voice:", list(voice_options.keys()))

if st.button("🎙️ Generate Voice"):
    if text:
        st.info("⏳ Processing your request... Please wait.")
        
        # Generate Speech
        audio_file = asyncio.run(text_to_speech(text, voice_options[selected_voice]))
        
        st.success("✅ Voice generated successfully!")
        st.audio(audio_file, format='audio/mp3')

        # Allow users to download the generated audio
        with open(audio_file, "rb") as file:
            audio_bytes = file.read()
        
        st.download_button(label="⬇️ Download Audio", data=audio_bytes, 
                           file_name=audio_file, mime="audio/mp3")
    else:
        st.warning("⚠️ Please enter text to generate voice.")

st.markdown("---")
st.caption("🔹 **Supports high-quality male & female voices with different accents.**")
st.caption("🔹 **Runs offline using Edge TTS for fast voice generation.**")
st.divider()
st.caption("👻 So called Arman.")
