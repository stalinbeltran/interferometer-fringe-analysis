import os

def createDirectory(folder):
    os.makedirs(folder, exist_ok=True)
