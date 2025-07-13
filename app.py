from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    print(f"📥 Received file: {file.filename}, size: {file.content_length}")

    try:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=file.stream  # ✅ REQUIRED for SDK v1.x
        )
        print("✅ Transcription complete")
        return jsonify({'text': response.text})
    except Exception as e:
        print("❌ Error during transcription:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Whisper backend running ✅", 200
