from flask import Flask, request, jsonify
import openai
import os

# ✅ Make sure this is declared first
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        print("❌ No file uploaded")
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    print(f"📥 Received file: {file.filename}, Type: {file.content_type}")

    try:
        transcript = openai.Audio.transcribe("whisper-1", file)
        print("✅ Transcription complete")
        return jsonify({'text': transcript['text']})
    except openai.error.OpenAIError as e:
        print("❌ OpenAI Error:", str(e))
        return jsonify({'error': f'OpenAI API Error: {str(e)}'}), 500
    except Exception as e:
        print("❌ General Error:", str(e))
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/')
def home():
    return "Whisper backend running ✅", 200
