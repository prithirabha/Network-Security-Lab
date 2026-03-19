from fastapi import FastAPI, Header, HTTPException
import jwt

app = FastAPI()

SECRET_KEY = "secret"

@app.get("/")
def home():
    return {"message": "JWT Secret Key Brute Force Demo"}

# login endpoint
@app.get("/login")
def login():

    payload = {
        "user": "guest",
        "role": "user"
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {"token": token}


# protected admin endpoint
@app.get("/admin")
def admin(authorization: str = Header(None)):

    if authorization is None:
        raise HTTPException(status_code=401, detail="Token missing")

    token = authorization.split(" ")[1]

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        if decoded["role"] != "admin":
            raise HTTPException(status_code=403, detail="Not Admin")

        return {"message": "Welcome Admin!", "payload": decoded}

    except:
        raise HTTPException(status_code=401, detail="Invalid Token")