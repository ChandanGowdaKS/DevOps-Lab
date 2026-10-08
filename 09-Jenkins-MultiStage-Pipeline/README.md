# Lab 09: Jenkins Multi-Stage Declarative Pipeline

## Objective
Design, configure, and execute a production-style multi-stage **Jenkins Pipeline** (`Jenkinsfile`) for an Order Management Flask microservice. The pipeline models 5 phases:
1. **Build & Dependencies**: Environment configuration and library installation.
2. **Automated Unit Testing**: Executing comprehensive unit test cases (`tests/test_api.py`).
3. **Artifact Staging & Deploy**: Deploying binary/code artifacts to a local staging environment.
4. **Launch Background Service**: Starting the microservice daemon in the background with PID tracking.
5. **Smoke Test & Verification**: Probing live endpoints using `curl` to validate operational readiness.
6. **Teardown**: Gracefully terminating the background process and archiving artifacts.

---

## File Structure
- `app.py`: Flask application with order management and health endpoints.
- `tests/test_api.py`: Automated test cases validating JSON contracts.
- `requirements.txt`: Package manifest (`Flask==2.2.5`).
- `Jenkinsfile`: Declarative Pipeline script controlling stage execution.

---

## Local Verification
```bash
python3 -m unittest discover -s tests
```
Expected output:
```text
...
----------------------------------------------------------------------
Ran 3 tests in 0.005s

OK
```

---

## Setting Up the Pipeline in Jenkins
1. Open Jenkins: `http://localhost:8080`.
2. Click **New Item** -> Name: `Order-Service-MultiStage-Pipeline` -> Choose **Pipeline** -> Click **OK**.
3. Under the **Pipeline** configuration section:
   - **Definition**: `Pipeline script from SCM`
   - **SCM**: `Git`
   - **Repository URL**: `https://github.com/ChandanGowdaKS/DevOps-Lab.git`
   - **Branch Specifier**: `*/main`
   - **Script Path**: `09-Jenkins-MultiStage-Pipeline/Jenkinsfile`
4. Click **Save** and trigger via **Build Now**.

---

## Troubleshooting Jenkins Environment
If running inside a vanilla Jenkins Docker image lacking Python utilities, connect into the container as `root`:
```bash
docker exec -it -u root jenkins-ci-server bash
apt-get update && apt-get install -y python3 python3-pip python3-flask
exit
```
Re-trigger the build in the Jenkins UI to observe all stages completing with green status.
