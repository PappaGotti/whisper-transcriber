from flask import Flask, request, jsonify
import os
import openai

# NEW OpenAI client format for SDK v1.95.1
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    print(f"📥 Received file: {file.filename}")

    try:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=file
        )
        print("✅ Transcription complete")
        return jsonify({'text': response.text})
    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/')
def health():
    return "Whisper backend running ✅", 200
