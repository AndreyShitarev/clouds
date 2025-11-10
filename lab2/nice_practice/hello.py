import os

def read_secret(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception:
        return None

if __name__ == "__main__":
    print("nice practice tesr start")
    print("User UID:", os.getuid())
    secret_path = os.environ.get("ADMIN_SECRET_PATH")
    secret = read_secret(secret_path) if secret_path else None
    if secret:
        print("Secret file detected")
    else:
        print("No secret file found")
