from fastapi import FastAPI, Header, HTTPException
import jwt

app = FastAPI()

SECRET_KEY = "supersecretkey"

@app.get("/")
def home():
    return {"message": "JWT None Algorithm Attack Demo"}

# Login endpoint to generate token
@app.get("/login")
def login():
    payload = {
        "user": "guest",
        "role": "user"
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {"token": token}

# Protected endpoint (VULNERABLE)
@app.get("/admin")
def admin(authorization: str = Header(None)):

    # prevent crash if header missing
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.split(" ")[1]

    # VULNERABLE decoding
    decoded = jwt.decode(token, options={"verify_signature": False})

    return {
        "message": "Welcome Admin!",
        "decoded_token": decoded
    }