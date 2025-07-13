from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Make sure your OpenAI key is set in the Render environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    print(f"📥 Received file: {file.filename}, Content-Type: {file.content_type}")

    try:
        # Save a copy of the file to disk for debug purposes
        print("📦 Saving temp file...")
        temp_path = "/tmp/test.mp3"
        with open(temp_path, "wb") as f:
            f.write(file.read())

        # Reset file stream position for OpenAI API
        file.stream.seek(0)

        # Call Whisper API via OpenAI
        print("🧠 Sending to OpenAI Whisper API...")
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=file.stream
        )

        print("✅ Transcription complete")
        return jsonify({'text': response.text})
    except Exception as e:
        print("❌ Transcription failed:", str(e))
        return jsonify({'error': str(e)}), 500
