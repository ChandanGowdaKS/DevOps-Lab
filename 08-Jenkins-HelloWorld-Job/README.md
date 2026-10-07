# Lab 08: Creating and Running a "Hello World" Jenkins CI Job

## Objective
Configure an automated build job in Jenkins to pull an executable shell script from a remote Git repository (`ChandanGowdaKS/DevOps-Lab`), execute it as a build step, and inspect the console logs to verify automated build execution.

---

## Files
- `run_job.sh`: Executable bash script printing formatted build telemetry.
- `Jenkinsfile`: Declarative Pipeline definition for running the script.

---

## Instructions

### Step 1: Verify Script Locally
```bash
chmod +x run_job.sh
./run_job.sh
```

### Step 2: Configure Jenkins Freestyle Job
1. Access Jenkins Dashboard at `http://localhost:8080`.
2. Click **New Item** on the left navigation panel.
3. Name the item `Chandan-HelloWorld-Job`.
4. Choose **Freestyle project** and click **OK**.

#### SCM Configuration
- Under **Source Code Management**, select **Git**.
- **Repository URL**: `https://github.com/ChandanGowdaKS/DevOps-Lab.git`
- **Branch Specifier**: `*/main`

#### Build Step Configuration
- Scroll to **Build Steps** and select **Add build step -> Execute shell**.
- Enter command:
  ```bash
  sh 08-Jenkins-HelloWorld-Job/run_job.sh
  ```

#### Save and Trigger
- Click **Save**.
- Click **Build Now** to execute the job.

---

### Step 3: Verify Build Console Output
Navigate to **Build History -> #1 -> Console Output**:
```text
Started by user admin
Running as SYSTEM
Building in workspace /var/jenkins_home/workspace/Chandan-HelloWorld-Job
Cloning the remote Git repository
Cloning repository https://github.com/ChandanGowdaKS/DevOps-Lab.git
 > git init /var/jenkins_home/workspace/Chandan-HelloWorld-Job
Fetching upstream changes from https://github.com/ChandanGowdaKS/DevOps-Lab.git
Checking out Revision 8f23... (refs/remotes/origin/main)
[Chandan-HelloWorld-Job] $ /bin/sh -xe /tmp/jenkins8912384.sh
+ sh 08-Jenkins-HelloWorld-Job/run_job.sh
==========================================================
          Jenkins CI/CD Automation Pipeline               
==========================================================
 Project Name  : DevOps Lab - Hello World Automation Job 
 Author        : Chandan Gowda K S                        
 Host Machine  : jenkins-ci-server                         
 Current User  : jenkins                                   
 Status        : Build Stage Succeeded                    
==========================================================
Hello, World! Jenkins Job executed successfully from Git!
Finished: SUCCESS
```
