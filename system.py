import os
import shutil

WATCH_DIR = os.path.expanduser("~/Downloads")

EXTENSIONS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".csv"],
    "Executables": [".exe", ".msi"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Archives": [".zip", ".rar", ".7z"]
}

def organize_folder():
    for filename in os.listdir(WATCH_DIR):
        file_path = os.path.join(WATCH_DIR, filename)
        if os.path.isdir(file_path):
            continue

        ext = os.path.splitext(filename)[1].lower()
        for folder_name, ext_list in EXTENSIONS.items():
            if ext in ext_list:
                target_dir = os.path.join(WATCH_DIR, folder_name)
                os.makedirs(target_dir, exist_ok=True)
                shutil.move(file_path, os.path.join(target_dir, filename))
                print(f"Moved {filename} -> {folder_name}/")
                break

if __name__ == "__main__":
    organize_folder()