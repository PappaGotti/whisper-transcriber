@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        print("❌ No file uploaded")
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    print(f"📥 Received file: {file.filename}")
    print(f"📦 Content-Type: {file.content_type}, Size: {request.content_length}")

    try:
        transcript = openai.Audio.transcribe("whisper-1", file)
        print("✅ Transcription successful")
        return jsonify({'text': transcript['text']})
    except openai.error.OpenAIError as e:
        print("❌ OpenAI API Error:", str(e))
        return jsonify({'error': f'OpenAI API Error: {str(e)}'}), 500
    except Exception as e:
        print("❌ General Server Error:", str(e))
        return jsonify({'error': f'Server error: {str(e)}'}), 500
