"""Command to run: streamlit run streamlit_app.py"""

import streamlit as st
import yt_dlp
import os
import io
import zipfile
import tempfile
from pydub import AudioSegment
from demucs import separate
import torchaudio

# Dummy implementation of the separate function for demonstration purposes.
def separate_audio(audio_file_path):
    # Using demucs to separate the audio file
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

def create_zip(separated_files):
    # Create a BytesIO object to hold the ZIP data
    zip_buffer = io.BytesIO()
    
    # Create a ZIP file in the BytesIO object
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in separated_files:
            # Add each file to the ZIP archive
            zip_file.write(file_path, os.path.basename(file_path))
    
    # Seek to the beginning of the BytesIO object
    zip_buffer.seek(0)
    return zip_buffer

st.title("Simple Stem Track Separator")
st.write("""
Hi, this is a simple app that allows you to input a song and processes it into multiple stems. 
It's using project Demucs by Alexandre Défossez as the separation engine.
         
At the moment you can input audio files (so if you've got a song, you can drag and drop it there),
it can also download a song directly from **Youtube**, you have to select the YouTube Link option on the 
"Select input type" prompt, then
provide the whole link to the song you want to separate into stems.
         
At the moment, this is using a model that will generate 4 different tracks: 
         
- vocals
- bass
- drums
- others

Feel free to experiment!
""")


# Initialize session state for separated files
if 'separated_files' not in st.session_state:
    st.session_state.separated_files = None

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
        
        if st.button("Process Audio"):
            st.session_state.separated_files = separate_audio(audio_file_path)
            st.write("Audio processing complete!")
        
        if st.session_state.separated_files is not None:
            # Create a zip of the separated files
            zip_buffer = create_zip(st.session_state.separated_files)
            
            st.download_button(
                label="Download All Separated Files",
                data=zip_buffer,
                file_name="separated_files.zip",
                mime="application/zip"
            )

elif option == 'YouTube Link':
    youtube_link = st.text_input("Enter YouTube link")
    if st.button('Download and Separate Audio'):
        if youtube_link:
            with st.spinner('Downloading and processing...'):
                audio_file_path = download_audio_from_youtube(youtube_link)
                st.success('Download complete!')
                
                st.session_state.separated_files = separate_audio(audio_file_path)
                
                # Create a zip of the separated files
                zip_buffer = create_zip(st.session_state.separated_files)
                
                st.download_button(
                    label="Download All Separated Files",
                    data=zip_buffer,
                    file_name="separated_files.zip",
                    mime="application/zip"
                )
        else:
            st.error("Please enter a valid YouTube link")

st.write("Also, feel free to leave some feedback, I'd love to hear back new ideas!")
