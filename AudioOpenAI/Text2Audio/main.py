import os
import base64
import openai
import streamlit as st
from pathlib import Path
from openai import OpenAI


OpenAI_Key = ""
client = openai.OpenAI(api_key=OpenAI_Key)

# Supported voices (replace with actual voice names from OpenAI documentation)
supported_voices = ["onyx", "alloy", "fable", "echo", "nova", "shimmer"]

def generate_speech(text, selected_voice="onyx"):
  """
  Generates audio using OpenAI Text-to-Speech API.

  Args:
      text: The text to convert to speech.
      voice: The voice to use (default: onyx).

  Returns:
      A byte string containing the generated audio data.
  """
  response = client.audio.speech.create(
      model="tts-1",  # Adjust model based on needs
      voice=selected_voice,
      input=text,
  )
  return response

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )
        
st.title("OpenAI Text-to-Speech")

# Text input for user prompt
user_text = st.text_area("Enter the text to convert to speech:")

# Select voice dropdown
selected_voice = st.selectbox("Select Voice", supported_voices)

# Generate audio button
if st.button("Generate Audio"):
  with st.spinner("Generating audio..."):
    audio_data = generate_speech(user_text, selected_voice)

  # Download button if audio generated
  if audio_data:
    # Create temporary file for audio data
    speech_file_path = Path(__file__).parent / "speech.mp3"
    audio_data.stream_to_file(speech_file_path)
    autoplay_audio(speech_file_path)