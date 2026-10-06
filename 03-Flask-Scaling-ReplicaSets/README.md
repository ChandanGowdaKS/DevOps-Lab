# Lab 03: Scaling Flask Application Using Kubernetes ReplicaSets

## Objective
Demonstrate horizontal scaling, self-healing, and fault tolerance in Kubernetes using `ReplicaSet` resources for a high-concurrency **Flash Sale** microservice. Configure HTTP **Liveness** and **Readiness** health probes to ensure only healthy containers serve user checkout requests.

---

## Architectural Scenario
During e-commerce flash sales, traffic spikes abruptly. A single pod will become CPU-throttled and drop requests.
We configure a Kubernetes `ReplicaSet` with:
- **Desired Replicas**: 4 pods
- **Readiness Probe**: Queries `/healthz` every 5 seconds. Pods are kept out of the Service endpoints until ready.
- **Liveness Probe**: Detects deadlocks and restarts unresponsive containers automatically.
- **Service**: ClusterIP load-balances checkout requests across all 4 healthy pods.

---

## Instructions

### Step 1: Switch Docker Context to Minikube
```bash
eval $(minikube docker-env)
```

### Step 2: Build the Container Image
```bash
docker build -t flash-service:1.0 .
```

### Step 3: Deploy the ReplicaSet and Service
```bash
kubectl apply -f replicaset.yaml
```

### Step 4: Verify Running Pods and Replicas
```bash
kubectl get replicasets
kubectl get pods -l app=flash-deal -o wide
```
Verify that all 4 pods display `READY 1/1` and `STATUS Running`.

### Step 5: Test Load Balancing Across Pods
Forward port 8080 on the host to the ClusterIP service:
```bash
kubectl port-forward svc/flash-deal-service 8080:80 &
```

Send 5 concurrent requests to the checkout endpoint:
```bash
for i in {1..5}; do
  curl -s http://localhost:8080/checkout | grep -E '"order_id"|"processed_by_pod"'
done
```
Observe that the `processed_by_pod` value alternates across the different pod hostnames, demonstrating traffic distribution.

### Step 6: Test Self-Healing Mechanism
Simulate a catastrophic pod crash by deleting one pod manually:
```bash
POD_TO_KILL=$(kubectl get pods -l app=flash-deal -o jsonpath='{.items[0].metadata.name}')
echo "Terminating: $POD_TO_KILL"
kubectl delete pod $POD_TO_KILL
```
Immediately inspect the pods:
```bash
kubectl get pods -l app=flash-deal
```
Notice how the ReplicaSet controller detects that the current count (3) is less than the desired count (4) and instantaneously creates a new pod to restore the desired state.

---

## Teardown
```bash
kubectl delete -f replicaset.yaml
kill $(pgrep -f "kubectl port-forward svc/flash-deal-service") || true
```
