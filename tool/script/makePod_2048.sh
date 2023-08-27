#!/bin/sh
kubectl create -f /home/dnclab/hokun/IITP/tool/podfolder/2048/cuda1.yaml
kubectl create -f /home/dnclab/hokun/IITP/tool/podfolder/2048/cuda2.yaml
kubectl create -f /home/dnclab/hokun/IITP/tool/podfolder/2048/cuda3.yaml
kubectl create -f /home/dnclab/hokun/IITP/tool/podfolder/2048/cuda4.yaml
kubectl create -f /home/dnclab/hokun/IITP/tool/podfolder/2048/cuda5.yaml
sleep 13
kubectl get pods -o wide




