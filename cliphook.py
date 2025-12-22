#!/usr/bin/env python3
import subprocess
import time
import hashlib
from datetime import datetime

# Log-Datei
LOG_FILE = "/home/dein_user/clipboard.log"

# Intervall in Sekunden
INTERVAL = 2

def get_clipboard():
    """Liest das Wayland-Clipboard via wl-paste"""
    try:
        result = subprocess.run(["wl-paste", "-n"], capture_output=True, text=True)
        return result.stdout.strip()
    except FileNotFoundError:
        print("wl-paste nicht gefunden! Bitte installieren.")
        exit(1)

def hash_content(content):
    """Gibt einen Hash zurück, um Änderungen schnell zu erkennen"""
    return hashlib.sha256(content.encode()).hexdigest()

def log_clipboard(content):
    """Schreibt Inhalt mit Timestamp in die Log-Datei"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}]\n{content}\n\n")

def main():
    last_hash = None
    while True:
        content = get_clipboard()
        current_hash = hash_content(content)
        if current_hash != last_hash:
            if content:  # nur nicht-leere Inhalte loggen
                log_clipboard(content)
                print(f"Neuer Inhalt geloggt: {content[:30]}...")
            last_hash = current_hash
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()

