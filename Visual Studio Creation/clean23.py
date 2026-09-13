import os
import sys
import shutil
import ctypes
import threading
import customtkinter as ctk

# Configure GUI appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Targets to clean
USER_PROFILE = os.environ.get("USERPROFILE", "C:\\Users\\Default")
TARGET_FOLDERS = {
    "User Temp": os.environ.get("TEMP"),
    "System Temp": "C:\\Windows\\Temp",
    "Prefetch": "C:\\Windows\\Prefetch",
    "Software Downloads": "C:\\Windows\\SoftwareDistribution\\Download"
}

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

class SystemCleanerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("⚡ Windows Storage Optimizer")
        self.geometry("600 x 480")
        self.resizable(False, False)

        # Header Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="STORAGE OPTIMIZER", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#60A5FA"
        )
        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="Scan and purge unused temporary system cache", 
            font=ctk.CTkFont(size=12)
        )
        self.subtitle_label.pack(pady=(0, 20))

        # Status Display Box
        self.status_card = ctk.CTkFrame(self, width=520, height=140, corner_radius=12)
        self.status_card.pack(pady=10)
        self.status_card.pack_propagate(False)

        self.junk_size_label = ctk.CTkLabel(
            self.status_card, 
            text="-- MB", 
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#F87171"
        )
        self.junk_size_label.pack(pady=(25, 0))

        self.status_detail_label = ctk.CTkLabel(
            self.status_card, 
            text="Click 'Scan Drive' to calculate cleanable space", 
            font=ctk.CTkFont(size=12)
        )
        self.status_detail_label.pack(pady=(5, 10))

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self, width=520, height=12)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=20)

        # Action Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.scan_btn = ctk.CTkButton(
            self.button_frame, 
            text="🔍 Scan Drive", 
            width=160, 
            height=40,
            command=self.start_scan_thread
        )
        self.scan_btn.grid(row=0, column=0, padx=10)

        self.clean_btn = ctk.CTkButton(
            self.button_frame, 
            text="⚡ Clean Junk", 
            width=160, 
            height=40,
            fg_color="#10B981",
            hover_color="#059669",
            state="disabled",
            command=self.start_clean_thread
        )
        self.clean_btn.grid(row=0, column=1, padx=10)

        # Log Output Console
        self.log_box = ctk.CTkTextbox(self, width=520, height=100, font=ctk.CTkFont(size=11))
        self.log_box.pack(pady=15)
        self.log("Ready. Click 'Scan Drive' to start.")

        self.total_bytes = 0
        self.total_files = 0

    def log(self, text):
        self.log_box.insert("end", f"{text}\n")
        self.log_box.see("end")

    # --- Scanning Logic ---
    def start_scan_thread(self):
        self.scan_btn.configure(state="disabled")
        self.clean_btn.configure(state="disabled")
        self.progress_bar.set(0)
        threading.Thread(target=self.scan_drive, daemon=True).start()

    def scan_drive(self):
        self.log("\n--- Starting Deep Scan ---")
        self.total_bytes = 0
        self.total_files = 0

        for name, path in TARGET_FOLDERS.items():
            if path and os.path.exists(path):
                folder_bytes = 0
                folder_files = 0
                for root, _, files in os.walk(path):
                    for f in files:
                        try:
                            fp = os.path.join(root, f)
                            folder_bytes += os.path.getsize(fp)
                            folder_files += 1
                        except Exception:
                            pass
                self.total_bytes += folder_bytes
                self.total_files += folder_files
                size_mb = folder_bytes / (1024 * 1024)
                self.log(f"Found {folder_files} files in {name} (~{size_mb:.2f} MB)")

        total_mb = self.total_bytes / (1024 * 1024)
        self.junk_size_label.configure(text=f"{total_mb:.2f} MB")
        self.status_detail_label.configure(text=f"{self.total_files} junk files detected across system folders")

        self.scan_btn.configure(state="normal")
        if self.total_files > 0:
            self.clean_btn.configure(state="normal")
        else:
            self.log("System is completely clean!")

    # --- Cleaning Logic ---
    def start_clean_thread(self):
        self.scan_btn.configure(state="disabled")
        self.clean_btn.configure(state="disabled")
        threading.Thread(target=self.clean_drive, daemon=True).start()

    def clean_drive(self):
        self.log("\n--- Starting Purge Process ---")
        freed_bytes = 0
        deleted_files = 0
        total_targets = len(TARGET_FOLDERS)

        for idx, (name, path) in enumerate(TARGET_FOLDERS.items(), 1):
            if path and os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for f in files:
                        fp = os.path.join(root, f)
                        try:
                            sz = os.path.getsize(fp)
                            os.remove(fp)
                            freed_bytes += sz
                            deleted_files += 1
                        except Exception:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except Exception:
                            pass
            
            progress = idx / total_targets
            self.progress_bar.set(progress)
            self.log(f"Cleaned category: {name}")

        freed_mb = freed_bytes / (1024 * 1024)
        self.junk_size_label.configure(text="0.00 MB", text_color="#10B981")
        self.status_detail_label.configure(text=f"Successfully freed ~{freed_mb:.2f} MB of disk space!")
        self.log(f"\nSUCCESS: Removed {deleted_files} files.")
        self.scan_btn.configure(state="normal")


if __name__ == "__main__":
    if not is_admin():
        # Auto-request Administrator permissions
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{os.path.abspath(__file__)}"', None, 1
        )
    else:
        app = SystemCleanerApp()
        app.mainloop()