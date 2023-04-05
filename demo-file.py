import boto3
import hashlib
import time


def transcribe_audio(file_name):
    # Create a session with a specific region
    session = boto3.Session(region_name='us-west-1')

    # Create a Transcribe client using the session
    transcribe = session.client('transcribe')

    # Set the file name and format
    file_format = file_name.split('.')[-1]

    # Generate a unique hash based on the current time
    timestamp = str(time.time()).encode('utf-8')
    hash_object = hashlib.sha256(timestamp)
    hash_string = hash_object.hexdigest()

    # Set the transcription job name
    job_name = f'example-job-{hash_string}'

    # Set the language code (e.g. 'en-US' for US English)
    language_code = 'en-US'

    # Set the S3 bucket name and key where the audio file is stored
    bucket_name = 'meeting-to-text'

    s3 = boto3.client('s3')

    key = f'audio/upload_{hash_string}.wav'

    # Upload the audio file to S3
    with open(file_name, 'rb') as f:
        s3.upload_fileobj(f, bucket_name, key)

    # Start the transcription job
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': f's3://{bucket_name}/{key}'},
        MediaFormat=file_format,
        LanguageCode=language_code,
        OutputBucketName=bucket_name,
        OutputKey=key
    )

    # Wait for the transcription job to complete
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)['TranscriptionJob'][
            'TranscriptionJobStatus']
        if status in ['COMPLETED', 'FAILED']:
            break
        print(f'Transcription job status: {status}')
        time.sleep(5)

    # Get the transcription results
    if status == 'COMPLETED':
        response = boto3.client('s3').get_object(Bucket=bucket_name, Key=key)
        transcription = response['Body'].read().decode('utf-8')
        return transcription
    else:
        print(f'Transcription job failed with status: {status}')
        return None

transcription = transcribe_audio('english.wav')
print(transcription)
