import os
import shutil
import string

# Define file category mappings
EXTENSIONS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico", ".bmp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".csv"],
    "Executables_and_Setups": [".exe", ".msi", ".bat", ".apk"],
    "Audio": [".mp3", ".wav", ".flac", ".m4a", ".aac"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso"]
}

# Critical system directories that MUST NOT be touched
PROTECTED_PATHS = [
    "windows", "program files", "program files (x86)", "programdata",
    "appdata", "$recycle.bin", "system volume information", "boot",
    "recovery", "msocache"
]

def get_available_drives():
    """Detects all active drive letters on Windows (C:, D:, E:, etc.)."""
    drives = []
    for letter in string.ascii_uppercase:
        drive_path = f"{letter}:\\"
        if os.path.exists(drive_path):
            drives.append(drive_path)
    return drives

def move_file_safely(src, dest_folder, filename):
    """Moves a file to the target category folder safely without overwriting."""
    os.makedirs(dest_folder, exist_ok=True)
    target_path = os.path.join(dest_folder, filename)

    # Handle duplicate file names safely
    if os.path.exists(target_path):
        name, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(dest_folder, f"{name}_{counter}{ext}")):
            counter += 1
        target_path = os.path.join(dest_folder, f"{name}_{counter}{ext}")

    try:
        shutil.move(src, target_path)
        print(f"  [MOVED] {filename} -> {os.path.basename(dest_folder)}/")
    except Exception as e:
        print(f"  [ERROR] Could not move {filename}: {e}")

def is_protected(path):
    """Checks if a given folder path is a protected system directory."""
    path_lower = path.lower()
    for protected in PROTECTED_PATHS:
        if protected in path_lower:
            return True
    return False

def organize_location(target_dir):
    """Organizes loose files directly inside the specified folder."""
    if not os.path.exists(target_dir) or is_protected(target_dir):
        print(f"[SKIP] Protected or invalid directory: {target_dir}")
        return

    print(f"\nScanning: {target_dir}")
    category_folders = set(EXTENSIONS.keys())

    try:
        for filename in os.listdir(target_dir):
            file_path = os.path.join(target_dir, filename)

            # Skip directories so we don't break existing folder structures
            if os.path.isdir(file_path):
                continue

            ext = os.path.splitext(filename)[1].lower()

            # Check matching extension
            for folder_name, ext_list in EXTENSIONS.items():
                if ext in ext_list:
                    target_category_dir = os.path.join(target_dir, folder_name)
                    move_file_safely(file_path, target_category_dir, filename)
                    break
    except PermissionError:
        print(f"[ACCESS DENIED] Skipping {target_dir} (Requires Administrator permissions)")
    except Exception as e:
        print(f"[ERROR] Unable to process {target_dir}: {e}")

def main():
    print("==================================================")
    print("       FULL SYSTEM FILE ORGANIZER UTILITY        ")
    print("==================================================")

    # 1. Target standard User Profile directories
    user_profile = os.path.expanduser("~")
    user_targets = [
        os.path.join(user_profile, "Desktop"),
        os.path.join(user_profile, "Documents"),
        os.path.join(user_profile, "Downloads")
    ]

    print("\n--- Phase 1: Organizing User Profile Folders ---")
    for target in user_targets:
        organize_location(target)

    # 2. Target root directories of available drives (C:\, D:\, E:\, etc.)
    print("\n--- Phase 2: Organizing Drive Roots ---")
    active_drives = get_available_drives()
    print(f"Detected drives: {', '.join(active_drives)}")

    for drive in active_drives:
        organize_location(drive)

    print("\n==================================================")
    print("      SYSTEM FILE ORGANIZATION COMPLETE!         ")
    print("==================================================")

if __name__ == "__main__":
    main()