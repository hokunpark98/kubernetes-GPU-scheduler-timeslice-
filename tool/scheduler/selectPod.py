
class SelectPod:
    def __init__(self, podInfo):
        self.podInfo = podInfo
        
        
    def getMedianCount(self):  
        count_values = [item['count'] for item in self.podInfo.values()]
 
        sorted_counts = sorted(count_values)
        length = len(sorted_counts)
        median_count = -1
        if length % 2 == 1:
            median_count = sorted_counts[length // 2]
        else:
            median_count = (sorted_counts[length // 2 - 1] + sorted_counts[length // 2]) / 2
        
        return median_count



    def getMedianTime(self):    
        time_values = [item['meanTime'] for item in self.podInfo.values()]
 
        sorted_times = sorted(time_values)
        length = len(sorted_times)
        median_time = -1
        if length % 2 == 1:
            median_time = sorted_times[length // 2]
        else:
            median_time = (sorted_times[length // 2 - 1] + sorted_times[length // 2]) / 2
        
        return median_time
    


    def select(self):
        medianCount = self.getMedianCount()
        medianTime = self.getMedianTime()
        fastList = dict()
        slowList = dict()
        
        upperBoundCount = medianCount * 1.1
        upperBoundTime = medianTime * 0.9
        lowerBoundCount = medianCount * 0.9
        lowerBoundTime = medianTime * 1.1 

        for key, nested in self.podInfo.items():
            tmpCount = self.podInfo[key]['count']
            tmpTime = self.podInfo[key]['meanTime']
                
            if tmpCount > upperBoundCount or tmpTime < upperBoundTime:
                tmp = {key: self.podInfo[key]}
                fastList.update(tmp)

            elif tmpCount < lowerBoundCount or tmpTime > lowerBoundTime:
                tmp = {key: self.podInfo[key]}
                slowList.update(tmp)
        
       
        return medianCount, medianTime, fastList, slowList



