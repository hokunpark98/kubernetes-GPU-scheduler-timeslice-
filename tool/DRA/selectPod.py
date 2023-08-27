
class SelectPod:
    def getMedianCount(self):    
        l = len(self.podInfo)
        m = int(l/2)
        return self.podInfo[m][2]


    def getMedianTime(self):    
        self.podInfo.sort(key=lambda x:x[1])
        l = len(self.podInfo)
        m = int(l/2)
        return self.podInfo[m][1]
    

    def select(self, podInfo):
        self.podInfo = podInfo
        #cpu 증가시킬 pod 선택
        medianCount = self.getMedianCount()
        medianTime = self.getMedianTime()
        
        print(f'standard: {medianCount}회, {medianTime}ms')

        upperBoundCount = medianCount * 1.1
        upperBoundTime = medianTime * 0.9
        lowerBoundCount = medianCount * 0.9
        lowerBoundTime = medianTime * 1.1 

        upperList = list()
        lowerList = list()

        for r in self.podInfo:
            if r[2] > upperBoundCount or r[1] < upperBoundTime:
                upperList.append(r)

            elif r[2] < lowerBoundCount or r[1] > lowerBoundTime:
                lowerList.append(r)
            
       
        return upperList, lowerList


                  



