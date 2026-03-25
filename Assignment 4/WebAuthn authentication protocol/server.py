from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import base64, os

app = FastAPI()

users = {}

def generate_challenge():
    return os.urandom(32)

def b64encode(data):
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r") as f:
        return f.read()


# 🔹 REGISTER CHALLENGE
@app.get("/register-challenge")
def register_challenge(username: str):
    challenge = generate_challenge()

    users[username] = {
        "challenge": challenge
    }

    return {
        "challenge": b64encode(challenge),
        "rp": {"name": "SecureLab WebAuthn"},
        "user": {
            "id": b64encode(username.encode()),
            "name": username,
            "displayName": username
        },
        "pubKeyCredParams": [
            {"type": "public-key", "alg": -7},
            {"type": "public-key", "alg": -257}
        ],
        "authenticatorSelection": {
            "requireResidentKey": True,
            "userVerification": "required"
        },
        "timeout": 60000,
        "attestation": "none"
    }


# 🔹 STORE CREDENTIAL
@app.post("/register")
async def register(req: Request):
    data = await req.json()
    username = data["username"]

    users[username]["credential"] = data

    return {"message": "Registered successfully"}


# 🔹 LOGIN CHALLENGE
@app.get("/login-challenge")
def login_challenge(username: str):
    if username not in users:
        return {"error": "User not found"}

    challenge = generate_challenge()
    users[username]["challenge"] = challenge

    return {
        "challenge": b64encode(challenge),
        "timeout": 60000
    }


# 🔹 VERIFY LOGIN
@app.post("/login")
async def login(req: Request):
    data = await req.json()
    username = data["username"]

    if username in users and "credential" in users[username]:
        return {"message": "Authentication Successful"}
    
    return {"message": "Authentication Failed"}