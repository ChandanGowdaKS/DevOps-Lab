# Lab 02: Deploying a Python Flask App on Minikube

## Objective
Containerize a custom Python Flask microservice using Docker and deploy it to a single-node Minikube cluster using declarative Kubernetes Deployment and Service manifests.

## Key Learning Concepts
- Building custom application container images directly inside Minikube's Docker daemon.
- Writing declarative Kubernetes Deployment specifications with replica control and resource constraints.
- Exposing the microservice internally and externally using a `NodePort` Service.
- Inspecting pod logs and container lifecycle events using `kubectl`.

---

## Step-by-Step Implementation

### Step 1: Initialize Minikube
Start your local Kubernetes cluster:
```bash
minikube start
```

### Step 2: Configure Docker CLI to Use Minikube Daemon
By default, `docker build` builds images in your host's Docker daemon. To build directly inside Minikube's internal container runtime so Kubernetes can access it without a remote registry:
```bash
eval $(minikube docker-env)
```

### Step 3: Build the Application Image
Build the container image tagged as `zepto-catalog:latest`:
```bash
docker build -t zepto-catalog:latest .
```

Verify that the image is present:
```bash
docker images | grep zepto-catalog
```

### Step 4: Apply Kubernetes Manifests
Deploy the Deployment and Service objects:
```bash
kubectl apply -f deployment.yaml
```

Check the rollout status:
```bash
kubectl rollout status deployment/zepto-catalog-deploy
kubectl get pods -l app=zepto-catalog -o wide
kubectl get svc zepto-catalog-svc
```

### Step 5: Test the API Endpoint
Retrieve the service URL from Minikube:
```bash
minikube service zepto-catalog-svc --url
```

Query the endpoints with `curl`:
```bash
# Test root endpoint
curl $(minikube service zepto-catalog-svc --url)

# Test health check
curl $(minikube service zepto-catalog-svc --url)/api/health
```

Expected JSON response:
```json
{
  "container_id": "zepto-catalog-deploy-7c858bd9f-9kxwt",
  "environment": "development",
  "message": "Welcome to Zepto fast-delivery catalog API on Kubernetes!",
  "service": "Zepto Product Catalog Microservice",
  "status": "UP"
}
```

---

## Teardown
```bash
kubectl delete -f deployment.yaml
```
