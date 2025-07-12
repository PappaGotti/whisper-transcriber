from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)  # ✅ This is the line that was missing

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    print(f"📥 Received file: {file.filename}")

    try:
        transcript = openai.Audio.transcribe("whisper-1", file)
        return jsonify({'text': transcript['text']})
    except openai.error.OpenAIError as e:
        print("❌ OpenAI API Error:", str(e))
        return jsonify({'error': f'OpenAI API Error: {str(e)}'}), 500
    except Exception as e:
        print("❌ General Server Error:", str(e))
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/')
def home():
    return 'Whisper backend is running.', 200
