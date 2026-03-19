from fastapi import FastAPI, Header, HTTPException
import jwt
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "secret"

@app.get("/login")
def login():

    payload = {
        "user": "guest",
        "role": "user",
        "exp": datetime.utcnow() + timedelta(seconds=15)  # short expiry
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {"token": token}


@app.get("/protected")
def protected(authorization: str = Header(None)):

    if authorization is None:
        raise HTTPException(status_code=401, detail="Token missing")

    token = authorization.split(" ")[1]

    # Vulnerable: expiry not checked
    decoded = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=["HS256"],
    options={"verify_exp": False}  # INTENTIONAL VULNERABILITY
    )

    return {
        "message": "Access granted",
        "payload": decoded
    }