import psutil

def stop_server():
    for process in psutil.process_iter():
        if 'uvicorn' in process.name():
            print('the server is shutting down')
            process.terminate()

# stop the server
stop_server()