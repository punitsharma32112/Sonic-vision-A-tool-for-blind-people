import os
import sys
import subprocess
import time
import re
import threading

from chatbot.voice_chatbot import listen_command
from point_object_module.scripts.audio_feedback import AudioFeedback

# ─── Constants & Paths ─────────────────────────────────────────────────────────
OCR_DIR           = "easyocr_module"
POINT_DIR         = "point_object_module"
OCR_CAPTURE_FILE  = os.path.join(OCR_DIR,   "capture_trigger.txt")
OCR_STOP_FILE     = os.path.join(OCR_DIR,   "stop_ocr.txt")
POINT_STOP_FILE   = os.path.join(".",       "stop_pointer.txt")
PAGE_FOLDER       = "pages"

# ─── Reader Thread State ───────────────────────────────────────────────────────
_current_reader = None
_reader_lock    = threading.Lock()

# ─── Globals ───────────────────────────────────────────────────────────────────
running_processes = {}
audio_feedback    = AudioFeedback()

# ─── TTS Helpers ───────────────────────────────────────────────────────────────
def speak(msg: str):
    audio_feedback.speak(msg)

def tts_stop():
    if hasattr(audio_feedback, "stop"):
        audio_feedback.stop()
    elif hasattr(audio_feedback, "engine") and hasattr(audio_feedback.engine, "stop"):
        audio_feedback.engine.stop()

# ─── Single‑Page Read Worker & Control ─────────────────────────────────────────
def _read_page_worker(n: int):
    path = os.path.join(OCR_DIR, PAGE_FOLDER, f"page{n}.txt")
    if not os.path.exists(path):
        speak(f"Page {n} not found.")
        return
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    if not text:
        speak(f"Page {n} is empty.")
    else:
        speak(text)

def start_read_page(n: int):
    global _current_reader
    with _reader_lock:
        if _current_reader and _current_reader.is_alive():
            tts_stop()
            _current_reader.join()
        _current_reader = threading.Thread(
            target=_read_page_worker,
            args=(n,),
            daemon=True
        )
        _current_reader.start()

# ─── Pages Cleanup ─────────────────────────────────────────────────────────────
def clear_pages():
    folder = os.path.join(OCR_DIR, PAGE_FOLDER)
    if os.path.isdir(folder):
        for fn in os.listdir(folder):
            if fn.startswith("page") and fn.endswith(".txt"):
                try:
                    os.remove(os.path.join(folder, fn))
                except OSError:
                    pass

# ─── Process Launchers ─────────────────────────────────────────────────────────
def run_easyocr():
    return subprocess.Popen([sys.executable, "easyocr_main.py"], cwd=OCR_DIR)

def run_point_detector():
    return subprocess.Popen([sys.executable, "point_detection_main.py"], cwd=POINT_DIR)

# ─── Process Stoppers ──────────────────────────────────────────────────────────
def stop_easyocr(silent=False):
    p = running_processes.get("ocr")
    if not p or p.poll() is not None:
        if not silent:
            speak("Text reader is not running.")
        return
    open(OCR_STOP_FILE, "w").write("stop")
    p.wait()
    del running_processes["ocr"]
    if os.path.exists(OCR_STOP_FILE):
        os.remove(OCR_STOP_FILE)

def stop_point_detector(silent=False):
    p = running_processes.get("point")
    if not p or p.poll() is not None:
        if not silent:
            speak("Object detection is not running.")
        return
    open(POINT_STOP_FILE, "w").write("stop")
    p.wait()
    del running_processes["point"]
    if os.path.exists(POINT_STOP_FILE):
        os.remove(POINT_STOP_FILE)
        
def stop_all(silent=False):
    stop_easyocr(silent=True)
    stop_point_detector(silent=True)
    if not silent:
        speak("All modules stopped.")

# ─── Main Controller Loop ─────────────────────────────────────────────────────
def main():
    speak("Controller active.")

    while True:
        cmd = listen_command()
        if not cmd:
            time.sleep(0.3)
            continue

        cmd = cmd.lower().strip()
        print(f"Command received: '{cmd}'")

        m = re.search(r"read page (\d+)", cmd)
        if m:
            start_read_page(int(m.group(1)))
            continue

        # ─── Start Reader ──────────────────────────────────────
        if any(phrase in cmd for phrase in ("start reader", "read text", "start read", "chart reader")):
            # stop pointer if running
            if "point" in running_processes:
                speak("Stopping pointer before starting reader.")
                stop_point_detector()
            # clear old pages
            clear_pages()
            # launch the OCR module
            speak("Starting reader.")
            running_processes["ocr"] = run_easyocr()
            continue

        # ─── Capture Image ─────────────────────────────────────
        if "capture" in cmd:
            if "ocr" in running_processes:
                speak("Capturing image now.")
                open(OCR_CAPTURE_FILE, "w").write("go")
            else:
                speak("Text reader is not running. Please start reader first.")
            continue

        # ─── Stop Reader ───────────────────────────────────────
        if "stop reader" in cmd or "stop ocr" in cmd:
            stop_easyocr()
            continue

        # ─── Pointer Controls ──────────────────────────────────
        if any(phrase in cmd for phrase in ("start pointer", "start object")):
            if "ocr" in running_processes:
                speak("Stopping reader before starting pointer.")
                stop_easyocr(silent=True)
            if "point" not in running_processes:
                speak("Starting pointer.")
                running_processes["point"] = run_point_detector()
            else:
                speak("Object detection is already running.")
            continue

        if any(phrase in cmd for phrase in ("stop pointer", "stop object")):
            stop_point_detector()
            continue

        # ─── Stop All & Exit ───────────────────────────────────
        if cmd in ("stop all"):
            stop_all()
            continue

        if cmd in ("exit", "quit"):
            stop_all(silent=True)
            speak("Exiting controller.")
            time.sleep(2)
            break

        time.sleep(0.3)

if __name__ == "__main__":
    main()
