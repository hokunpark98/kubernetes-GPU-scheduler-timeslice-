import os        
import socket
import json
import numpy as np
import time


class Monitor:
    def __init__(self):
        self.UDP_IP = "172.27.205.178"
        self.UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.folder_path = '/home/dnclab/hokun/IITP/saveInfo'
        self.result = dict()
   
   
    def makeDict(self, podNM, data):
        data = list(map(float, data.strip().split('\n')))
        data = np.round(data, 3)
        data = data.tolist()
        tmp = {podNM: data}   
        return tmp
   
    
    def getInfo(self):
        count = 0
        print('Monitor Client')
        while(True):
            for folder in os.listdir(self.folder_path):
                file_path = f'{self.folder_path}/{folder}'
                for file_name in os.listdir(file_path):
                    if file_name == 'info.txt':
                        file_path = f'{file_path}/{file_name}'
                        if count == 0:
                            os.remove(file_path)
                        else:
                            with open(file_path, 'r') as file:
                                content = file.read() 
                                tmp = self.makeDict(folder, content) 
                                self.result.update(tmp)
                            os.remove(file_path)
            if count != 0:              
                json_str = json.dumps(self.result)
                self.sock.sendto(json_str.encode("utf-8"), (self.UDP_IP, self.UDP_PORT)) 
                print('send to server')

            time.sleep(15)
            count = 1
                


if __name__ == '__main__':
    monitor = Monitor()
    monitor.getInfo()


