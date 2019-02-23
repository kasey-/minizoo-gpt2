import pickle
import time
import re
import os
import timeit
import schedule

is_uuid_pkl = re.compile("^[a-f0-9]{40}.pkl$")

from keras_gpt_2 import load_trained_model_from_checkpoint, get_bpe_from_files, generate

global model
global bpe

model_folder = './models/117M'
config_path = os.path.join(model_folder, 'hparams.json')
checkpoint_path = os.path.join(model_folder, 'model.ckpt')
encoder_path = os.path.join(model_folder, 'encoder.json')
vocab_path = os.path.join(model_folder, 'vocab.bpe')

print('Load model from checkpoint...')
model = load_trained_model_from_checkpoint(config_path, checkpoint_path)
print('Load BPE from files...')
bpe = get_bpe_from_files(encoder_path, vocab_path)
print('Running...')

def cleanup_old_tasks(ttl=900):
    now = time.time()
    for job_type in ['jobs/pending','jobs/done']:
        jobs = os.listdir(job_type)
        jobs = cleanup_task_list(jobs)
        for job in jobs:
            job_path = job_type+"/"+job
            job_age = os.path.getmtime(job_path)
            if(now - ttl > job_age):
                os.remove(job_path)
                print("Delete too old "+job_path)

def cleanup_task_list(task_list):
    return list(filter(is_uuid_pkl.search, task_list))

def get_next_task(task_list):
    uuid = task_list.pop()
    infile = open('jobs/pending/'+uuid,'rb')
    task = pickle.load(infile)
    infile.close()
    return uuid,task

def process_task(task,uuid):
    print("Processing %s" % (uuid))
    tic=timeit.default_timer()
    output = generate(model, bpe, [task['text']], length=task['length'], top_k=task['top_k'])
    toc=timeit.default_timer()
    print(output)
    print('Processing time %s' % (toc-tic))
    return output[0]

def commit_task(task,result,uuid):
    print("Saving jobs/done/%s" % (uuid))
    outfile = open('jobs/done/'+uuid,'wb')
    payload = {'task':task, 'result':result, 'uuid':uuid}
    pickle.dump(payload,outfile)
    outfile.close()
    print("Deleting jobs/pending/%s" % (uuid))
    os.remove('jobs/pending/'+uuid)

def generate_text_if_req():
    task_list = os.listdir('jobs/pending')
    task_list = cleanup_task_list(task_list)
    if len(task_list) > 0:
        uuid,task = get_next_task(task_list)
        result = process_task(task,uuid)
        commit_task(task,result,uuid)

if __name__ == "__main__":
    schedule.every(5).minutes.do(cleanup_old_tasks)
    schedule.every(1).seconds.do(generate_text_if_req)
    while True:
        time.sleep(1)
        schedule.run_pending()
