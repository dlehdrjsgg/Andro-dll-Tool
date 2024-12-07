# main.py
from modules.run import multiRun
from modules.handler.load import listApkFiles

def main():
    al = listApkFiles()
    multiRun(al)

if __name__ == "__main__":
    main()
