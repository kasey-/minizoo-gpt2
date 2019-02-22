from flask import Flask
from flask_cors import CORS
from flask import request
from flask import jsonify

from os import path
import pickle
import hashlib

app = Flask(__name__)
CORS(app)

def save_task(text,length=200,top_k=1):
    uuid = "%s%s%s" % (text,length,top_k)
    uuid = hashlib.sha1(uuid.encode('utf-8')).hexdigest()
    task = {'text':text,'length':length,'top_k':top_k}
    outfile = open('jobs/pending/'+uuid+'.pkl','wb')
    pickle.dump(task,outfile)
    outfile.close()
    print("Next task saved in "+uuid)
    return uuid

def get_task_status(uuid):
    return path.isfile('jobs/done/'+uuid+'.pkl')

def get_task_result(uuid):
    infile = open('jobs/done/'+uuid+'.pkl','rb')
    task = pickle.load(infile)
    infile.close()
    return task

@app.route('/gpt-2/generate', methods=["POST"])
def answer():
    data = request.get_json()
    return save_task(data['text'],data['length'],data['top_k'])

@app.route('/gpt-2/generate/<uuid>', methods=["GET"])
def get_answer(uuid):
    if(get_task_status(uuid)):
        return jsonify(status='ok',result=get_task_result(uuid))
    else:
        return jsonify(status='pending')
