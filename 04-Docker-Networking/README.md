# Lab 04: Docker Networking – Multi-Container Communication

## Objective
Explore Docker networking primitives, isolate multi-tier applications using custom user-defined bridge networks, and leverage Docker's built-in DNS server for automatic service discovery.

---

## Architecture
The application consists of three decoupled micro-services residing inside a private bridge network (`custom-app-network`):
1. **Flask API Gateway (`backend-api`)**: Web application container exposing port `5000`.
2. **Database Container (`mysql-db`)**: Relational database engine (`mysql:8.0`).
3. **In-Memory Cache (`redis-cache`)**: Key-value data store (`redis:7-alpine`).

```
+-----------------------------------------------------------+
|               DOCKER BRIDGE: custom-app-network           |
|                                                           |
|  [backend-api] <====== Embedded DNS ======> [mysql-db]    |
|   (Port 5000)                                (Port 3306)  |
|        ^                                                  |
|        |=========== Embedded DNS ==========> [redis-cache]|
|                                              (Port 6379)  |
+-----------------------------------------------------------+
        |
   Host Port: 5000
```

---

## Step-by-Step Execution

### Step 1: Create a Custom Bridge Network
Create an isolated software bridge:
```bash
docker network create --driver bridge custom-app-network
```

### Step 2: Inspect Network Configuration
Inspect subnet allocations, IPAM configurations, and connected container interfaces:
```bash
docker network inspect custom-app-network
```

### Step 3: Build & Launch Containers Manually (or with Compose)
```bash
# Build the Flask backend
docker build -t flask-backend:1.0 .

# Run MySQL
docker run -d --name mysql-db --net=custom-app-network \
  -e MYSQL_ROOT_PASSWORD=securepassword123 mysql:8.0

# Run Redis
docker run -d --name redis-cache --net=custom-app-network \
  redis:7-alpine

# Run Flask Backend
docker run -d --name backend-api --net=custom-app-network \
  -p 5000:5000 flask-backend:1.0
```

*(Alternatively: run `docker compose up -d`)*

### Step 4: Verify Container Connectivity via DNS
Open a shell session inside the Flask container:
```bash
docker exec -it backend-api bash
```

Ping other containers using container names (testing internal DNS resolution):
```bash
ping -c 3 mysql-db
ping -c 3 redis-cache
exit
```

### Step 5: Test Web API Endpoint
```bash
curl http://localhost:5000/api/status
```

Expected Response:
```json
{
  "connected_tiers": {
    "cache": "redis-cache:6379",
    "database": "mysql-db:3306"
  },
  "service": "Flask REST Gateway",
  "status": "online"
}
```

---

## Lab Review Questions & Answers

### Q1: What does the `--net` parameter achieve during `docker run`?
**Answer:** The `--net` (or `--network`) flag attaches the newly spawned container to a specific Docker network. This determines the container's IP subnet, gateway, isolation boundaries, and access to internal DNS service discovery.

### Q2: How do containers discover and reach each other across a user-defined bridge?
**Answer:** Docker runs an embedded DNS resolver at `127.0.0.11`. When a container on a user-defined bridge issues a lookup for a peer container name (e.g. `mysql-db`), Docker's DNS intercepts the query and returns that container's dynamically allocated IP address on the network.

### Q3: How do Bridge networks differ fundamentally from Host networks in Docker?
**Answer:**
- **Bridge Network**: Implements network namespace virtualization. Containers receive isolated IP addresses on a virtual subnet (`veth` pair connected to `docker0` or user bridge). Ports must be forwarded to the host.
- **Host Network**: Strips away network isolation. The container directly binds to the host's physical network interfaces and port space without NAT overhead.

### Q4: How is container port publication handled to allow host traffic?
**Answer:** Port mapping is defined using the `-p <host_port>:<container_port>` flag. Docker utilizes kernel `iptables` NAT PREROUTING rules to translate incoming packets on the host port and forward them to the target container IP and port.

---

## Teardown
```bash
docker stop backend-api mysql-db redis-cache
docker rm backend-api mysql-db redis-cache
docker network rm custom-app-network
```
