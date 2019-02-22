# minizoo-chatbot
Python [GPT-2](https://blog.openai.com/better-language-models/) as a Service handling request trough a crude file based job system.

Thank you to `CyberZHG` for its [keras-gpt-2](https://github.com/CyberZHG/keras-gpt-2) module :)

# Local build and run

```
pip3 install -r requirements.txt
python3 worker.py
FLASK_APP=server.py flask run
```

# Docker build

```
docker build -t minizoo-gpt2 .
```

Built from conda docker source because handle better tensorflow build...
Use `supervisor` to run both the `server` and the `worker`.