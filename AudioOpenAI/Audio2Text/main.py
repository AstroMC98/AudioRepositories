import os
import sys
import datetime
import openai
import streamlit as st
from audio_recorder_streamlit import audio_recorder


OpenAI_Key = ""
client = openai.OpenAI(api_key=OpenAI_Key)

def transcribe(audio_file):
    transcript = client.audio.transcriptions.create(model="whisper-1", 
                                                    file=audio_file)
    return transcript


def save_audio_file(audio_bytes, file_extension):
    """
    Save audio bytes to a file with the specified extension.

    :param audio_bytes: Audio data in bytes
    :param file_extension: The extension of the output audio file
    :return: The name of the saved audio file
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}.{file_extension}"

    with open(file_name, "wb") as f:
        f.write(audio_bytes)

    return file_name


def transcribe_audio(file_path):
    """
    Transcribe the audio file at the specified path.

    :param file_path: The path of the audio file to transcribe
    :return: The transcribed text
    """
    with open(file_path, "rb") as audio_file:
        transcript = transcribe(audio_file)

    return transcript.text

st.title("Whisper Transcription")

tab1, tab2 = st.tabs(["Record Audio", "Upload Audio"])

# Record Audio tab
with tab1:
    audio_bytes = audio_recorder()
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        save_audio_file(audio_bytes, "mp3")

# Transcribe button action
if st.button("Transcribe"):
    # Find the newest audio file
    audio_file_path = max(
        [f for f in os.listdir(".") if f.startswith("audio")],
        key=os.path.getctime,
    )

    # Transcribe the audio file
    transcript_text = transcribe_audio(audio_file_path)

    # Display the transcript
    st.header("Transcript")
    st.write(transcript_text)

    # Save the transcript to a text file
    with open("transcript.txt", "w") as f:
        f.write(transcript_text)

    # Provide a download button for the transcript
    st.download_button("Download Transcript", transcript_text)