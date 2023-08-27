from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
from kubernetes import client, config
from kubernetes.stream import stream
from datetime import datetime

import time


class Calculate:

    def avgTime(self, log):
        log = list(map(float, log))
        mean = sum(log) / len(log)
        mean = round(mean, 3)
        mean = mean * 1000
        return int(mean)

    

        
        



