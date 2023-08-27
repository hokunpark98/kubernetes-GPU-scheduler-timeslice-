import time
from kubernetes import client as kubernetes_client
from kubernetes import utils
from kubernetes import config
import yaml
import os


class makePod:
    def __init__(self):
        self.folder_path = '/home/dnclab/hokun/IITP/cuda/podfolder'
        config.load_kube_config()
        self.k8s_client = kubernetes_client.api_client.ApiClient()


    def make(self):
        file_list = os.listdir(self.folder_path)
        for file in file_list:
            file = self.folder_path + '/' + file
            print(file)
            with open(file) as f:
                yaml_file = yaml.safe_load(f)

            # create pods from yaml object
            utils.create_from_yaml(self.k8s_client, yaml_objects=[
                                yaml_file], namespace="default")


if __name__ == '__main__':
    makepod = makePod()
    makepod.make()
