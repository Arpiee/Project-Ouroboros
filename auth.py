import json
import os
import hashlib

USERS_FILE = "users.json"
HISTORY_FILE = "idea_history.json"

# -----------------------------
# Helpers
# -----------------------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# -----------------------------
# USER AUTH
# -----------------------------
def create_user(username: str, password: str) -> bool:
    users = load_json(USERS_FILE)

    if username in users:
        return False  # user exists

    users[username] = {
        "password": hash_password(password),
        "profile": {
            "full_name": "",
            "role": "",
            "focus": ""
        }
    }

    save_json(USERS_FILE, users)
    return True

def login_user(username: str, password: str) -> bool:
    users = load_json(USERS_FILE)

    if username not in users:
        return False

    return users[username]["password"] == hash_password(password)

# -----------------------------
# PROFILE MANAGEMENT
# -----------------------------
def get_user_profile(username: str):
    users = load_json(USERS_FILE)
    if username not in users:
        return None
    return users[username].get("profile", {})

def update_user_profile(username: str, data: dict):
    users = load_json(USERS_FILE)
    if username not in users:
        return False

    users[username]["profile"].update(data)
    save_json(USERS_FILE, users)
    return True

# -----------------------------
# IDEA HISTORY
# -----------------------------
def save_idea_history(username: str, idea_data: dict):
    history = load_json(HISTORY_FILE)

    if username not in history:
        history[username] = []

    history[username].append(idea_data)
    save_json(HISTORY_FILE, history)

def load_idea_history(username: str):
    history = load_json(HISTORY_FILE)
    return history.get(username, [])
