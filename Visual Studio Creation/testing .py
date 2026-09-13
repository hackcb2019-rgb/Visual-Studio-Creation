import pygame
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
import random

# Initialize pygame mixer
pygame.mixer.init()

playlist = []
current_index = 0
repeat_mode = False
shuffle_mode = False

# ---------------- Media Player Functions ----------------
def add_songs():
    files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav")])
    for f in files:
        playlist.append(f)
    update_playlist_box()

def update_playlist_box():
    playlist_box.delete(0, tk.END)
    for song in playlist:
        playlist_box.insert(tk.END, song.split("/")[-1])

def play_song():
    global current_index
    if playlist:
        song = playlist[current_index]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        song_label.config(text=f"Playing: {song.split('/')[-1]}")

def pause_song():
    pygame.mixer.music.pause()

def resume_song():
    pygame.mixer.music.unpause()

def stop_song():
    pygame.mixer.music.stop()
    song_label.config(text="Stopped")

def next_song():
    global current_index
    if playlist:
        if shuffle_mode:
            current_index = random.randint(0, len(playlist)-1)
        else:
            current_index = (current_index + 1) % len(playlist)
        play_song()

def prev_song():
    global current_index
    if playlist:
        current_index = (current_index - 1) % len(playlist)
        play_song()

def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

def toggle_repeat():
    global repeat_mode
    repeat_mode = not repeat_mode
    repeat_button.config(text=f"Repeat: {'ON' if repeat_mode else 'OFF'}")

def toggle_shuffle():
    global shuffle_mode
    shuffle_mode = not shuffle_mode
    shuffle_button.config(text=f"Shuffle: {'ON' if shuffle_mode else 'OFF'}")

def update_progress():
    if pygame.mixer.music.get_busy():
        pos = pygame.mixer.music.get_pos() / 1000
        progress_var.set(pos)
    root.after(1000, update_progress)

def seek_song(val):
    if playlist:
        pygame.mixer.music.play(start=float(val))

# ---------------- Notepad Functions ----------------
def new_file():
    text_area.delete(1.0, tk.END)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as f:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, f.read())

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write(text_area.get(1.0, tk.END))

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Smart Media Player + Notepad")

# Frames
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Playlist box
playlist_box = tk.Listbox(left_frame, width=40)
playlist_box.pack(pady=10)

# Media Player Buttons
tk.Button(left_frame, text="Add Songs", command=add_songs).pack(pady=5)
tk.Button(left_frame, text="Play", command=play_song).pack(pady=5)
tk.Button(left_frame, text="Pause", command=pause_song).pack(pady=5)
tk.Button(left_frame, text="Resume", command=resume_song).pack(pady=5)
tk.Button(left_frame, text="Stop", command=stop_song).pack(pady=5)
tk.Button(left_frame, text="Previous", command=prev_song).pack(pady=5)
tk.Button(left_frame, text="Next", command=next_song).pack(pady=5)

shuffle_button = tk.Button(left_frame, text="Shuffle: OFF", command=toggle_shuffle)
shuffle_button.pack(pady=5)
repeat_button = tk.Button(left_frame, text="Repeat: OFF", command=toggle_repeat)
repeat_button.pack(pady=5)

volume_slider = ttk.Scale(left_frame, from_=0, to=100, orient="horizontal", command=set_volume)
volume_slider.set(70)
volume_slider.pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Scale(left_frame, from_=0, to=300, orient="horizontal", variable=progress_var, command=seek_song)
progress_bar.pack(pady=10)

song_label = tk.Label(left_frame, text="No song playing")
song_label.pack(pady=10)

# Keyboard shortcuts
root.bind("<space>", lambda e: pause_song() if pygame.mixer.music.get_busy() else play_song())
root.bind("<Right>", lambda e: next_song())
root.bind("<Left>", lambda e: prev_song())

# Notepad area
text_area = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=50, height=25)
text_area.pack()

# Notepad buttons
tk.Button(right_frame, text="New", command=new_file).pack(pady=5)
tk.Button(right_frame, text="Open", command=open_file).pack(pady=5)
tk.Button(right_frame, text="Save", command=save_file).pack(pady=5)

update_progress()
root.mainloop()
