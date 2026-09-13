import os
import shutil

# Specify the main directories you want to clean up.
# You can add or remove folders here.
TARGET_DIRECTORIES = [
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Documents")
]

# File category map
EXTENSIONS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Executables_and_Setup": [".exe", ".msi", ".bat", ".apk"],
    "Audio": [".mp3", ".wav", ".flac", ".m4a"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"]
}

def move_file_safely(src, dest_folder, filename):
    """Moves a file safely without overwriting existing files of the same name."""
    os.makedirs(dest_folder, exist_ok=True)
    target_path = os.path.join(dest_folder, filename)

    # If a file with the same name exists, append a number counter
    if os.path.exists(target_path):
        name, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(dest_folder, f"{name}_{counter}{ext}")):
            counter += 1
        target_path = os.path.join(dest_folder, f"{name}_{counter}{ext}")

    try:
        shutil.move(src, target_path)
        print(f"[SUCCESS] Moved: {filename} -> {os.path.basename(dest_folder)}/")
    except Exception as e:
        print(f"[ERROR] Could not move {filename}: {e}")

def organize_directory(base_path):
    """Scans and organizes files within a specified base directory."""
    if not os.path.exists(base_path):
        print(f"[SKIP] Path does not exist: {base_path}")
        return

    print(f"\n--- Organizing Directory: {base_path} ---")
    
    # Get category names to prevent moving already organized folders into themselves
    category_folders = set(EXTENSIONS.keys())

    for filename in os.listdir(base_path):
        file_path = os.path.join(base_path, filename)

        # Skip directories (so created category folders stay intact)
        if os.path.isdir(file_path):
            continue

        ext = os.path.splitext(filename)[1].lower()
        
        # Match file extension to category
        for folder_name, ext_list in EXTENSIONS.items():
            if ext in ext_list:
                target_dir = os.path.join(base_path, folder_name)
                move_file_safely(file_path, target_dir, filename)
                break

if __name__ == "__main__":
    for folder in TARGET_DIRECTORIES:
        organize_directory(folder)
        
    print("\nSystem Organization Complete!")