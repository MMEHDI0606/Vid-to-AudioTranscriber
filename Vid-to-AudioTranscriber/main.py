import sys
import os
import tempfile
import torch
import subprocess

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QComboBox,
    QTextEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QScrollArea
)
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


# ---- CONFIGURATION ----
MODEL_ID = "openai/whisper-large-v3-turbo"

# Path to your ffmpeg.exe
FFMPEG_PATH = r"C:\Users\hkals\Downloads\ffmpeg-7.0.2-full_build\bin\ffmpeg.exe"

# Supported languages
SUPPORTED_LANGUAGES = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Dutch": "nl",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh",
    "Auto-detect": None
}


# ---- HELPER FUNCTIONS ----
def is_video_file(file_path):
    """Returns True if file has a video stream."""
    try:
        # Probe with ffmpeg
        command = [
            FFMPEG_PATH,
            "-v", "error",
            "-show_entries", "stream=codec_type",
            "-of", "default=nw=1",
            "-i", file_path
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return "video" in result.stdout
    except Exception:
        return False


def extract_audio_from_video(video_path):
    temp_dir = tempfile.mkdtemp()
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(temp_dir, f"{base_name}_audio.wav")

    command = [
        FFMPEG_PATH,
        "-i", video_path,
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1",
        audio_path
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return audio_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error extracting audio: {e}")


def transcribe_audio_with_whisper(audio_path, language):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        MODEL_ID, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    ).to(device)

    processor = AutoProcessor.from_pretrained(MODEL_ID)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
        chunk_length_s=30,
        generate_kwargs={"output_attentions": True}
    )

    generate_kwargs = {
        "task": "transcribe",
        "return_timestamps": "word"
    }

    if language:
        generate_kwargs["language"] = language

    result = pipe(audio_path, generate_kwargs=generate_kwargs)
    return result["text"], result.get("chunks", [])


# ---- MAIN WINDOW ----
class TranscriptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Video & Audio Transcriber")
        self.setGeometry(100, 100, 700, 600)
        self.setAcceptDrops(True)

        self.file_path = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Drag-and-drop label
        self.drop_label = QLabel("Drag and drop a video or audio file here\n(or click below to select)")
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setStyleSheet("border: 2px dashed gray; padding: 40px;")
        layout.addWidget(self.drop_label)

        # File button
        self.select_button = QPushButton("Select File")
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)

        # Language selection
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Language:")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(SUPPORTED_LANGUAGES.keys())
        self.lang_combo.setCurrentText("English")
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        layout.addLayout(lang_layout)

        # Transcribe button
        self.transcribe_button = QPushButton("Transcribe")
        self.transcribe_button.clicked.connect(self.run_transcription)
        self.transcribe_button.setEnabled(False)
        layout.addWidget(self.transcribe_button)

        # Transcript display
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        scroll = QScrollArea()
        scroll.setWidget(self.output_text)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        mime_data: QMimeData = event.mimeData()
        if mime_data.hasUrls() and len(mime_data.urls()) == 1:
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        url = event.mimeData().urls()[0]
        file_path = url.toLocalFile()
        if os.path.isfile(file_path):
            self.file_path = file_path
            self.drop_label.setText(f"Selected file:\n{os.path.basename(file_path)}")
            self.transcribe_button.setEnabled(True)
        else:
            self.show_error("Invalid file dropped.")

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Video or Audio File",
            "", "All Media (*.mp4 *.mkv *.avi *.mov *.mp3 *.wav *.m4a *.flac *.ogg *.wma *.aac)"
        )
        if file_path:
            self.file_path = file_path
            self.drop_label.setText(f"Selected file:\n{os.path.basename(file_path)}")
            self.transcribe_button.setEnabled(True)

    def show_error(self, message):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Error", message)

    def run_transcription(self):
        lang_key = self.lang_combo.currentText()
        lang_code = SUPPORTED_LANGUAGES[lang_key]

        if not self.file_path:
            self.show_error("No file selected.")
            return

        try:
            if is_video_file(self.file_path):
                self.output_text.setPlainText("Detected video file.\nExtracting audio...\n")
                audio_path = extract_audio_from_video(self.file_path)
            else:
                self.output_text.setPlainText("Detected audio file.\nUsing directly...\n")
                audio_path = self.file_path

            self.output_text.append("\nTranscribing...\n")
            transcript, chunks = transcribe_audio_with_whisper(audio_path, lang_code)

            # Show full transcript
            self.output_text.setPlainText("Full Transcript:\n" + transcript + "\n\n")

            # Show word-by-word breakdown
            self.output_text.append("Word-by-word Timestamps:\n")
            for chunk in chunks:
                start = chunk["timestamp"][0]
                end = chunk["timestamp"][1]
                word = chunk["text"]
                self.output_text.append(f"[{start:.2f} - {end:.2f}] {word}")

        except Exception as e:
            self.show_error(f"Error during transcription:\n{str(e)}")


# ---- RUN APP ----
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranscriptionApp()
    window.show()
    sys.exit(app.exec_())