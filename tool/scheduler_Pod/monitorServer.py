import socket
import json
import os
from selectPod import SelectPod
from updateQuota import UpdateQuota
from datetime import datetime
from pytz import timezone

class MonitorServer():
    def __init__(self):
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        self.UDP_IP = ip_address
        self.UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.log = ''
        

    def countFile(self):
        folder_path = '/home/tmp/'
        all_files = os.listdir(folder_path)
        file_count = sum(1 for entry in all_files if os.path.isfile(os.path.join(folder_path, entry)))
        return file_count

    
    
    def splitKeyValue(self, received_dict, addr):
        tmp = dict()
        for key, values in received_dict.items():
            mean_time = round(sum(values) / len(values), 3) * 1000
            length = len(values)
            tmp[key] = {'meanTime': mean_time, 'count': length, 'addr': '192.168.0.4'}
              
        return tmp
    
    
    def printPodInfo(self, result, file):
        for key, nested in result.items():
            file.write(f'Pod Name: {key}, SPEC: {nested}\n')
        
        
    def runMonitor(self):
        #num_file = self.countFile() + 1
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        result = dict()

        while True:
            try:
                data, addr = self.sock.recvfrom(500000)  
                received_dict = json.loads(data.decode("utf-8")) # 클라이언트로부터 데이터를 받음
                
                file = open(f'/home/tmp/log.txt', 'a') # 정보 저장할 파일 열기
                file.write("---------------------------------------\n")
                file.write("Received message\n")
                now = datetime.now(timezone('Asia/Seoul')) # 현재 시간 구함
                file.write(f"Received Time: {now}\n")

                result = self.splitKeyValue(received_dict, addr) # 딕셔너리 형태로 보기 편하게 정리 {'pod명': {'평균소요시간', '실행 횟수', '노드IP'}}
                self.printPodInfo(result, file)
                selectPod = SelectPod(result) # 어떤 파드가 fast, slow인지 확인
                medianCount, medianTime, fastList, slowList = selectPod.select()
                file.write(f'standard: {medianCount}회, {medianTime}ms\n')
                file.write(f'fastList: {fastList}\n')
                file.write(f'slowList: {slowList}\n')
                
                ssh = UpdateQuota() # fast, slow Pod의 cpu Quota 변경
                ssh.updateFastContainer(fastList, file)
                ssh.updateSlowContainer(slowList, file)
                file.write("---------------------------------------\n\n")
                file.close()
                
            except json.JSONDecodeError:
                file.write("Failed to decode JSON.")
            except Exception as e:
                file.write(f"An error occurred: {e}")
                
            
        

if __name__ == '__main__':
    monitorServer = MonitorServer()
    monitorServer.runMonitor()