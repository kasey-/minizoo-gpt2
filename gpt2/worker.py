from os import listdir, remove as rmfile
import pickle
import time

def get_next_task():
#    print("get next task")
    task_list = listdir('jobs/pending')
    uuid = task_list.pop()
    infile = open('jobs/pending/'+uuid,'rb')
    task = pickle.load(infile)
    infile.close()
    return uuid,task

def process_task(task):
#    time.sleep(5)
    return "Processed : <%s> <%s> <%s>" % (task['text'],task['length'],task['top_k'])

def commit_task(result,uuid):
    print("Save %s in jobs/done/%s" % (result,uuid))
    outfile = open('jobs/done/'+uuid,'wb')
    pickle.dump(result,outfile)
    outfile.close()
    print("Delete jobs/pending/%s" % (uuid))
    rmfile('jobs/pending/'+uuid)

while True:
    time.sleep(1)
    try:
        uuid,task = get_next_task()
    except IndexError:
        pass
#        print("No task to handle")
    else:
        result = process_task(task)
        commit_task(result,uuid)
    


