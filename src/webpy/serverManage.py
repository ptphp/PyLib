from subprocess import Popen
import os,sys

PYTHON_EXE = "C:\Python27\Pythonw.exe"
WEB_SERVER = None
PORT = "8089"
HOME_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

def run_server():
    global WEB_SERVER
    WEB_SERVER = Popen(args=[PYTHON_EXE,['"'+HOME_DIR+'\code.py"'],PORT],cwd='/')
    
def stop_server():
    global WEB_SERVER
    if WEB_SERVER:
        WEB_SERVER.kill()
        WEB_SERVER.wait()
    WEB_SERVER=None
    
def restart_server():
    stop_server()
    run_server
if __name__ == "__main__":
    run_server()
    stop_server()