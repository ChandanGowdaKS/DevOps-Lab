# Lab 10: Multi-Node Kubernetes Deployment with Pod Anti-Affinity & ReplicaSets

## Objective
Configure a multi-node Kubernetes cluster using Minikube, deploy two decoupled backend microservices (**Inventory Service** and **Order Service**), and apply **Pod Anti-Affinity** rules to guarantee that no two instances of the same service run on the same physical/virtual cluster node, maximizing high availability and redundancy.

---

## Architectural Scenario
An online store requires continuous availability for its core purchasing flows:
- **Inventory Service** (2 Replicas): Serves stock availability queries.
- **Order Service** (3 Replicas): Handles customer purchase orders.
- **Resilience Policy**: With `podAntiAffinity` rules keyed on `kubernetes.io/hostname`, Kubernetes automatically schedules pods across separate cluster nodes. If one node encounters hardware degradation or failure, the remaining replicas on other nodes seamlessly serve user traffic.

---

## Instructions

### Step 1: Start 3-Node Minikube Cluster
Clean up previous Minikube configurations and launch a fresh 3-node cluster:
```bash
minikube stop
minikube delete
minikube start --nodes 3 -p devops-cluster
```

Verify all 3 nodes report status `Ready`:
```bash
kubectl get nodes
```
Expected output:
```text
NAME                     STATUS   ROLES           AGE   VERSION
devops-cluster           Ready    control-plane   2m    v1.31.0
devops-cluster-m02       Ready    <none>          1m    v1.31.0
devops-cluster-m03       Ready    <none>          1m    v1.31.0
```

### Step 2: Build Images and Load into Minikube Nodes
Build Docker images locally:
```bash
docker build -t inventory-service:latest -f Dockerfile.inventory .
docker build -t order-service:latest -f Dockerfile.order .
```

Load images into the Minikube cluster nodes:
```bash
minikube -p devops-cluster image load inventory-service:latest
minikube -p devops-cluster image load order-service:latest
```

### Step 3: Deploy Applications and Services
Apply manifests:
```bash
kubectl apply -f inventory-deployment.yaml
kubectl apply -f order-deployment.yaml
kubectl apply -f inventory-service.yaml
kubectl apply -f order-service.yaml
```

### Step 4: Verify Pod Anti-Affinity Scheduling
Inspect the pods with wide output:
```bash
kubectl get pods -o wide
```
Expected Output:
```text
NAME                                        READY   STATUS    RESTARTS   AGE   IP           NODE                 
inventory-service-deploy-5cb68d5b94-2m4qf   1/1     Running   0          35s   10.244.1.2   devops-cluster-m02   
inventory-service-deploy-5cb68d5b94-8n6xp   1/1     Running   0          35s   10.244.2.3   devops-cluster-m03   
order-service-deploy-67df768ccb-4p8rk       1/1     Running   0          30s   10.244.0.5   devops-cluster       
order-service-deploy-67df768ccb-7w2zq       1/1     Running   0          30s   10.244.1.3   devops-cluster-m02   
order-service-deploy-67df768ccb-9b4kt       1/1     Running   0          30s   10.244.2.4   devops-cluster-m03   
```
*Note that each replica of Inventory Service and Order Service is placed on different nodes, satisfying the strict `podAntiAffinity` rules.*

### Step 5: Test Microservice Endpoints
Retrieve NodePort endpoints:
```bash
minikube -p devops-cluster service inventory-svc --url
minikube -p devops-cluster service order-svc --url
```

Test endpoints:
```bash
# Query Inventory
curl http://<inventory-service-url>/inventory

# Check Stock for SKU-001
curl http://<inventory-service-url>/inventory/stock/SKU-001

# Place a new Order
curl -X POST http://<order-service-url>/orders/create \
  -H "Content-Type: application/json" \
  -d '{"sku": "SKU-001", "customer": "Chandan"}'

# View all Orders
curl http://<order-service-url>/orders
```

---

## Teardown
```bash
kubectl delete -f order-service.yaml
kubectl delete -f inventory-service.yaml
kubectl delete -f order-deployment.yaml
kubectl delete -f inventory-deployment.yaml
minikube stop -p devops-cluster
```
