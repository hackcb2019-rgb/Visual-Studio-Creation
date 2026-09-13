import os
import shutil
import tempfile

def clean_directory(folder_path):
    """Deletes files and subdirectories inside a given folder."""
    if not os.path.exists(folder_path):
        print(f"Directory not found: {folder_path}")
        return

    print(f"\n--- Cleaning: {folder_path} ---")
    deleted_files = 0
    deleted_folders = 0
    skipped_items = 0

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
                deleted_files += 1
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                deleted_folders += 1
        except Exception as e:
            # Files currently locked or used by active programs will be skipped
            skipped_items += 1

    print(f"Finished cleaning {folder_path}:")
    print(f"  - Deleted files: {deleted_files}")
    print(f"  - Deleted folders: {deleted_folders}")
    print(f"  - Skipped (in-use) items: {skipped_items}")

def main():
    # 1. User Temp Directory (e.g., C:\Users\<Name>\AppData\Local\Temp)
    user_temp = tempfile.gettempdir()
    
    # 2. System Temp Directory (C:\Windows\Temp)
    system_temp = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp')

    print("Starting Temporary Files Cleanup...")
    
    clean_directory(user_temp)
    clean_directory(system_temp)

    print("\nCleanup completed successfully!")

if __name__ == "__main__":
    main()