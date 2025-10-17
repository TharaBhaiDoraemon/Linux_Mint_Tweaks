#!/usr/bin/env python3
"""
Instant-launch PowerToys-style Text Extractor for Linux Mint / GNOME.
Launches gnome-screenshot immediately, loads EasyOCR in background,
copies recognized text to clipboard, and exits cleanly.
"""

import subprocess
import tempfile
import os
import threading
import time

# 📸 Launch screenshot *instantly* before heavy imports
tmpfile = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
print("📸 Select the area to extract text from...")
screenshot_proc = subprocess.Popen(["gnome-screenshot", "-a", "-f", tmpfile])

# ⏳ While screenshot selector is active, import heavy libraries
def load_dependencies():
    global easyocr, cv2, notify2, pyperclip, re
    import easyocr
    import cv2
    import notify2
    import pyperclip
    import re

    globals().update(locals())

# Load heavy modules in background
loader_thread = threading.Thread(target=load_dependencies, daemon=True)
loader_thread.start()

# 🕒 Wait for screenshot to finish (user completes selection)
screenshot_proc.wait()

# Give the background import thread a moment to finish
loader_thread.join()

# ✅ Dependencies ready
reader = easyocr.Reader(['en'])

def extract_text(img_path):
    """Run OCR on the captured image and join lines naturally."""
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Could not open image: {img_path}")

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = reader.readtext(img_rgb)

    texts = [text.strip() for _, text, _ in results if text.strip()]
    if not texts:
        return ""

    joined = " ".join(texts)
    joined = re.sub(r"\s+", " ", joined).replace("- ", "")
    return joined.strip()

def show_notification(title, message):
    notify2.init("Linux Text Extractor")
    n = notify2.Notification(title, message)
    n.set_timeout(3000)
    n.show()

# 🧠 Run OCR now that the screenshot is saved
if os.path.exists(tmpfile) and os.path.getsize(tmpfile) > 0:
    print(f"🔍 Running OCR on: {tmpfile}")
    text = extract_text(tmpfile)

    if text.strip():
        pyperclip.copy(text)
        show_notification("✅ Text Copied!", "Extracted text copied to clipboard.")
        print("\n--- Extracted Text ---\n" + text + "\n")
    else:
        show_notification("⚠️ No text detected", "Try again with clearer text.")
else:
    print("⚠️ No screenshot captured.")

# 🧹 Clean up
try:
    os.remove(tmpfile)
except Exception:
    pass

print("👋 Done.")

