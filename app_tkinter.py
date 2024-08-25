import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import yt_dlp
import os
import io
import zipfile
import tempfile
from pydub import AudioSegment
from demucs import separate
import torchaudio

class AudioSeparatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Stem Track Separator")
        self.geometry("400x200")
        
        self.option = tk.StringVar(value="Audio File")
        self.create_widgets()
        self.separated_files = None
        self.track_title = "separated_files"  # Default title if none is available

    def create_widgets(self):
        tk.Label(self, text="Select input type:").pack()

        tk.Radiobutton(self, text="Audio File", variable=self.option, value="Audio File", command=self.update_interface).pack(anchor=tk.W)
        tk.Radiobutton(self, text="YouTube Link", variable=self.option, value="YouTube Link", command=self.update_interface).pack(anchor=tk.W)

        self.file_button = tk.Button(self, text="Upload an audio file", command=self.upload_audio_file)
        self.file_button.pack(pady=10)

        self.youtube_link_entry = tk.Entry(self, width=50)
        self.youtube_link_entry.pack(pady=10)

        self.process_button = tk.Button(self, text="Process", command=self.start_processing)
        self.process_button.pack(pady=10)

        self.download_button = tk.Button(self, text="Download All Separated Files", command=self.download_files)
        self.download_button.pack(pady=10)
        self.download_button.config(state=tk.DISABLED)

        self.update_interface()  # Initial update to set correct visibility

    def update_interface(self):
        if self.option.get() == "Audio File":
            self.file_button.pack(pady=10)
            self.youtube_link_entry.pack_forget()
        else:
            self.file_button.pack_forget()
            self.youtube_link_entry.pack(pady=10)

    def upload_audio_file(self):
        filetypes = (("Audio files", "*.mp3 *.wav *.ogg"),)
        self.audio_file_path = filedialog.askopenfilename(filetypes=filetypes)
        if self.audio_file_path:
            self.track_title = os.path.splitext(os.path.basename(self.audio_file_path))[0]
            messagebox.showinfo("Info", "Audio file uploaded successfully!")

    def download_audio_from_youtube(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': tempfile.mktemp(suffix=".%(ext)s")
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            audio_file = ydl.prepare_filename(info_dict)
            self.track_title = info_dict.get('title', 'separated_files')  # Get title from metadata
        return audio_file

    def start_processing(self):
        threading.Thread(target=self.process_audio).start()

    def process_audio(self):
        if self.option.get() == "Audio File":
            if not hasattr(self, 'audio_file_path'):
                messagebox.showerror("Error", "No audio file uploaded.")
                return
            self.separated_files = self.separate_audio(self.audio_file_path)
        elif self.option.get() == "YouTube Link":
            youtube_link = self.youtube_link_entry.get()
            if not youtube_link:
                messagebox.showerror("Error", "Please enter a valid YouTube link.")
                return
            audio_file_path = self.download_audio_from_youtube(youtube_link)
            self.separated_files = self.separate_audio(audio_file_path)

        if self.separated_files:
            messagebox.showinfo("Info", "Audio processing complete!")
            self.download_button.config(state=tk.NORMAL)

    def separate_audio(self, audio_file_path):
        output_path = tempfile.mkdtemp()
        separate.main(["--out", output_path, audio_file_path])
        separated_files = []
        for root, dirs, files in os.walk(output_path):
            for file in files:
                if file.endswith(".wav"):
                    separated_files.append(os.path.join(root, file))
        return separated_files

    def create_zip(self, separated_files):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in separated_files:
                zip_file.write(file_path, os.path.basename(file_path))
        zip_buffer.seek(0)
        return zip_buffer

    def download_files(self):
        if not self.separated_files:
            messagebox.showerror("Error", "No files to download.")
            return

        # Set the default filename based on the track title
        default_filename = f"{self.track_title}.zip"

        # Prompt the user to choose a location and name for the ZIP file
        save_path = filedialog.asksaveasfilename(
            defaultextension=".zip", 
            filetypes=[("ZIP files", "*.zip")],
            initialfile=default_filename,  # Set the default file name
            title="Save Separated Files As"
        )

        if save_path:  # Check if the user selected a path
            zip_buffer = self.create_zip(self.separated_files)
            with open(save_path, "wb") as f:
                f.write(zip_buffer.read())
            messagebox.showinfo("Info", f"Files saved as {save_path}")

if __name__ == "__main__":
    app = AudioSeparatorApp()
    app.mainloop()
