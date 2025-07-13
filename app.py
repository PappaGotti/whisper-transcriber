import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import traceback

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Empty filename"}), 400

        # Save temporarily
        temp_path = "/tmp/temp_audio"
        file.save(temp_path)

        # Reopen for OpenAI
        with open(temp_path, "rb") as audio_file:
            transcription = openai.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1"
                # ❌ Don't pass batch_size here!
            )

        return jsonify({"text": transcription.text})

    except Exception as e:
        print("❌ Transcription error:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500
