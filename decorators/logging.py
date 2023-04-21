import functools
import os


def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling function {func.__name__} with arguments {args} {kwargs}")
        return func(*args, **kwargs)
    return wrapper


from flask import request
import functools
import json
import time

def log_request_info(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check for "env:dev" header and skip logging if present
        if "testing" in request.headers:
            return func(*args, **kwargs)

        # Log request information
        request_info = {
            "url": request.url,
            "method": request.method,
            "headers": dict(request.headers),
            "data": request.data.decode("utf-8"),
            "form": dict(request.form),
            "args": dict(request.args),
            "cookies": dict(request.cookies)
        }
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        filename = f"request_logs/request-{timestamp.replace(':', '-')}.json"
        with open(filename, "w") as f:
            json.dump(request_info, f, indent=4)

        # Call the function and return the result
        return func(*args, **kwargs)

    return wrapper


import os
import hashlib
import time
import shutil
from flask import request, jsonify


def middleware_log_request_info():

    if "Testing" in request.headers:
        # If present, do not log the request
        return

    # Log request information
    request_info = {
        "url": request.url,
        "method": request.method,
        "headers": dict(request.headers),
        "data": request.data.decode("utf-8"),
        "form": dict(request.form),
        "args": dict(request.args),
        "cookies": dict(request.cookies)
    }

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    folder = os.path.join(os.getcwd(), "request_logs", f"request-{timestamp.replace(':', '-')}")
    if not os.path.exists(folder):
        os.mkdir(folder)

    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return

        # if file was uploaded, save to uploads folder
        print(file, flush=True)
        file_extension = file.filename.rsplit('.', 1)[1]
        hash_object = hashlib.sha256(str(time.time()).encode('utf-8'))
        file_hash = hash_object.hexdigest()
        file_path = os.path.join(folder, f"{file_hash}.{file_extension}")
        file.save(file_path)

        # reset the file pointer
        request.files['file'].seek(0)

        request_info['files'] = f"{file_hash}.{file_extension}"

    # save request info to file
    filename = os.path.join(folder, f"request-{timestamp.replace(':', '-')}.json")
    with open(filename, "w+") as f:
        json.dump(request_info, f, indent=2)







