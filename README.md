# Sonic Vision – A Tool for Blind People

A voice-assisted tool that uses computer vision to help visually impaired individuals interact with their surroundings through sound-based feedback.

## 📁 Project Structure

```
Sonic-Vision-master/
├── chatbot/                # Voice chatbot scripts
├── easyocr_module/        # OCR functionality using EasyOCR
├── point_object_module/   # Object pointing & detection using YOLO & MediaPipe
├── controller.py          # Main control script
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

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

## 📝 Notes

- Python 3.7 or above is required.
- Ensure internet access for downloading models (if required by OCR or YOLO).
