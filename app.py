import hashlib
import json
import os
import time
from typing import List

from flask import Flask, render_template, request, jsonify

from database import db, SoundClip
from transcription import transcribe_audio

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("AI_DETECTOR_RDS_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


from pydub import AudioSegment
import wave

def calculate_audio_hash(filepath):
    with wave.open(filepath, 'rb') as wav:
        frames = wav.readframes(wav.getnframes())
        hash_object = hashlib.md5(frames)
        return hash_object.hexdigest()

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

        data_hash = calculate_audio_hash(os.path.join(output_dir, chunk_filename))

        hash_exists = SoundClip.query.filter(SoundClip.hash==data_hash).first()
        if hash_exists:
            print('hash collision, skipping', data_hash)
            continue
        print('adding new sound clip', data_hash)
        # Create a new SoundClip object for the chunk and add it to the database
        sound_clip = SoundClip(
            hash=data_hash,
            file_size_mb=os.path.getsize(os.path.join(output_dir, chunk_filename)) / (1024 * 1024),
            file_name=chunk_filename,
            chunk=True,
            chunk_index=i
        )
        db.session.add(sound_clip)
        db.session.commit()



def longest_string_from_aws_transcribe_response(res):
    # res is a [] of {}'s
    data = res['results']['transcripts']
    data.sort(key=lambda x: len(x['transcript']) )
    return data[0]['transcript']

def process_chunks(file_hash):
    reduced_transcriptions = []
    output_dir = f'./output_{file_hash}'
    for filename in os.listdir(f'./output_{file_hash}'):
        if filename.endswith('.wav'):
            chunk_path = os.path.join(f'./output_{file_hash}', filename)

            # Get the SoundClip object with the same hash as the current chunk
            data_hash = calculate_audio_hash(os.path.join(output_dir, filename))

            sound_clip = SoundClip.query.filter_by(hash=data_hash).first()

            if sound_clip.transcriptions is None:
                # If the transcriptions column is None, transcribe the chunk and store the transcription in the database
                transcription_response = transcribe_audio(chunk_path)
                sound_clip.transcriptions = json.dumps(transcription_response)
                db.session.commit()
                transcription = sound_clip.transcriptions
            else:
                # If the transcriptions column is not None, use the existing transcriptions
                transcription = json.loads(sound_clip.transcriptions)
            loaded_transcription = json.loads(transcription)
            reduced_transcriptions.append({
                'index': sound_clip.chunk_index,
                'text': longest_string_from_aws_transcribe_response(loaded_transcription)
            })
    reduced_transcriptions.sort(key=lambda x: x['index'])
    return reduced_transcriptions


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
    transcriptions = process_chunks(file_hash)

    # Concatenate the transcriptions and return as the response
    return jsonify({'transcriptions': transcriptions})

if __name__ == '__main__':
    app.run()
