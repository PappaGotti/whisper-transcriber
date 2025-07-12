@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        print("❌ No file uploaded")
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    print(f"📥 Received file: {file.filename}")

    try:
        # Pass raw file stream directly to Whisper
        transcript = openai.Audio.transcribe("whisper-1", file.stream)
        print("✅ Transcription complete")
        return jsonify({'text': transcript['text']})
    except openai.error.OpenAIError as e:
        print("❌ OpenAI API Error:", str(e))
        return jsonify({'error': f'OpenAI API Error: {str(e)}'}), 500
    except Exception as e:
        print("❌ General Error:", str(e))
        return jsonify({'error': f'Server error: {str(e)}'}), 500
