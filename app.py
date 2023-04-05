import hashlib
import os
import time

from flask import Flask, render_template, request, jsonify
from transcription import transcribe_audio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


from pydub import AudioSegment


def chop_audio_file(filepath, output_dir='./output', chunk_length=10000):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the audio file
    audio = AudioSegment.from_file(filepath)

    # Calculate the total length of the audio file in milliseconds
    audio_length = len(audio)

    # Calculate the number of chunks needed to split the audio file into 10 second blocks
    num_chunks = (audio_length // chunk_length) + 1

    # Split the audio file into 10 second blocks and save each chunk to a file
    for i in range(num_chunks):
        start_time = i * chunk_length
        end_time = min((i + 1) * chunk_length, audio_length)
        chunk = audio[start_time:end_time]
        chunk_filename = f'{os.path.splitext(os.path.basename(filepath))[0]}_{i}.wav'
        chunk.export(os.path.join(output_dir, chunk_filename), format='wav')


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

    # Chop the audio file into 10 second blocks
    chop_audio_file(file_path, output_dir=f'./output_{file_hash}')

    # Transcribe each chunk and collect the transcriptions
    transcriptions = []
    for filename in os.listdir(f'./output_{file_hash}'):
        if filename.endswith('.wav'):
            chunk_path = os.path.join(f'./output_{file_hash}', filename)
            transcription = transcribe_audio(chunk_path)
            transcriptions.append(transcription)

    # Concatenate the transcriptions and return as the response
    return jsonify({'transcriptions': transcriptions})

if __name__ == '__main__':
    app.run()
