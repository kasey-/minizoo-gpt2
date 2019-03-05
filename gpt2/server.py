from flask import Flask
from flask import abort
from flask_cors import CORS
from flask import request
from flask import jsonify

from os import path, remove
import json
import hashlib
import re

is_uuid_correct = re.compile("^[a-f0-9]{64}$")

app = Flask(__name__)
CORS(app)

def save_task(text,length=200,top_k=1):
    uuid = "%s%s%s" % (text,length,top_k)
    uuid = hashlib.sha256(uuid.encode('utf-8')).hexdigest()
    task = {'text':text,'length':length,'top_k':top_k}
    with open('jobs/pending/'+uuid+'.json','w') as f:
        json.dump(task,f)
    f.close()
    print("Next task saved in "+uuid)
    return uuid

def get_task_status(uuid):
    if path.isfile('jobs/pending/'+uuid+'.json'):
        return 'pending'
    elif path.isfile('jobs/done/'+uuid+'.json'):
        return 'done'
    else:
        return '404'

def get_task_result(uuid):
    with open('jobs/done/'+uuid+'.json','r') as f:
        task = json.load(f)
    f.close()
    return task

def del_task_result(uuid):
    return remove('jobs/done/'+uuid+'.json')

@app.route('/gpt-2/generate', methods=["POST"])
def answer():
    data = request.get_json()
    return save_task(data['text'],data['length'],data['top_k'])

@app.route('/gpt-2/generate/<uuid>', methods=["GET"])
def get_answer(uuid):
    if not is_uuid_correct.match(uuid):
        abort(400)
    status = get_task_status(uuid)
    if status == 'pending':
        return jsonify(status='pending')
    elif status == 'done':
        payload = get_task_result(uuid)
        del_task_result(uuid)
        return jsonify(
            status='done',
            result=payload['result'],
            task=payload['task'])
    else:
        abort(404)
