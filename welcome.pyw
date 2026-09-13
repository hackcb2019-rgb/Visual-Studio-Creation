import os
import psutil
import pyttsx3
import getpass

def get_system_status():
    # Check CPU usage (percentage)
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Check RAM usage (percentage)
    ram = psutil.virtual_memory()
    ram_usage = ram.percent
    
    # Check Battery (if available)
    battery = psutil.sensors_battery()
    battery_status = ""
    if battery is not None:
        battery_status = f" Battery is at {int(battery.percent)} percent."

    # Determine health status based on CPU and RAM loads
    if cpu_usage < 80 and ram_usage < 85:
        health_summary = "Your PC is running smoothly and performance looks good."
    else:
        health_summary = "System load is currently high. You may want to close unused apps."

    status_msg = (
        f"CPU usage is at {int(cpu_usage)} percent. "
        f"RAM usage is at {int(ram_usage)} percent.{battery_status} "
        f"{health_summary}"
    )
    return status_msg

def speak_welcome():
    username = getpass.getuser()
    
    # Initialize Text-To-Speech engine
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speech speed

    # Search installed voices for a female/Indian accent voice
    voices = engine.getProperty('voices')
    selected_voice = None

    # 1. First priority: Search for an Indian female voice (e.g., "Heera" or "India")
    for voice in voices:
        voice_name = voice.name.lower()
        if "female" in voice_name or "zira" in voice_name or "heera" in voice_name or "hazel" in voice_name:
            if "india" in voice_name or "en-in" in voice.id.lower():
                selected_voice = voice.id
                break

    # 2. Second priority: Any available female voice if an Indian accent isn't installed
    if not selected_voice:
        for voice in voices:
            voice_name = voice.name.lower()
            if "female" in voice_name or "zira" in voice_name or "hazel" in voice_name:
                selected_voice = voice.id
                break

    if selected_voice:
        engine.setProperty('voice', selected_voice)

    # Build and deliver greeting
    system_status = get_system_status()
    full_message = f"Welcome back, {username}! {system_status}"
    
    print(full_message)
    engine.say(full_message)
    engine.runAndWait()

if __name__ == "__main__":
    speak_welcome()