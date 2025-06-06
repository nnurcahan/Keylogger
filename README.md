# Keylogger
# 🔍 Keylogger for Red Team Operations

A stealthy, persistent keylogger designed for use during Red Team post-exploitation scenarios. This tool logs keystrokes as full words, captures periodic screenshots, monitors clipboard activity, and detects analysis tools like Wireshark.

---

## ✨ Features

- ⌨️ **Word-based Keystroke Logging** – Captures entire words instead of individual characters for clearer logs.
- 📌 **Active Window Tracking** – Records the name of the application or window receiving input.
- 📸 **Screenshot Capture** – Takes a screenshot every 60 seconds and logs the file path.
- 📋 **Clipboard Monitoring** – Detects and logs changes in clipboard data.
- 🚨 **Wireshark Detection** – Monitors system processes and logs if Wireshark is detected.
- 🔁 **Startup Persistence** – Automatically adds itself to Windows startup via registry.
- 🧩 **Threaded Architecture** – Multithreaded design ensures minimal performance impact.

---

## ⚠️ Usage Disclaimer

> **Disclaimer**
>
> This software is intended for **educational purposes only**. It is developed to support **authorized penetration testing**, **Red Team exercises**, and **cybersecurity research** within environments where **all participants have given explicit permission**.
>
> **Unauthorized use of this tool is strictly prohibited.** Misuse may violate local, national, or international laws. The developer is not responsible for any damage or legal consequences resulting from the misuse of this software.

---

## 🛠 Dependencies

To install the required packages, run:

```bash
pip install -r requirements.txt
