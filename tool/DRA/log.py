from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
from calculate import Calculate


class Log:
    def __init__(self):
        config.load_kube_config()
        
        try:
            c = Configuration().get_default_copy()
        except AttributeError:
            c = Configuration()
            c.assert_hostname = False
        
        Configuration.set_default(c)
        self.core_v1 = core_v1_api.CoreV1Api()
        self.ret = self.core_v1.list_namespaced_pod(namespace='default')
    

    def exec_commands(self, api_instance, podNM, exec_command):
        resp = None
        try:
            resp = api_instance.read_namespaced_pod(name=podNM,
                                                    namespace='default')
        except ApiException as e:
            if e.status != 404:
                print("Unknown error: %s" % e)
                exit(1)

        resp = stream(api_instance.connect_get_namespaced_pod_exec,
                    podNM,
                    container='cuda-container',
                    namespace='default',
                    command=exec_command,
                    stderr=True, stdin=False,
                    stdout=True, tty=False)
        return resp



    def splitLog(self, response, podNM):
        result = response.split('\n')
        result = result[1:-1]
        return result



    def getLog(self, api_instance, podNM):
        exec_command1 = [       
            'cat',
            'log.txt'
        ]
        log = self.exec_commands(api_instance, podNM, exec_command1)
        return self.splitLog(log, podNM)


    def initLog(self, api_instance, podNM):
        exec_command = [       
            'sh',
            '-c',
            'cat /dev/null > log.txt'
        ] 
        self.exec_commands(api_instance, podNM, exec_command)


    def getPodHostIP(self, podNM):
        pod = self.core_v1.read_namespaced_pod(name=podNM, namespace="default")
        return pod.status.host_ip


    def podInfo(self, count):
        result = list()
        cal = Calculate()

        #print(ret..nodeName)
        #모니터링
        for i in self.ret.items:         
            podNM = i.metadata.name 
            if count == 0:
                self.initLog(self.core_v1, podNM)
                break
            log = self.getLog(self.core_v1, podNM)
            calAvgTime = cal.avgTime(log)
            hostIP = self.getPodHostIP(podNM)
            result.append([podNM, calAvgTime, len(log), hostIP])        
            self.initLog(self.core_v1, podNM)

        result.sort(key=lambda x:x[2])
        
        return result


                  



