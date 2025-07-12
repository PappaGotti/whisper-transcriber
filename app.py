from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    try:
        transcript = openai.Audio.transcribe("whisper-1", file)
        return jsonify({'text': transcript['text']})
    except openai.error.OpenAIError as e:
        print("OpenAI error:", e)
        return jsonify({'error': f'OpenAI API Error: {str(e)}'}), 500
    except Exception as e:
        print("Unexpected error:", e)
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run()
