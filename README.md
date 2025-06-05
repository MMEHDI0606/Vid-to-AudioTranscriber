# 🎥 Local Video & Audio Transcriber App

A **local, offline video and audio transcription app** built with Python.  
Supports drag-and-drop files, language selection, and word-level timestamps using **Whisper Large V3 Turbo**.

---

## 📌 Features

- ✅ Drag-and-drop support for video/audio files
- ✅ Supports common formats: `.mp4`, `.mkv`, `.avi`, `.mov`, `.mp3`, `.wav`, etc.
- ✅ Local Whisper transcription (no internet required)
- ✅ Word-level timestamps (e.g., `[0.5 - 1.2] Hello`)
- ✅ Language selection (English, French, Spanish, etc.)
- ✅ Works fully offline
- ✅ Hardcoded path to `ffmpeg.exe` (ideal for portable use)

---

## 🧰 Requirements

### System Requirements

- Windows, macOS, or Linux
- Python 3.8+
- At least 6GB RAM recommended for Whisper Large models

### Software Dependencies

Install via pip:

```bash
pip install PyQt5 transformers ffmpeg-python torch accelerate
```

You also need:
- `ffmpeg` installed and working
- Or use the **hardcoded path version**, as shown in this project

---

## ⚙️ Installation Instructions

### Step 1: Clone or Download This Project

```bash
git clone https://github.com/yourusername/local-transcriber-app.git
cd local-transcriber-app
```

Or just download and save the script file (`transcriber_gui.py`).

---

### Step 2: Install Required Packages

```bash
pip install PyQt5 transformers ffmpeg-python torch accelerate
```

---

### Step 3: Install FFmpeg

#### Windows Users:

Download from:  
👉 [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)

Place `ffmpeg.exe` at:
```
C:\Users\hkals\Downloads\ffmpeg-7.0.2-full_build\bin\ffmpeg.exe
```

> 🔁 If you're using a different path, update the `FFMPEG_PATH` variable in the script accordingly.

---

## 🚀 How to Run

### Run the App:

```bash
python transcriber_gui.py
```

### Use the App:

1. **Drag and drop** a video or audio file onto the window  
   OR  
   Click "Select File" to browse your system

2. Choose the **language** of the audio/video

3. Click **"Transcribe"**

4. View the **full transcript** and **word-by-word timestamps**

---

## 📦 Optional: Bundle as Standalone `.exe`

Use PyInstaller to create a standalone executable:

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Build the App

```bash
pyinstaller --onefile --windowed --add-data "C:\\path\\to\\PyQt5\\Qt5\\bin\\platforms;platforms" transcriber_gui.py
```

> Replace the path above with your actual Qt platform plugins folder.

### Step 3: Distribute

Your `.exe` will be in the `dist/` folder.  
Include `ffmpeg.exe` alongside it for full portability.

---

## 📂 Folder Structure (Suggested)

```
/local-transcriber-app/
│
├── transcriber_gui.py       # Main GUI application
├── ffmpeg.exe               # (Optional) Portable ffmpeg binary
└── README.md                # This file
```

---

## 🛠 Troubleshooting

### ❗ "ffmpeg was not found but is required"

Make sure:
- `ffmpeg` is installed and accessible
- The hardcoded path in the script matches where `ffmpeg.exe` is located

---

## 🤝 Contributions

Contributions are welcome! Feel free to open issues or PRs for:

- UI improvements
- Export features (`.txt`, `.srt`, `.json`)
- Batch processing
- Dark mode theme
- Performance optimizations

---

## 📄 License

MIT License – see `LICENSE` file for details.

---

## 📞 Contact

For questions or feature requests, feel free to reach out or open an issue on GitHub.

---

✅ You now have a powerful, private, and portable transcription tool — no internet needed!

Let me know if you'd like:
- A pre-built `.exe` package
- An installer (Inno Setup / NSIS)
- Export options (SRT, TXT, JSON)
- Multi-threading or GPU acceleration enhancements

I'm happy to help!
