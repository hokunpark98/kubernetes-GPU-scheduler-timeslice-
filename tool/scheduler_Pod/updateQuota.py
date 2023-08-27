import paramiko
import json
import time
 

class UpdateQuota:
    def __init__(self):
        self.cli = paramiko.SSHClient()
        self.cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.userNM = "dnclab"
        self.password = "dnclab"   
        self.plus = 10000
        self.minus = -10000


    def getContianerID(self, podNM):
        stdin, stdout, stderr = self.cli.exec_command(f'echo {self.password} | sudo -S crictl ps | grep {podNM}')
        stdin.flush()
        line = stdout.readlines()
        lines = line[0].split(' ')
        containerID = lines[0]
        return containerID


    def getQuota(self, containerID):
        stdin, stdout, stderr = self.cli.exec_command(f'echo {self.password} | sudo -S crictl inspect {containerID}')
        stdin.flush()
        line = stdout.read()
        data = json.loads(line)
        quota = data["info"]["runtimeSpec"]["linux"]["resources"]["cpu"]["quota"]
        return quota
    

    def updateQuota(self, containerID, quota, plus):
        quota = quota + plus
        stdin, stdout, stderr = self.cli.exec_command(f'echo {self.password} | sudo -S crictl update --cpu-quota {quota}  {containerID}')
        stdin.flush()


    def updateFastContainer(self, fastList, file):
        file.write('updateFastList:\n')
        for key, _ in fastList.items():
            hostIP = fastList[key]['addr']
            podNM = key
            self.cli.connect(hostIP, port=22, username=self.userNM, password=self.password)
            containerID = self.getContianerID(podNM)
            beforeQuota = self.getQuota(containerID)
            self.updateQuota(containerID, beforeQuota, self.minus)
            time.sleep(0.1)
            afterQuota = self.getQuota(containerID)
            file.write(f'\tUPDATE podNM: {podNM}, beforeQuota: {beforeQuota}, afterQuota: {afterQuota}\n')

            

    def updateSlowContainer(self, slowList, file):
        file.write('updateSlowList:\n')
        for key, _ in slowList.items():
            hostIP = slowList[key]['addr']
            podNM = key
            self.cli.connect(hostIP, port=22, username=self.userNM, password=self.password)
            containerID = self.getContianerID(podNM)
            beforeQuota = self.getQuota(containerID)
            self.updateQuota(containerID, beforeQuota, self.plus)
            time.sleep(0.1)
            afterQuota = self.getQuota(containerID)
            file.write(f'\tUPDATE podNM: {podNM}, beforeQuota: {beforeQuota}, afterQuota: {afterQuota}\n')
        