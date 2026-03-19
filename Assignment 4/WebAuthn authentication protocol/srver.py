from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import secrets

app = FastAPI()

# Store users (demo only)
users = {}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>WebAuthn Demo</h2>

    <button onclick="register()">Register</button>
    <button onclick="login()">Login</button>

    <script>
    async function register() {
        const res = await fetch("/register");
        const data = await res.json();

        localStorage.setItem("credential", data.credential);
        alert("Registered with credential");
    }

    async function login() {
        const credential = localStorage.getItem("credential");

        const res = await fetch("/login?cred=" + credential);
        const data = await res.json();

        alert(data.message);
    }
    </script>
    """

@app.get("/register")
def register():
    # Simulate public-private key generation
    credential = secrets.token_hex(16)

    users[credential] = True

    return {"credential": credential}

@app.get("/login")
def login(cred: str):
    if cred in users:
        return {"message": "Authentication Successful"}
    return {"message": "Authentication Failed"}