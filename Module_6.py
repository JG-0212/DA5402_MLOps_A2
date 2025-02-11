import os

def provide_path():
    parent = os.abspath(os.path.join(os.getcwd(),os.pardir))
    file_path = os.path.join(parent,r"run/status.txt")
    return file_path

def update_inserts():
    file_path = provide_path()
    file = open(file_path,"r")
    inserts = eval(file.read())
    return inserts