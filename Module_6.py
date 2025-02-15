import os

def update_inserts():
    file_path = os.path.join(os.getcwd(),'dags/run/status.txt')
    file = open(file_path,"r")
    inserts = eval(file.read())
    return inserts
