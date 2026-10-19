import docker

def run_security_audits():
    client = docker.from_env()

    print("[AUDIT] Starting security audit container with AppArmor profile...")
    container = client.containers.run(
        "chandan-flask-apparmor:latest",
        ports={'5050/tcp': 5050},
        security_opt=["apparmor=docker-flask-secure"],
        detach=True,
        name="flask-audit-runner"
    )

    try:
        # Audit Test 1: Sensitive file reading (/etc/passwd)
        print("\n--- Test 1: Reading sensitive system configuration (/etc/passwd) ---")
        code, out = container.exec_run("cat /etc/passwd")
        print(f"Result -> Exit Code: {code}")
        print(f"Output: {out.decode().strip() if out else '<DENIED / BLOCKED BY APPARMOR>'}")
        if code != 0:
            print("[PASSED] Read access denied to /etc/passwd as intended.")

        # Audit Test 2: Spawning restricted shell binary (/bin/sh)
        print("\n--- Test 2: Executing restricted shell binary (/bin/sh) ---")
        code, out = container.exec_run("/bin/sh -c 'echo shell-escaped'")
        print(f"Result -> Exit Code: {code}")
        print(f"Output: {out.decode().strip() if out else '<EXECUTION BLOCKED BY APPARMOR>'}")
        if code != 0:
            print("[PASSED] Binary execution prevented by AppArmor profile.")

    finally:
        print("\n[CLEANUP] Stopping and removing test container...")
        container.stop()
        container.remove()
        print("[DONE] Security validation complete.")

if __name__ == "__main__":
    run_security_audits()
