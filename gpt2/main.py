from flask import Flask
from flask_cors import CORS
from flask import request

import os
from keras_gpt_2 import load_trained_model_from_checkpoint, get_bpe_from_files, generate

global model
global bpe

app = Flask(__name__)
CORS(app)

model_folder = './models/117M'
config_path = os.path.join(model_folder, 'hparams.json')
checkpoint_path = os.path.join(model_folder, 'model.ckpt')
encoder_path = os.path.join(model_folder, 'encoder.json')
vocab_path = os.path.join(model_folder, 'vocab.bpe')

print('Load model from checkpoint...')
model = load_trained_model_from_checkpoint(config_path, checkpoint_path)
print('Load BPE from files...')
bpe = get_bpe_from_files(encoder_path, vocab_path)
print('Generate text...')
output = generate(model, bpe, ['From the day forth, my arm'], length=20, top_k=1)
print(output[0])

@app.route('/gpt--2/generate', methods=["POST"])
def answer():
    data = request.get_json()
    output = generate(model, bpe, [data['text']], length=data['size'], top_k=data['top_k'])
    return output[0]
