import paramiko
import getpass
import json
import time
 

class UpdateQuota:
    def __init__(self):
        self.cli = paramiko.SSHClient()
        self.cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.userNM = "dnclab"
        self.password = "dnclab"   


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


    def updateCPU(self, select, plus):
        for s in select:
            hostIP = s[3]
            podNM = s[0]
            self.cli.connect(hostIP, port=22, username=self.userNM, password=self.password)
            containerID = self.getContianerID(podNM)
            beforeQuota = self.getQuota(containerID)
            self.updateQuota(containerID, beforeQuota, plus)
            time.sleep(0.1)
            afterQuota = self.getQuota(containerID)
            print(f'UPDATE podNM: {podNM}, beforeQuota: {beforeQuota}, afterQuota: {afterQuota}')
        