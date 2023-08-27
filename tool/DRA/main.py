from log import Log
from selectPod import SelectPod
from updateQuota import UpdateQuota
import time


if __name__ == '__main__':
    log = Log()
    selectPod = SelectPod()
    ssh = UpdateQuota()
    count = 0

    while True:
        podInfo = log.podInfo(count)
        print('podInfo:', podInfo)
        
        if count != 0:
            upperList, lowerList = selectPod.select(podInfo)

            if upperList:
                print("upperList:", upperList)
                ssh.updateCPU(upperList, -10000)
                
            if lowerList:
                print("lowerList:", lowerList)
                ssh.updateCPU(lowerList, 10000)

        count = 1
        print('----------------------------------------')
        time.sleep(12)    
