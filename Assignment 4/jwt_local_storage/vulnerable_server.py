from fastapi import FastAPI, Header, HTTPException

from fastapi.responses import HTMLResponse
import jwt

app = FastAPI()

SECRET_KEY = "supersecretkey"

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <body>

    <h2>Login</h2>
    <button onclick="login()">Login</button>

    <h2>User Input (Vulnerable)</h2>
    <input id="input" type="text">
    <button onclick="display()">Submit</button>

    <div id="output"></div>

    <script>
    async function login() {
        const res = await fetch("/login");  // ✅ same origin now
        const data = await res.json();

        localStorage.setItem("token", data.token);
        alert("Token stored");
    }

    function display() {
    const input = document.getElementById("input").value;
    const output = document.getElementById("output");

    output.innerHTML = input;

    // 🔥 Execute script tags manually
    const scripts = output.getElementsByTagName("script");
    for (let script of scripts) {
        eval(script.innerText);
    }
}
    </script>

    </body>
    </html>
    """

@app.get("/login")
def login():
    payload = {
        "user": "samyak",
        "role": "user"
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {"token": token}

@app.get("/stolen_access")
def protected(authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.split(" ")[1]

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "message": "Access granted",
        "user": decoded
    }