kubectl delete pod monitorclient
kubectl get pods -A | grep -i 4096 | awk '{print $2}' | xargs kubectl delete pod
