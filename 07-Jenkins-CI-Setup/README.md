# Lab 07: Continuous Integration Fundamentals & Jenkins Server Setup

## What is Continuous Integration (CI)?
**Continuous Integration (CI)** is a software engineering methodology in which members of a team integrate their work into a shared mainline repository multiple times a day. Each commit triggers an automated build-and-test sequence to detect syntax errors, integration conflicts, and regression defects as early as possible.

---

## The CI Automation Feedback Loop

```
+------------------+         +------------------+         +------------------+
| 1. Developer     |  Push   | 2. Version       | Webhook | 3. CI Server     |
|    Workstation   | ------> |    Control (Git) | ------> |    (Jenkins)     |
+------------------+         +------------------+         +--------+---------+
         ^                                                         |
         |                   Feedback Notification                 |
         +---------------------------------------------------------+
                                (Success / Failure)
```

---

## Comparison of Leading CI/CD Solutions

| CI/CD Tool | Architecture | Key Advantages | Best Suited For |
|---|---|---|---|
| **Jenkins** | Controller/Agent (Self-hosted) | Open-source, plugin ecosystem (1800+), customizable pipelines | Enterprise on-prem / cloud-custom setups |
| **GitHub Actions** | Cloud / Self-hosted Runners | Deep GitHub integration, marketplace workflows, zero-setup | GitHub-first software projects |
| **GitLab CI** | GitLab Runner Agent | Native single-application DevOps platform, built-in registry | Teams utilizing full GitLab stack |
| **CircleCI** | Cloud SaaS / Server | Fast container caching, optimized parallelism, Docker native | High-speed agile SaaS teams |
| **Travis CI** | Hosted Cloud | Pioneer in open source CI, declarative `.travis.yml` | Open source public libraries |
| **Azure Pipelines** | Cloud / Agent Pools | Seamless integration with Microsoft ecosystem, multi-OS support | Enterprise Azure-based environments |
| **TeamCity** | Server / Build Agents | Kotlin-based configuration DSL, advanced build analytics | Multi-technology enterprise teams |
| **Atlassian Bamboo** | Server | Direct traceability with Jira tickets and Bitbucket | Atlassian ecosystem users |
| **Drone CI** | Ephemeral Containers | Ultra-lightweight, every step runs inside dedicated container | Cloud-native microservices |
| **ArgoCD** | GitOps Controller | Kubernetes-native continuous delivery via declarative GitOps | K8s GitOps application delivery |

---

## Jenkins Controller-Agent Topology

```
+-----------------------------------------------------------------+
|                   JENKINS CONTROLLER (MASTER)                   |
|  - Manages Web UI & Webhooks                                    |
|  - Dispatches build jobs                                        |
|  - Archives build artifacts & logs                              |
+--------------------------------+--------------------------------+
                                 |
                                 | TCP Port 50000 (JNLP/SSH)
                                 v
        +------------------------+------------------------+
        |                                                 |
        v                                                 v
+-------------------------------+ +-------------------------------+
|     BUILD WORKER (AGENT 1)    | |     BUILD WORKER (AGENT 2)    |
| - Docker build engine         | | - Python / Unit Test runner   |
| - Isolated build workspace    | | - Isolated build workspace    |
+-------------------------------+ +-------------------------------+
```

---

## Installation & Deployment

### Step 1: Launch Jenkins via Docker
Using the provided `docker-compose.yml`:
```bash
docker compose up -d
```
Or via single command:
```bash
docker run -d \
  --name jenkins-ci-server \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home_volume:/var/jenkins_home \
  jenkins/jenkins:lts-jdk17
```

### Step 2: Extract Initial Admin Secret
```bash
docker exec -it jenkins-ci-server cat /var/jenkins_home/secrets/initialAdminPassword
```
Copy the generated 32-character hexadecimal key.

### Step 3: Complete Setup Wizard
1. Open browser to `http://localhost:8080`.
2. Enter the administrator unlock password.
3. Select **Install suggested plugins** (installs Git, Pipeline, Credentials, Workspace Cleanup).
4. Create your Admin user profile.
5. Save and proceed to the Jenkins Dashboard.
