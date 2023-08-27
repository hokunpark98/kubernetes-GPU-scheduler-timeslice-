#!/bin/sh
kubectl create -f /home/dnclab/hokun/IITP/tool/podfolder/4096/cuda1.yaml
kubectl create -f /home/dnclab/hokun/IITP/tool/podfolder/4096/cuda2.yaml
kubectl create -f /home/dnclab/hokun/IITP/tool/podfolder/4096/cuda3.yaml
kubectl create -f /home/dnclab/hokun/IITP/tool/podfolder/4096/cuda4.yaml
kubectl create -f /home/dnclab/hokun/IITP/tool/podfolder/4096/cuda5.yaml
kubectl create -f /home/dnclab/hokun/IITP/tool/yaml/monitorClient.yaml
sleep 15
kubectl get pods -o wide




