import os
import sys
import time
import shutil
import ctypes

# Directories to analyze/clean
USER_PROFILE = os.environ.get("USERPROFILE", "C:\\Users\\Default")
CLEANUP_TARGETS = {
    "User Temp": os.environ.get("TEMP"),
    "System Temp": "C:\\Windows\\Temp",
    "Prefetch Cache": "C:\\Windows\\Prefetch",
    "Update Download Cache": "C:\\Windows\\SoftwareDistribution\\Download",
    "Thumbnail Cache": os.path.join(USER_PROFILE, "AppData\\Local\\Microsoft\\Windows\\Explorer")
}

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def draw_progress_bar(percent, width=30):
    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percent * 100:.1f}%"

def get_dir_stats(path):
    """Calculates size and file count without deleting."""
    if not path or not os.path.exists(path):
        return 0, 0
    total_size = 0
    file_count = 0
    for root, _, files in os.walk(path):
        for f in files:
            try:
                fp = os.path.join(root, f)
                total_size += os.path.getsize(fp)
                file_count += 1
            except Exception:
                pass
    return total_size, file_count

def clean_dir(path):
    """Deletes files and counts successfully freed space."""
    if not path or not os.path.exists(path):
        return 0, 0
    freed_bytes = 0
    deleted_files = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                size = os.path.getsize(fp)
                os.remove(fp)
                freed_bytes += size
                deleted_files += 1
            except Exception:
                pass
        for d in dirs:
            try:
                shutil.rmtree(os.path.join(root, d))
            except Exception:
                pass
    return freed_bytes, deleted_files

def main():
    if not is_admin():
        # Relaunch script as administrator
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{os.path.abspath(__file__)}"', None, 1
        )
        return

    os.system("cls" if os.name == "nt" else "clear")
    print("==================================================")
    print("      ⚡ WINDOWS STORAGE OPTIMIZATION DASHBOARD   ")
    print("==================================================\n")

    # Step 1: Scan Phase
    print("🔍 Scanning targeted system locations...\n")
    scan_data = {}
    total_junk_bytes = 0
    total_junk_files = 0

    for name, path in CLEANUP_TARGETS.items():
        if path and os.path.exists(path):
            size, count = get_dir_stats(path)
            scan_data[name] = (path, size, count)
            total_junk_bytes += size
            total_junk_files += count
            size_mb = size / (1024 * 1024)
            print(f"  • {name:<22} : {count:>5} files | ~{size_mb:>7.2f} MB")

    total_mb = total_junk_bytes / (1024 * 1024)
    print("\n--------------------------------------------------")
    print(f"  TOTAL JUNK DETECTED : {total_junk_files} files (~{total_mb:.2f} MB)")
    print("--------------------------------------------------\n")

    if total_junk_files == 0:
        print("✨ Your system is already completely clean!")
        input("\nPress Enter to exit...")
        return

    # User Confirmation
    choice = input("Proceed with cleanup? (Y/N): ").strip().lower()
    if choice != "y":
        print("Operation cancelled.")
        return

    print("\n🚀 Starting cleanup process...\n")
    
    # Step 2: Animated Cleaning Phase
    cleaned_bytes = 0
    cleaned_files = 0
    targets_count = len(scan_data)

    for idx, (name, (path, size, count)) in enumerate(scan_data.items(), 1):
        freed, deleted = clean_dir(path)
        cleaned_bytes += freed
        cleaned_files += deleted

        percent = idx / targets_count
        progress_str = draw_progress_bar(percent)
        print(f"\r{progress_str} | Cleaning: {name:<22}", end="", flush=True)
        time.sleep(0.3)

    # Step 3: Final Report
    freed_mb = cleaned_bytes / (1024 * 1024)
    print("\n\n==================================================")
    print("               CLEANUP COMPLETE                   ")
    print("==================================================")
    print(f"  • Files Removed : {cleaned_files}")
    print(f"  • Disk Space Freed : ~{freed_mb:.2f} MB")
    print("==================================================\n")
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()