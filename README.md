# meeting-to-text
speech to text <br>

to run flask app: 
```
python3 app.py
```

you will need a valid Aws account, and a user with the necessary privileges: aws transcribe full access, aws s3 full access. 
<br>

set these as environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY<br>

you will also need a database setup with the only table in the database.py file <br>

endpoint accepts an audio file, sends it to amazon transcribe (aws speech to text service), and returns response to user

![image](https://user-images.githubusercontent.com/20212151/230215817-6927134a-af3a-4ba5-9aa3-d96d3cea7fea.png)

typical response: <br/>

```
{
  "transcriptions": [
    {
      "index": 0, 
      "text": "Testing testing. This is a, this is a test."
    }
  ]
}
```

## Test Generation 

```
rm -r request_logs/request-*
<- browse around with app running, requests are captured ->
python generate-test-suite.py
```
Test are generated into the generated_test_suites folder. Refactor those folders into the 
test_suites folder if the test is useful.

## Run Single Test Suite

```
python auto-test.py
```

## Run All Tests
```commandline
cd test_suites
python run.py
```

```commandline
$ python run.py
['delete_clips_and_uploads', 'upload_10s_audio_sample', 'upload_bad_filetype', '__pycache__']
============ delete_clips_and_uploads ============
sending request GET http://localhost:5000/delete_all_sound_clips
200
============ upload_10s_audio_sample ============
sending request GET http://localhost:5000/
200
sending request POST http://localhost:5000/transcribe
handled as file upload
200
============ upload_bad_filetype ============
sending request POST http://localhost:5000/transcribe
handled as file upload
400
============ __pycache__ ============

```