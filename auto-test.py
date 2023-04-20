import os
import json
from io import BytesIO

import requests

# this file serves as a place to log test suites, and to run them
# test suites:
# SUITE_DIR = "test_suites/upload_10s_audio_sample"
# SUITE_DIR = "test_suites/delete_clips_and_upload_60s_wav"

# how to make a new test suite
# clear request_logs directory so only "empty.txt" is remaining
# browse through app normally, all requests are being captured by default
# run python generate-test-suite.py
# to test the test suite run python auto-test.py after updating auto-test.py to use the correct directory
# refactor the name of the generated suite and move into test_suites for long term storage

# Define the directory containing the generated test suite
SUITE_DIR = "test_suites/delete_clips_and_upload_60s_wav"


# Get a list of all the JSON files in the directory
log_files = sorted(
    [f for f in os.listdir(SUITE_DIR) if f.endswith(".json")],
    key=lambda f: f.split("-")[1].replace(".json", "")
)

# Loop through the log files and replicate each request
for filename in log_files:
    with open(os.path.join(SUITE_DIR, filename), "r") as f:
        request_info = json.load(f)
        modified_headers = {**request_info["headers"], "testing": "true"}
        print('sending request', request_info, flush=True)

        # Get the filename of the associated audio file
        if 'files' in request_info:
            print("adding file", request_info['files'])
            audio_filename = request_info['files']
            audio_path = os.path.join(SUITE_DIR, audio_filename)
            audio_data = open(audio_path, "rb")
            print('added audio files', audio_filename, flush=True)
        else:
            audio_data = None

        files = {"file": audio_data} if audio_data else None
        print('files', files)

        # Send the request
        if request_info["method"] == 'GET':
            response = requests.get(
                url=request_info["url"],
                headers=modified_headers,
                data=request_info["data"],
                params=request_info["args"],
                cookies=request_info["cookies"],
            )
        elif 'files' in request_info:
            print("POST file upload")
            response = requests.post(
                url=request_info["url"],
                files=files,
                headers={'Testing': 'True'},
                data=request_info["data"],
                params=request_info["args"],
                cookies=request_info["cookies"],
            )
        else:
            response = requests.post(
                url=request_info["url"],
                headers=modified_headers,
                data=request_info["data"],
                params=request_info["args"],
                cookies=request_info["cookies"],
            )

        print(response.status_code, filename, response.text)

