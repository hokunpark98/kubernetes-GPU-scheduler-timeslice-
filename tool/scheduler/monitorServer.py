import socket
import json
from selectPod import SelectPod
from updateQuota import UpdateQuota
        
class MonitorServer():
    def __init__(self):
        self.UDP_IP = "192.168.0.3"
        self.UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        #self.url = 'http://192.168.0.3:5006/api/runSelector'
    
    
    def splitKeyValue(self, received_dict, addr):
        tmp = dict()
        for key, values in received_dict.items():
            mean_time = round(sum(values) / len(values), 3) * 1000
            length = len(values)
            tmp[key] = {'meanTime': mean_time, 'count': length, 'addr': addr[0]}   
        
        return tmp
    
    '''
    def runSelector(self):
        data_to_send = {'name': name}
        response = requests.post(self.url, json=data_to_send)

        if response.status_code == 200:
            data_received = response.json()
            return data_received.get('greeting')
        else:
            return f"Failed to get response. Status code: {response.status_code}"
    '''
    
    def printPodInfo(self, result):
        for key, nested in result.items():
            print(f'Pod Name: {key}, SPEC: {nested}')
        
        
    def runMonitor(self):
        print('Monitoring start')
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        result = dict()

        while True:
            try:
                data, addr = self.sock.recvfrom(500000)  
                received_dict = json.loads(data.decode("utf-8")) # 클라이언트로부터 데이터를 받음
                
                print("---------------------------------------")
                print("Received message")
                result = self.splitKeyValue(received_dict, addr) # 딕셔너리 형태로 보기 편하게 정리 {'pod명': {'평균소요시간', '실행 횟수', '노드IP'}}
                self.printPodInfo(result)
                
                selectPod = SelectPod(result) # 어떤 파드가 fast, slow인지 확인
                medianCount, medianTime, fastList, slowList = selectPod.select()
                print(f'standard: {medianCount}회, {medianTime}ms')
                print('fastList:', fastList)
                print('slowList:', slowList)
                
                ssh = UpdateQuota() # fast, slow Pod의 cpu Quota 변경
                ssh.updateFastContainer(fastList)
                ssh.updateSlowContainer(slowList)
                print("---------------------------------------")
               
                
            except json.JSONDecodeError:
                print("Failed to decode JSON.")
            except Exception as e:
                print(f"An error occurred: {e}")
        

if __name__ == '__main__':
    monitorServer = MonitorServer()
    monitorServer.runMonitor()