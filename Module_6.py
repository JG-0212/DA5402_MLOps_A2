import os

#Function to read the status.txt file if present and update its content
def update_inserts():
    file_path = os.path.join(os.getcwd(),'dags/run/status.txt')
    file = open(file_path,"r")
    inserts = eval(file.read())
    return inserts
