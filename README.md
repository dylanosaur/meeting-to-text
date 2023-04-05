# meeting-to-text
speech to text <br>

to run flask app: python3 app.py <br>

you will need a valid Aws account, and a user with the necessary privileges: aws transcribe full access, aws s3 full access <br>

endpoint accepts an audio file, sends it to amazon transcribe (aws speech to text service), and returns response to user

![image](https://user-images.githubusercontent.com/20212151/230215817-6927134a-af3a-4ba5-9aa3-d96d3cea7fea.png)

typical response: <br>

```'{"jobName":"example-job-a0d8a04dec7353d28e86d6805295386348b19fccf59109c695e11496a7730503","accountId":"065461454706","results":{"transcripts":[{"transcript":"Testing, testing, testing."}],"items":[{"start_time":"3.21","end_time":"4.059","alternatives":[{"confidence":"0.997","content":"Testing"}],"type":"pronunciation"},{"alternatives":[{"confidence":"0.0","content":","}],"type":"punctuation"},{"start_time":"4.07","end_time":"4.789","alternatives":[{"confidence":"0.998","content":"testing"}],"type":"pronunciation"},{"alternatives":[{"confidence":"0.0","content":","}],"type":"punctuation"},{"start_time":"4.8","end_time":"5.59","alternatives":[{"confidence":"0.998","content":"testing"}],"type":"pronunciation"},{"alternatives":[{"confidence":"0.0","content":"."}],"type":"punctuation"}]},"status":"COMPLETED"}'```
