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
        self.root=root
        self.root.title("YouTube Audio Downloader")
        self.root.geometry("+-5+0")
        self.root.resizable(0,0)
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)

        main_frame=ctk.CTkFrame(root,fg_color="#101010")
        main_frame.grid(row=0,column=0,sticky="nsew")
        main_frame.columnconfigure(0,weight=1)
        main_frame.columnconfigure(1,weight=1)

        self.link_entry=ctk.CTkEntry(main_frame,width=500,height=40,placeholder_text="Paste YouTube link...",fg_color="#101010",border_color="#ff0000",border_width=1)
        self.link_entry.grid(row=0,column=0,sticky="nsew",pady=(10,5),padx=(10,5))

        self.download_button=ctk.CTkButton(main_frame,width=130,height=40,text="Download",command=self.download_audio,fg_color="#101010",border_color="#ff0000",border_width=1,hover_color="#990000")
        self.download_button.grid(row=0,column=1,sticky="nsew",pady=(10,5),padx=(0,10))

        self.console=ctk.CTkTextbox(main_frame,height=300,wrap="word",fg_color="#101010",border_color="#ff0000",border_width=1)
        self.console.grid(row=1,column=0,columnspan=2,sticky="nsew",pady=(0,10),padx=(10,10))

        # self.progress_label=ctk.CTkLabel(randFrame,text="Progress:")
        # self.progress_label.pack()

        # self.progress_bar=ctk.CTkProgressBar(randFrame,width=400)
        # self.progress_bar.pack(pady=(5,5))
        # self.progress_bar.set(0)

        # self.speed_label=ctk.CTkLabel(randFrame,text="Speed: 0 KB/s")
        # self.speed_label.pack()

        # self.console=ctk.CTkTextbox(main_frame)
        # self.console.grid(row=1,column=0,sticky="nsew",columnspan=2)

   

    def log_to_console(self,message):
        self.console.insert("end",f"{message}\n")
        self.console.see("end")

    def download_audio(self):
        link=self.link_entry.get().strip()
        if not link:
            self.log_to_console("Error: Please enter a YouTube link.")
            return

        threading.Thread(target=self.start_download, args=(link,)).start()

    def start_download(self, link):
        try:
            self.log_to_console("Initializing download...")
            downloads_path=str(Path.home() / "Downloads")
            command=[
                "yt-dlp", "-x", "--audio-format", "mp3",
                "--ffmpeg-location", "c:/Users/<username>/ffmpeg-full_build/bin",
                "-o", f"{downloads_path}/%(title)s.%(ext)s", link,
            ]

            process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            start_time=time.time()

            for line in process.stdout:
                if "downloaded" in line.lower():
                    self.log_to_console(line.strip())
                elif "speed" in line.lower():
                    self.log_to_console(line.strip())

            process.wait()
            elapsed_time=time.time()-start_time

            if process.returncode==0:
                self.log_to_console(f"COMPLETED! Total time: {elapsed_time:.2f} seconds.")
            else:
                self.log_to_console("Error: Download failed.")

        except Exception as e:
            self.log_to_console(f"Error: An unexpected error occurwhite: {e}")

    def on_progress(self,stream,chunk,bytes_remaining):
        total_size=stream.filesize
        bytes_downloaded=total_size-bytes_remaining
        percentage=bytes_downloaded/total_size
        self.progress_bar.set(percentage)

        #Calculate speed
        elapsed_time=time.time()-stream._start_time
        if elapsed_time>0:
            speed=bytes_downloaded/elapsed_time/1024  # KBps
            self.speed_label.configure(text=f"Speed: {speed:.2f} KB/s")

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    app_root=ctk.CTk()
    app=YouTubeAudioDownloader(app_root)
    app_root.mainloop()
