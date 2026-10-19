# Lab 05: Docker Security with AppArmor Profiles & Python Automation

## Objective
Implement mandatory access control (MAC) security profiles using Linux **AppArmor** to confine a Dockerized Python web application, preventing privilege escalation, arbitrary binary execution, and unauthorized access to host filesystem trees. Automate deployment and security validation using the **Docker SDK for Python**.

---

## Technical Context
Default container runtimes rely on namespaces and cgroups, which provide resource virtualization but not full protection against kernel exploit paths or compromised application processes.
AppArmor restricts what files a process can read, write, or execute, as well as restricting network and kernel capabilities.

---

## Profile Breakdown (`docker-flask-secure`)
- **Restricted Directories**: Access to `/etc/**`, `/var/**`, and `/root/**` is explicitly set to `deny`.
- **Restricted Execution**: Executing system shells or binaries under `/bin/**` and `/usr/bin/**` is blocked.
- **Allowed Sandbox**: Full read/write is allowed exclusively inside the app directory `/app/**`.
- **Capabilities**: Drops `CAP_SYS_ADMIN` and `CAP_SYS_PTRACE`, granting only basic network binding.

---

## Instructions

### Step 1: Install AppArmor Utilities (Linux/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install -y apparmor-utils python3-pip
pip install docker
```

### Step 2: Load and Parse Profile into Linux Kernel
Copy and load the profile:
```bash
sudo cp docker-flask-secure /etc/apparmor.d/
sudo apparmor_parser -r /etc/apparmor.d/docker-flask-secure
```
Confirm the profile is enforced:
```bash
sudo aa-status | grep docker-flask-secure
```

### Step 3: Run Container Manually via Docker CLI
```bash
docker build -t chandan-flask-apparmor:latest .
docker run -d --name flask-secure-app \
  --security-opt="apparmor=docker-flask-secure" \
  -p 5050:5050 chandan-flask-apparmor:latest
```

### Step 4: Automate Deployment via Python Docker SDK
Run the automated deployment script:
```bash
python3 enforce_profile.py
```
Output confirms:
```text
[INFO] Launching container with '--security-opt apparmor=docker-flask-secure'...
[SUCCESS] Container started: ID=d8e41bf9, Name=flask-apparmor-demo
[VERIFY] HostConfig.SecurityOpt: ['apparmor=docker-flask-secure']
```

### Step 5: Execute Security Audits
Run probe tests against restricted paths:
```bash
python3 verify_security.py
```
Expected Output:
```text
--- Test 1: Reading sensitive system configuration (/etc/passwd) ---
Result -> Exit Code: 1
Output: <DENIED / BLOCKED BY APPARMOR>
[PASSED] Read access denied to /etc/passwd as intended.

--- Test 2: Executing restricted shell binary (/bin/sh) ---
Result -> Exit Code: 126
Output: <EXECUTION BLOCKED BY APPARMOR>
[PASSED] Binary execution prevented by AppArmor profile.
```

---

## Lab Questions & Answers

### 1. What role does AppArmor play in container security?
**Answer:** AppArmor acts as a Linux Security Module (LSM) that provides Mandatory Access Control (MAC). While Docker namespaces isolate process IDs and mounts, AppArmor restricts what actions those processes can perform on the underlying filesystem, sockets, and kernel capabilities, mitigating zero-day vulnerabilities and container escape risks.

### 2. How do AppArmor profiles establish security boundaries for containerized applications?
**Answer:** Profiles associate path-based rules with executables. When a process attempts an action (e.g. `open()` or `execve()`), the Linux kernel checks the process's AppArmor confinement profile. If the action is denied or not explicitly allowed, the kernel immediately halts the operation with `EACCES` (Permission denied).

### 3. Why is blocking read/write access to `/etc` and `/var` critical?
**Answer:** `/etc` houses sensitive OS configuration, password hashes (`/etc/shadow`), system accounts (`/etc/passwd`), and SSL certificates. `/var` stores system logs, mail queues, and dynamic runtime data. Restricting these directories stops reconnaissance, credential exfiltration, and host tampering if an application process is compromised.

### 4. What additional capabilities can be restricted via AppArmor?
**Answer:**
- Kernel administration capabilities (`CAP_SYS_ADMIN`, `CAP_SYS_MODULE`)
- Process inspection and tracing (`CAP_SYS_PTRACE`)
- Raw disk access (`CAP_SYS_RAWIO`)
- Network socket operations (raw sockets, packet sniffing)

### 5. How can you verify that a container is running under AppArmor confinement?
**Answer:**
Run `docker inspect <container-id> --format '{{json .HostConfig.SecurityOpt}}'`. Alternatively, check the host's `/proc` filesystem: `cat /proc/<container_pid>/attr/current`, which prints the active AppArmor profile name.
