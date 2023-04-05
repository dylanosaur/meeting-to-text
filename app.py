import hashlib
import os
import time

from flask import Flask, render_template, request, jsonify
from transcription import transcribe_audio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    file_extension = file.filename.rsplit('.', 1)[1]
    hash_object = hashlib.sha256(str(time.time()).encode('utf-8'))
    file_hash = hash_object.hexdigest()
    file_path = os.path.join('uploads', f"{file_hash}.{file_extension}")
    file.save(file_path)
    transcription = transcribe_audio(file_path)
    return jsonify({'transcription': transcription})

if __name__ == '__main__':
    app.run()
