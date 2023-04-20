import os
import json
from io import BytesIO

import requests

# this file serves as a place to log test suites, and to run them
# test suites:
# SUITE_DIR = "test_suites/upload_10s_audio_sample"
# SUITE_DIR = "test_suites/delete_clips_and_upload_60s_wav"
# SUITE_DIR = os.path.join("test_suites", "upload_bad_filetype")

# how to make a new test suite
# clear request_logs directory so only "empty.txt" is remaining
# browse through app normally, all requests are being captured by default
# run python generate-test-suite.py
# to test the test suite run python auto-test.py after updating auto-test.py to use the correct directory
# refactor the name of the generated suite and move into test_suites for long term storage

# Define the directory containing the generated test suite
from test_suites.run import run_test_from_suite_path

if __name__ == '__main__':
    SUITE_DIR = os.path.join("test_suites", "upload_10s_audio_sample")
    run_test_from_suite_path(SUITE_DIR)