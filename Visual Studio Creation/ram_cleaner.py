import ctypes
import os
import sys
import gc
import psutil

def force_garbage_collection():
    """Forces Python's internal memory cleanup."""
    collected = gc.collect()
    print(f"[+] Python Garbage Collector freed {collected} objects.")

def trim_working_sets():
    """Requests Windows to trim idle memory from active processes."""
    if os.name != 'nt':
        print("[-] Working set trimming is only supported on Windows.")
        return

    # Windows API Constants
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010
    PROCESS_SET_QUOTA = 0x0100

    psapi = ctypes.windll.psapi
    kernel32 = ctypes.windll.kernel32

    trimmed_processes = 0
    failed_processes = 0

    print("\n[+] Trimming process working sets...")

    # Iterate through all running processes for the current user
    for proc in psutil.process_iter(['pid', 'name']):
        pid = proc.info['pid']
        
        # Skip System and Idle processes
        if pid <= 4:
            continue

        try:
            # Open process handle with permissions to modify working set
            handle = kernel32.OpenProcess(
                PROCESS_QUERY_INFORMATION | PROCESS_VM_READ | PROCESS_SET_QUOTA, 
                False, 
                pid
            )
            
            if handle:
                # Call EmptyWorkingSet to flush idle memory
                success = psapi.EmptyWorkingSet(handle)
                kernel32.CloseHandle(handle)
                
                if success:
                    trimmed_processes += 1
                else:
                    failed_processes += 1
            else:
                failed_processes += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            failed_processes += 1

    print(f"[+] Successfully trimmed working sets for {trimmed_processes} processes.")
    print(f"[-] Skipped/Protected processes: {failed_processes}")

def display_ram_usage():
    """Displays current system memory statistics."""
    mem = psutil.virtual_memory()
    total_gb = mem.total / (1024 ** 3)
    used_gb = mem.used / (1024 ** 3)
    available_gb = mem.available / (1024 ** 3)
    
    print(f"\n--- System Memory Status ---")
    print(f"Total RAM:     {total_gb:.2f} GB")
    print(f"Used RAM:      {used_gb:.2f} GB ({mem.percent}%)")
    print(f"Available RAM: {available_gb:.2f} GB")

def main():
    print("====================================")
    print("      Windows RAM Cleaner Tool      ")
    print("====================================")

    display_ram_usage()

    print("\nStarting memory optimization...")
    force_garbage_collection()
    trim_working_sets()

    print("\nOptimization Complete!")
    display_ram_usage()

if __name__ == "__main__":
    main()