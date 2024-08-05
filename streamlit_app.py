import streamlit as st
import yt_dlp
import os
import io
from pydub import AudioSegment
from demucs import separate
import tempfile
import torchaudio

# Dummy implementation of the separate function for demonstration purposes.
# Replace this with your actual separation logic.
def separate_audio(audio_file_path):
    # Use demucs to separate the audio file
    output_path = tempfile.mkdtemp()  # Create a temporary directory
    separate.main(["--out", output_path, audio_file_path])
    separated_files = []
    # Traverse the output directory to find the separated files
    for root, dirs, files in os.walk(output_path):
        for file in files:
            if file.endswith(".wav"):
                separated_files.append(os.path.join(root, file))
    return separated_files

def download_audio_from_youtube(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': tempfile.mktemp(suffix=".%(ext)s")
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_file = ydl.prepare_filename(info_dict)
    return audio_file

st.title("Audio File/YouTube Audio Downloader and Separator")

option = st.selectbox(
    'Select input type:',
    ('Audio File', 'YouTube Link')
)

if option == 'Audio File':
    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"])
    if audio_file is not None:
        st.audio(audio_file)
        st.write("Audio file uploaded successfully!")
        
        # Save uploaded file to disk
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(audio_file.getbuffer())
            audio_file_path = tmp_file.name
        
        separated_files = separate_audio(audio_file_path)
        
        for file_path in separated_files:
            with open(file_path, "rb") as f:
                st.download_button(
                    label=f"Download {os.path.basename(file_path)}",
                    data=f,
                    file_name=os.path.basename(file_path),
                    mime="audio/wav"
                )

elif option == 'YouTube Link':
    youtube_link = st.text_input("Enter YouTube link")
    if st.button('Download and Separate Audio'):
        if youtube_link:
            with st.spinner('Downloading...'):
                audio_file_path = download_audio_from_youtube(youtube_link)
                st.success('Download complete!')
                
                separated_files = separate_audio(audio_file_path)
                
                for file_path in separated_files:
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label=f"Download {os.path.basename(file_path)}",
                            data=f,
                            file_name=os.path.basename(file_path),
                            mime="audio/wav"
                        )
        else:
            st.error("Please enter a valid YouTube link")
