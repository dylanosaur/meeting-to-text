# this will run all the test suites and print out the results
import json
import os

import requests


def run_test_from_suite_path(SUITE_DIR):

    # Get a list of all the JSON files in the directory
    log_files = sorted(
        [f for f in os.listdir(SUITE_DIR) if f.endswith(".json")],
        key=lambda f: '-'.join(f.split("-")[1:]).replace(".json", "")
    )

    # Loop through the log files and replicate each request
    for filename in log_files:
        with open(os.path.join(SUITE_DIR, filename), "r") as f:
            request_info = json.load(f)
            modified_headers = {**request_info["headers"], "testing": "true"}
            print('sending request', request_info["method"], request_info["url"], flush=True)

            # Get the filename of the associated audio file
            if 'files' in request_info:
                # print("adding file", request_info['files'])
                audio_filename = request_info['files']
                audio_path = os.path.join(SUITE_DIR, audio_filename)
                audio_data = open(audio_path, "rb")
                # print('added audio files', audio_filename, flush=True)
            else:
                audio_data = None

            files = {"file": audio_data} if audio_data else None

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
                print("handled as file upload")
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

            print(response.status_code, )


if __name__ == '__main__':
    dir_path = os.getcwd()
    all_tests = [f.name for f in os.scandir(dir_path) if f.is_dir()]
    print(all_tests)
    for test_suite in all_tests:
        print(test_suite, '============')
        run_test_from_suite_path(test_suite)
