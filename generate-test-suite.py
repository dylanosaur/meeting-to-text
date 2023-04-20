import os
import shutil
import json

# Define the directory containing the request logs
import time

LOG_DIR = "./request_logs"

# Get a list of all the JSON files in the directory
print(os.listdir(LOG_DIR))
log_files = sorted(
    [os.path.join(LOG_DIR, f, f'{f}.json') for f in os.listdir(LOG_DIR) if f != 'empty.txt'],
    key=lambda f: ''.join(f.split("-")[1])
)

# Create a folder to store the generated suite
timehash = str(time.time()).replace(".", "")
suite_folder = f"./generated_test_suites/generated_suite_{timehash}"
os.makedirs(suite_folder)

# Loop through the log files and copy each request
for filename in log_files:
    with open(filename, "r") as f:
        print(filename)
        request_info = json.load(f)
        modified_headers = {**request_info["headers"], "testing": "true"}
        request_path = os.path.dirname(filename)
        wav_files = [f for f in os.listdir(request_path) if not f.endswith(".json")]
        for wav_file in wav_files:
            shutil.copy(os.path.join(request_path, wav_file), os.path.join(suite_folder, wav_file))
        with open(os.path.join(suite_folder, os.path.basename(filename)), "w") as f_out:
            json.dump(request_info, f_out, indent=4)

print(f"Generated suite: {suite_folder}")
