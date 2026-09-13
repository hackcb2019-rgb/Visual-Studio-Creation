import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class DeviceCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Device Storage Analyzer & Cleaner")
        self.root.geometry("550x520")
        self.root.config(bg="#1e1e2e")

        # Title
        title = tk.Label(root, text="⚡ System Storage Cleaner", font=("Helvetica", 16, "bold"), fg="#cba6f7", bg="#1e1e2e")
        title.pack(pady=15)

        # Storage Progress Bar
        self.progress_label = tk.Label(root, text="Checking Storage...", font=("Helvetica", 10), fg="#a6adc8", bg="#1e1e2e")
        self.progress_label.pack(pady=5)
        
        self.progress = ttk.Progressbar(root, orient="horizontal", length=420, mode="determinate")
        self.progress.pack(pady=5)

        # Storage Info Box
        self.info_label = tk.Label(root, text="", font=("Courier", 10), fg="#a6e3a1", bg="#1e1e2e", justify="left")
        self.info_label.pack(pady=10)

        # Buttons Frame
        btn_frame = tk.Frame(root, bg="#1e1e2e")
        btn_frame.pack(pady=10)

        # Control Buttons
        scan_btn = tk.Button(btn_frame, text="🔍 Refresh Storage", command=self.scan_storage, bg="#89b4fa", fg="#11111b", font=("Helvetica", 10, "bold"), padx=10, pady=5)
        scan_btn.grid(row=0, column=0, padx=5)

        clean_btn = tk.Button(btn_frame, text="🧹 Clean Temp Junk", command=self.clean_junk, bg="#f38ba8", fg="#11111b", font=("Helvetica", 10, "bold"), padx=10, pady=5)
        clean_btn.grid(row=0, column=1, padx=5)

        large_files_btn = tk.Button(btn_frame, text="📁 Find Large Files (100MB+)", command=self.find_large_files, bg="#fab387", fg="#11111b", font=("Helvetica", 10, "bold"), padx=10, pady=5)
        large_files_btn.grid(row=0, column=2, padx=5)

        # Large Files Output Window
        self.result_box = tk.Text(root, height=10, width=62, bg="#313244", fg="#cdd6f4", font=("Consolas", 9))
        self.result_box.pack(pady=10)

        self.scan_storage()

    def scan_storage(self):
        total, used, free = shutil.disk_usage("/")
        
        total_gb = round(total / (2**30), 2)
        used_gb = round(used / (2**30), 2)
        free_gb = round(free / (2**30), 2)
        used_percent = round((used / total) * 100, 1)

        self.progress['value'] = used_percent
        self.progress_label.config(text=f"Used Storage: {used_percent}% ({used_gb} GB / {total_gb} GB)")
        
        info_text = f"Total Space : {total_gb} GB\nUsed Space  : {used_gb} GB\nFree Space  : {free_gb} GB"
        self.info_label.config(text=info_text)

    def clean_junk(self):
        temp_dir = os.getenv('TEMP') if os.name == 'nt' else '/tmp'
        deleted_files = 0

        if temp_dir and os.path.exists(temp_dir):
            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        deleted_files += 1
                except Exception:
                    pass
        
        messagebox.showinfo("Success", f"Cleaning Complete!\n{deleted_files} temporary files delete ho gayi.")
        self.scan_storage()

    def find_large_files(self):
        folder_selected = filedialog.askdirectory(title="Folder Select Karein Large Files Search ke Liye")
        if not folder_selected:
            return

        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, f"Scanning folder: {folder_selected}\n\n")
        self.root.update()

        found = False
        limit_bytes = 100 * 1024 * 1024  # 100 MB Limit

        for root_dir, dirs, files in os.walk(folder_selected):
            for file in files:
                filepath = os.path.join(root_dir, file)
                try:
                    size = os.path.getsize(filepath)
                    if size >= limit_bytes:
                        size_mb = round(size / (1024 * 1024), 2)
                        self.result_box.insert(tk.END, f"[{size_mb} MB] {filepath}\n")
                        found = True
                except Exception:
                    pass

        if not found:
            self.result_box.insert(tk.END, "Koi bhi 100MB se badi file nahi mili.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DeviceCleanerApp(root)
    root.mainloop()