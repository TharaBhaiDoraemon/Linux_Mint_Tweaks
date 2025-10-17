#!/usr/bin/env python3
# ─────────────────────────────────────────────
# Instant-launch EasyOCR Text Extractor for Linux (Silent version)
# ─────────────────────────────────────────────

import subprocess
import tempfile
import os
import easyocr
import pyperclip
import cv2
import re

# ── Launch screenshot FIRST ────────────────────────────────
tmpfile = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
print("📸 Select the area to extract text from (you can take your time)...")

# Start selector instantly
screenshot_proc = subprocess.Popen(["gnome-screenshot", "-a", "-f", tmpfile])

# ── Load heavy modules while you select ─────────────────────
print("🧠 Preparing OCR model in background...")
reader = easyocr.Reader(['en'])

# Wait for selection completion
screenshot_proc.wait()

if not (os.path.exists(tmpfile) and os.path.getsize(tmpfile) > 0):
    print("⚠️  Screenshot not captured or file empty.")
    exit(0)

# ── Run OCR ─────────────────────────────────────────────────
print("🔍 Running OCR...")

img = cv2.imread(tmpfile)
if img is None:
    print("❌ Could not read captured image.")
    exit(1)

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
results = reader.readtext(img_rgb)

texts = [t.strip() for _, t, _ in results if t.strip()]
text = " ".join(texts)
text = re.sub(r"\s+", " ", text).replace("- ", "").strip()

# ── Output ─────────────────────────────────────────────────
if text:
    pyperclip.copy(text)
    print("\n✅ Text copied to clipboard!\n")
    print("--- Extracted Text ---\n" + text + "\n")
else:
    print("⚠️ No text detected.")

# Cleanup
os.remove(tmpfile)
print("👋 Done. Exiting Text Extractor.")

