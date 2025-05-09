# Sonic Vision – A Tool for Blind People

A voice-assisted tool that uses computer vision to help visually impaired individuals interact with their surroundings through sound-based feedback.

## 📁 Project Structure
![image](https://github.com/user-attachments/assets/9111cac9-d771-426e-a752-b54ac359a1bb)

```
Sonic-Vision-master/
├── chatbot/                # Voice chatbot scripts
├── easyocr_module/        # OCR functionality using EasyOCR
├── point_object_module/   # Object pointing & detection using YOLO & MediaPipe
├── controller.py          # Main control script
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```
👓 How It Helps Blind Users
Blind users often lack real-time, contextual feedback about their surroundings. This project solves that by integrating multiple technologies:

1. 🎙️ Voice Interaction + LLM (Gemini API)
We’ve integrated Google’s Gemini LLM API to allow blind users to ask natural language questions about the world around them and receive spoken answers.

💡 Use Cases:
“What is written on the signboard?”

“Tell me more about the object I’m pointing at.”

“Read this document for me.”

“What's the weather like now?”

The Gemini model processes the query, fetches real-time or contextual information, and the system reads it back aloud, enabling natural and dynamic interaction.

2. 📸 Real-Time Vision System
Uses YOLO + MediaPipe to detect and track objects the user is pointing at.

EasyOCR helps extract text from surroundings (like street signs, books, menus).

These visual insights are instantly converted into spoken feedback.

3. 🖐️ Haptic Feedback for Spatial Awareness
When an object is detected nearby, the system triggers a vibration motor (or buzzer) through GPIO (Raspberry Pi or Arduino) or a USB interface.

Intensity or frequency of vibration varies based on:

Distance from object

Urgency (e.g., fast-moving object)

This helps the user "feel" their environment, even without hearing the voice output — particularly useful in noisy environments.

🔁 Workflow Summary
User points toward an object.

Camera captures the scene → YOLO detects object.

If text is present, EasyOCR reads it.

If the user asks a question, it’s sent to Gemini LLM.

Response is spoken back and/or vibration feedback is given.

All happens in real-time with minimal delay.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Sonic-vision-A-tool-for-blind-people.git
cd Sonic-vision-A-tool-for-blind-people
```

### 2. Create and activate a virtual environment

#### For Linux/Mac:

```bash
python -m venv venv
source venv/bin/activate
```

#### For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Run the Project

```bash
python controller.py
```
![Screenshot 2025-05-09 114650](https://github.com/user-attachments/assets/06b211b8-3e8d-4a06-826f-64ee11aeddeb)

## 📝 Notes

- Python 3.7 or above is required.
- Ensure internet access for downloading models (if required by OCR or YOLO).
🎬 Demo Video


📄 Sample Files
📥 User Guide (PDF)

📹 Download Demo Video

Note: If you're viewing this on GitHub, media files must be uploaded via the web interface or Git LFS for large files.

🤖 Features
![image](https://github.com/user-attachments/assets/e529a1a0-f0d1-4e25-b997-fb895d3f7fc6)

OCR for reading printed text

Object pointing and detection
![image](https://github.com/user-attachments/assets/884f168b-7492-4901-90fd-ae944cf3fbdb)


Voice interaction with the user

Python-based modular structure

Real-time assistance via camera

👨‍💻 Author
Punit Sharma
YouTube Channel
Project Demo: https://www.youtube.com/watch?v=kfVsRI44wlw


