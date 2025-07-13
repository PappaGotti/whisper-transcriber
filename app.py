from flask import Flask, request, jsonify
from openai import OpenAI
import os
import traceback

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    print(f"📥 Received file: {file.filename}, Content-Type: {file.content_type}")

    try:
        # Save file temporarily
        temp_path = "/tmp/uploaded_audio"
        file.save(temp_path)
        print("📦 File saved to /tmp")

        # Open the saved file for OpenAI
        with open(temp_path, "rb") as f:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        print("✅ Transcription complete")
        return jsonify({'text': transcription.text})

    except Exception as e:
        print("❌ Transcription error:")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Whisper backend is live ✅", 200
