from fastapi import FastAPI, Header, HTTPException
import jwt
import uuid
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "secret"

# store used token IDs
used_tokens = set()


@app.get("/login")
def login():

    token_id = str(uuid.uuid4())

    payload = {
        "user": "guest",
        "role": "user",
        "jti": token_id,
        "exp": datetime.utcnow() + timedelta(minutes=10)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {"token": token}


@app.get("/protected")
def protected(authorization: str = Header(None)):

    if authorization is None:
        raise HTTPException(status_code=401, detail="Token missing")

    token = authorization.split(" ")[1]

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        token_id = decoded["jti"]

        # replay detection
        if token_id in used_tokens:
            raise HTTPException(status_code=401, detail="Token replay detected")

        used_tokens.add(token_id)

        return {
            "message": "Access granted",
            "payload": decoded
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")