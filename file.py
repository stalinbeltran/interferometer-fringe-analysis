import os

def createDirectory(folder):
    try:
        os.mkdir(folder)
    except:
        pass
        