import boto3

# Create a session with a specific region
session = boto3.Session(region_name='us-west-1')


# Create a client object for the IAM service
iam_client = session.client('iam')

# Get the current user's IAM user name
user_name = iam_client.get_user()['User']['UserName']

# Get a list of the policies attached to the current user
attached_policies = iam_client.list_attached_user_policies(UserName=user_name)['AttachedPolicies']

# Print out the names of the attached policies
print(f"The following policies are attached to user {user_name}:")
for policy in attached_policies:
    print(policy['PolicyName'])

# Set the file name and format
file_name = 'english.wav'
file_format = file_name.split('.')[-1]

import hashlib
import time

# Generate a unique hash based on the current time
timestamp = str(time.time()).encode('utf-8')
hash_object = hashlib.sha256(timestamp)
hash_string = hash_object.hexdigest()

# Set the transcription job name
job_name = f'example-job-{hash_string}'


# Set the S3 bucket name and key where the audio file is stored
bucket_name = 'meeting-to-text'
test_file_key = f'audio/{file_name}'

# Set the output S3 bucket name and key where the transcription results will be stored
test_output_bucket_name = 'meeting-to-text'
test_output_key = f'transcriptions/{job_name}.json'

s3 = boto3.client('s3')

# Test S3 read access
def test_s3_read_access():
    key = 'audio/english.wav'
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        print(f"Success! Object {key} exists in S3 bucket {bucket_name}.")
    except Exception as e:
        print(f"Failed to get object {key} from S3 bucket {bucket_name}. Error message: {str(e)}")

# Test S3 write access
def test_s3_write_access():
    key = 'audio/upload_test.wav'
    filename = 'english.wav'
    try:
        with open(filename, 'rb') as f:
            s3.upload_fileobj(f, bucket_name, key)
        print(f"Success! File {filename} uploaded to S3 bucket {bucket_name} with key {key}.")
    except Exception as e:
        print(f"Failed to upload file {filename} to S3 bucket {bucket_name} with key {key}. Error message: {str(e)}")

test_s3_read_access()
test_s3_write_access()