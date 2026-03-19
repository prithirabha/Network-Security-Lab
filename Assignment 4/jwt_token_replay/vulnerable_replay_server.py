from fastapi import FastAPI, Header
import jwt
import datetime

app = FastAPI()

SECRET_KEY = "supersecretkey"

@app.get("/")
def home():
    return {"message": "JWT Replay Attack Demo"}

@app.get("/login")
def login():

    payload = {
        "user": "samyak",
        "role": "user",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {"token": token}

@app.get("/profile")
def profile(authorization: str = Header(None)):

    token = authorization.split(" ")[1]

    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    return {
        "message": "User profile accessed",
        "data": decoded
    }