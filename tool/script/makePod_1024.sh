#!/bin/sh
kubectl create -f /home/dnclab/hokun/IITP/tool/podfolder/1024/cuda1.yaml
kubectl create -f /home/dnclab/hokun/IITP/tool/podfolder/1024/cuda2.yaml
kubectl create -f /home/dnclab/hokun/IITP/tool/podfolder/1024/cuda3.yaml
kubectl create -f /home/dnclab/hokun/IITP/tool/podfolder/1024/cuda4.yaml
kubectl create -f /home/dnclab/hokun/IITP/tool/podfolder/1024/cuda5.yaml
sleep 15
kubectl get pods -o wide





