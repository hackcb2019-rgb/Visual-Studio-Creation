import tkinter as tk
from tkinter import filedialog
import vlc
import os

# Initialize a highly-stable VLC media engine player instance
vlc_instance = vlc.Instance()
vlc_player = vlc_instance.media_player_new()

def save_file(event=None):
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, "w") as file:
            file.write(text_area.get("1.0", tk.END))
        root.title(f"Custom Notepad - {filepath}")

def open_file(event=None):
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, "r") as file:
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", file.read())
        root.title(f"Custom Notepad - {filepath}")

# Music Player Functions (Powered entirely by VLC)
def load_song(event=None):
    song_path = filedialog.askopenfilename(filetypes=[("Media Files", "*.mp3 *.wav *.ogg *.mp4 *.mkv *.avi")])
    if song_path:
        # Safety conversion check for structural Tkinter tuple path variations
        if isinstance(song_path, (tuple, list)):
            if len(song_path) > 0:
                song_path = song_path[0]
            else:
                return
        
        song_path = str(song_path)
        stop_song()
        
        # Parse extensions to cleanly split text layout or video frames dynamically
        ext = os.path.splitext(song_path).lower()
        song_name = os.path.basename(song_path)
        
        if ext in [".mp4", ".mkv", ".avi"]:
            # Slide video layout screen container onto display grid rows
            text_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            video_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
            main_split.grid_columnconfigure(1, weight=1)
            root.update()
            
            win_id = video_frame.winfo_id()
            if os.name == 'nt':  # Windows
                vlc_player.set_hwnd(win_id)
            else:  # Linux/Mac
                vlc_player.set_xwindow(win_id)
            status_label.config(text=f"🎬 Playing Video: {song_name}")
        else:
            # Drop structural frame references to cleanly keep fullscreen text space for music
            video_frame.grid_forget()
            main_split.grid_columnconfigure(1, weight=0)
            text_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
            
            if os.name == 'nt':
                vlc_player.set_hwnd(0)
            else:
                vlc_player.set_xwindow(0)
            status_label.config(text=f"🎵 Playing Audio: {song_name}")
            
        media = vlc_instance.media_new(song_path)
        vlc_player.set_media(media)
        vlc_player.play()
        
        # Match volume configuration tracking values
        set_volume(vol_slider.get())

def stop_song(event=None):
    vlc_player.stop()
    status_label.config(text="Music Stopped")

def toggle_pause(event=None):
    vlc_player.pause()
    if vlc_player.is_playing():
        status_label.config(text="Media Playing")
    else:
        status_label.config(text="Media Paused")

def increase_volume(event=None):
    current_vol = vol_slider.get()
    new_vol = min(current_vol + 5, 100)
    vol_slider.set(new_vol)
    set_volume(new_vol)

def decrease_volume(event=None):
    current_vol = vol_slider.get()
    new_vol = max(current_vol - 5, 0)
    vol_slider.set(new_vol)
    set_volume(new_vol)

def set_volume(val):
    volume_int = int(val)
    vlc_player.audio_set_volume(volume_int)

# GUI Setup
root = tk.Tk()
root.title("Custom Notepad with Media Player")
root.geometry("1100x650")
root.configure(bg="#2d2d2d")

# Keyboard Shortcut Bindings
root.bind("<Control-o>", open_file)
root.bind("<Control-s>", save_file)
root.bind("<Control-m>", load_song)
root.bind("<Control-p>", toggle_pause)
root.bind("<Control-q>", stop_song)
root.bind("<Control-Up>", increase_volume)
root.bind("<Control-Down>", decrease_volume)

# Main Grid View Workspace layout split wrapper
main_split = tk.Frame(root, bg="#2d2d2d")
main_split.pack(expand=True, fill="both", padx=5, pady=5)
main_split.grid_rowconfigure(0, weight=1)
main_split.grid_columnconfigure(0, weight=1)
main_split.grid_columnconfigure(1, weight=1)

# Left Block Section Layout Frame (Text Pad Editor Component)
text_frame = tk.Frame(main_split, bg="#2d2d2d")
text_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

text_area = tk.Text(text_frame, bg="#1e1e1e", fg="#ffffff", insertbackground="white", font=("Consolas", 12), undo=True)
text_area.pack(expand=True, fill="both")

# Right Block Section Layout Frame (Video Screening Component Container Box)
video_frame = tk.Frame(main_split, bg="black", width=540, height=380)
video_frame.grid_propagate(False)

# --- Media Player Panel ---
media_frame = tk.Frame(root, bg="#333333", bd=2, relief=tk.GROOVE)
media_frame.pack(fill="x", side="bottom", padx=5, pady=5)

# Song Title Label
status_label = tk.Label(media_frame, text="No song loaded  (Ctrl+M to Load)", bg="#333333", fg="#00ffcc", font=("Arial", 10, "bold"))
status_label.pack(anchor="w", padx=10, pady=2)

# Control Buttons Sub-Frame
btn_frame = tk.Frame(media_frame, bg="#333333")
btn_frame.pack(side="left", padx=10, pady=5)

load_btn = tk.Button(btn_frame, text="🎵 Load Song", command=load_song, bg="#444444", fg="white", bd=0, padx=10, pady=5)
load_btn.pack(side="left", padx=2)

play_btn = tk.Button(btn_frame, text="⏯ Play/Pause", command=toggle_pause, bg="#444444", fg="white", bd=0, padx=10, pady=5)
play_btn.pack(side="left", padx=2)

stop_btn = tk.Button(btn_frame, text="⏹ Stop", command=stop_song, bg="#d9534f", fg="white", bd=0, padx=10, pady=5)
stop_btn.pack(side="left", padx=2)

# Volume Control Slider
vol_frame = tk.Frame(media_frame, bg="#333333")
vol_frame.pack(side="right", padx=20, pady=5)

vol_label = tk.Label(vol_frame, text="Volume: ", bg="#333333", fg="white")
vol_label.pack(side="left")

vol_slider = tk.Scale(vol_frame, from_=0, to=100, orient="horizontal", command=set_volume, bg="#333333", fg="white", highlightthickness=0, length=130)
vol_slider.set(70) 
vol_slider.pack(side="left")

# File Menu Bar (Updated with shortcut labels)
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open Text File    (Ctrl+O)", command=open_file)
file_menu.add_command(label="Save Text File    (Ctrl+S)", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

root.config(menu=menu_bar)
root.mainloop()
