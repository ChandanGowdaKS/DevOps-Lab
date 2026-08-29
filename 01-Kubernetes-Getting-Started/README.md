# Lab 01: Kubernetes Getting Started – Deploying Nginx Web Pod

## Objective
The objective of this lab is to introduce Kubernetes fundamentals by setting up a local single-node cluster using Minikube, deploying an Nginx web server pod, and exposing it to external traffic using a Kubernetes NodePort Service.

## Scenario
As a DevOps engineer supporting an e-commerce platform (Zepto), you are asked to deploy a high-performance storefront landing page inside a Kubernetes Pod so that it can be managed, monitored, and scaled dynamically by the control plane.

---

## Prerequisites
- **Minikube** installed and started (`minikube start`)
- **kubectl** CLI installed and configured (`kubectl version --client`)
- **Docker** container runtime active

---

## Approaches

### Approach 1: Declarative Deployment (Recommended)
Declarative deployment uses YAML configuration files to define the desired state. Kubernetes reconciles the cluster to match this state.

1. **Deploy the Pod**:
   ```bash
   kubectl apply -f web-pod.yaml
   ```

2. **Verify Pod Status**:
   ```bash
   kubectl get pods -o wide
   ```

3. **Deploy the Service**:
   ```bash
   kubectl apply -f web-service.yaml
   ```

4. **Verify Service**:
   ```bash
   kubectl get svc zepto-frontend-svc
   ```

5. **Access the Application**:
   ```bash
   minikube service zepto-frontend-svc
   ```

---

### Approach 2: Imperative CLI Commands
Imperative commands allow rapid testing and experimentation directly from the terminal without YAML manifests.

```bash
# 1. Run Nginx container inside a Pod
kubectl run zepto-frontend --image=nginx:1.25-alpine --port=80

# 2. Check running pods
kubectl get pods

# 3. Expose the Pod via NodePort Service
kubectl expose pod zepto-frontend --type=NodePort --port=80 --name=zepto-frontend-svc

# 4. Open in browser
minikube service zepto-frontend-svc
```

---

## Kubernetes Architecture Overview
When you submit a Pod manifest via `kubectl`:
1. `kubectl` translates the YAML into JSON and sends a REST request to `kube-apiserver`.
2. `kube-apiserver` authenticates the request and stores the Pod specification in `etcd`.
3. `kube-scheduler` detects the unassigned Pod and selects a suitable worker node based on resource requests and affinities.
4. `kubelet` running on the chosen node receives the instruction and invokes the Container Runtime Interface (CRI) (e.g. containerd/docker) to pull the image and launch the container.
5. Container Network Interface (CNI) assigns a cluster-internal IP address to the Pod.
6. `kube-proxy` configures iptables/IPVS rules on the node to route traffic from the Service port to the Pod IP.

---

## Cleanup
To remove the deployed resources:
```bash
kubectl delete -f web-service.yaml
kubectl delete -f web-pod.yaml
```
