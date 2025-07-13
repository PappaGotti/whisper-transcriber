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
        # Save the file for debug
        with open("/tmp/test.mp3", "wb") as f:
            f.write(file.read())

        file.stream.seek(0)  # reset the stream pointer

        # Transcribe using OpenAI Whisper API (v1.95+ style)
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=file.stream
        )

        print("✅ Transcription complete")
        return jsonify({'text': response.text})
    except Exception as e:
        print("❌ Traceback:")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Whisper backend is live ✅", 200
