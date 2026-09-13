import tkinter as tk
from tkinter import filedialog, messagebox
import pygame

# Initialize pygame mixer for audio
pygame.mixer.init()

def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, "w") as file:
            file.write(text_area.get("1.0", tk.END))
        root.title(f"Custom Notepad - {filepath}")

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, "r") as file:
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", file.read())
        root.title(f"Custom Notepad - {filepath}")

# Music Player Functions
def load_song():
    song_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
    if song_path:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        # Extract and display just the file name
        song_name = song_path.split("/")[-1]
        status_label.config(text=f"Playing: {song_name}")

def stop_song():
    pygame.mixer.music.stop()
    status_label.config(text="Music Stopped")

def pause_song():
    pygame.mixer.music.pause()
    status_label.config(text="Music Paused")

def unpause_song():
    pygame.mixer.music.unpause()
    status_label.config(text="Music Resumed")

def set_volume(val):
    # Convert slider value (0-100) to pygame volume scale (0.0-1.0)
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

# GUI Setup
root = tk.Tk()
root.title("Custom Notepad with Media Player")
root.geometry("700x550")
root.configure(bg="#2d2d2d")

# Text Layout Area
text_area = tk.Text(root, bg="#1e1e1e", fg="#ffffff", insertbackground="white", font=("Consolas", 12))
text_area.pack(expand=True, fill="both", padx=5, pady=5)

# --- Media Player Panel ---
media_frame = tk.Frame(root, bg="#333333", bd=2, relief=tk.GROOVE)
media_frame.pack(fill="x", side="bottom", padx=5, pady=5)

# Song Title Label
status_label = tk.Label(media_frame, text="No song loaded", bg="#333333", fg="#00ffcc", font=("Arial", 10, "bold"))
status_label.pack(anchor="w", padx=10, pady=2)

# Control Buttons Sub-Frame
btn_frame = tk.Frame(media_frame, bg="#333333")
btn_frame.pack(side="left", padx=10, pady=5)

load_btn = tk.Button(btn_frame, text="🎵 Load Song", command=load_song, bg="#444444", fg="white", bd=0, padx=8, pady=4)
load_btn.pack(side="left", padx=2)

play_btn = tk.Button(btn_frame, text="▶ Resume", command=unpause_song, bg="#444444", fg="white", bd=0, padx=8, pady=4)
play_btn.pack(side="left", padx=2)

pause_btn = tk.Button(btn_frame, text="⏸ Pause", command=pause_song, bg="#444444", fg="white", bd=0, padx=8, pady=4)
pause_btn.pack(side="left", padx=2)

stop_btn = tk.Button(btn_frame, text="⏹ Stop", command=stop_song, bg="#d9534f", fg="white", bd=0, padx=8, pady=4)
stop_btn.pack(side="left", padx=2)

# Volume Control Slider
vol_frame = tk.Frame(media_frame, bg="#333333")
vol_frame.pack(side="right", padx=20, pady=5)

vol_label = tk.Label(vol_frame, text="Volume: ", bg="#333333", fg="white")
vol_label.pack(side="left")

vol_slider = tk.Scale(vol_frame, from_=0, to=100, orient="horizontal", command=set_volume, bg="#333333", fg="white", highlightthickness=0, length=120)
vol_slider.set(70) # Set starting volume to 70%
vol_slider.pack(side="left")

# File Menu Bar
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open Text File", command=open_file)
file_menu.add_command(label="Save Text File", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

root.config(menu=menu_bar)
root.mainloop()
