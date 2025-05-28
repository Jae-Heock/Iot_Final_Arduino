# IotServer.py 

from http.server import HTTPServer
from IotReqHnl import IotReqHnl
from PythonHub import PythonHub

class IotServer:
    __defHost = 'localhost'
    __defPort = 8080
    
    def __init__(self, host = __defHost, port = __defPort):
        self.host = host
        self.port = port
        self.webServer = HTTPServer((host, port), IotReqHnl)
        self.webServer.gateway = PythonHub()

    def start(self):
        print(f'My server started at http://{self.host}:{self.port}')
        self.webServer.serve_forever()