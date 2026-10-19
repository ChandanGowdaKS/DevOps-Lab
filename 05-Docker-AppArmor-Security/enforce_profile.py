import docker
import sys

def main():
    print("[INFO] Connecting to Docker Daemon via Python SDK...")
    client = docker.from_env()

    # Step 1: Build Docker image
    print("[INFO] Building Docker image 'chandan-flask-apparmor:latest'...")
    image, logs = client.images.build(path=".", tag="chandan-flask-apparmor:latest", rm=True)
    for chunk in logs:
        if 'stream' in chunk:
            print(f"  {chunk['stream'].strip()}")

    # Step 2: Run container with AppArmor profile
    print("[INFO] Launching container with '--security-opt apparmor=docker-flask-secure'...")
    container = client.containers.run(
        "chandan-flask-apparmor:latest",
        ports={'5050/tcp': 5050},
        security_opt=["apparmor=docker-flask-secure"],
        detach=True,
        name="flask-apparmor-demo"
    )
    print(f"[SUCCESS] Container started: ID={container.short_id}, Name={container.name}")

    # Step 3: Inspect security configurations
    details = client.api.inspect_container(container.id)
    sec_opts = details['HostConfig'].get('SecurityOpt', [])
    print(f"[VERIFY] HostConfig.SecurityOpt: {sec_opts}")

    # Step 4: Graceful termination
    print("[INFO] Stopping and cleaning up test container...")
    container.stop()
    container.remove()
    print("[SUCCESS] Container cleaned up successfully.")

if __name__ == "__main__":
    main()
