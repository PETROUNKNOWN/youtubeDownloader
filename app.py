import os
import time
import threading
import customtkinter as ctk
import subprocess
from pytube import YouTube
from tkinter import messagebox
from pathlib import Path

class YouTubeAudioDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Audio Downloader")
        self.root.geometry("500x200")

        self.link_label = ctk.CTkLabel(root, text="YouTube Link:")
        self.link_label.pack(pady=(10, 0))

        self.link_entry = ctk.CTkEntry(root, width=400)
        self.link_entry.pack(pady=(5, 10))

        self.download_button = ctk.CTkButton(root, text="Download", command=self.download_audio)
        self.download_button.pack(pady=(5, 10))

        self.progress_label = ctk.CTkLabel(root, text="Progress:")
        self.progress_label.pack()

        self.progress_bar = ctk.CTkProgressBar(root, width=400)
        self.progress_bar.pack(pady=(5, 5))
        self.progress_bar.set(0)

        self.speed_label = ctk.CTkLabel(root, text="Speed: 0 KB/s")
        self.speed_label.pack()

    def download_audio(self):
        link = self.link_entry.get()
        if not link:
            messagebox.showerror("Error", "Please enter a YouTube linK.")
            return

        threading.Thread(target=self.start_download, args=(link,)).start()

    def start_download(self, link):
        try:
            self.progress_bar.set(0)
            self.speed_label.configure(text="Speed: Calculating...")
            
            downloads_path = str(Path.home() / "Downloads")
            command = [
                "yt-dlp", "-x", "--audio-format", "mp3",
                "--ffmpeg-location", "c:/Users/petro/Downloads/ffmpeg-2025-01-08-git-251de1791e-full_build/ffmpeg-2025-01-08-git-251de1791e-full_build/bin",
                "-o", f"{downloads_path}/%(title)s.%(ext)s", link,
            ]
            
            subprocess.run(command, check=True)
            
            self.progress_bar.set(1)
            self.progress_bar.configure(progress_color="green")
            messagebox.showinfo("Success", "Download complete!")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = bytes_downloaded / total_size
        self.progress_bar.set(percentage)

        # Calculate speed
        elapsed_time = time.time() - stream._start_time
        if elapsed_time > 0:
            speed = bytes_downloaded / elapsed_time / 1024  # KBps
            self.speed_label.configure(text=f"Speed: {speed:.2f} KB/s")

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app_root = ctk.CTk()
    app = YouTubeAudioDownloader(app_root)
    app_root.mainloop()
