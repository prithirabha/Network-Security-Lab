import jwt

payload = {
    "user": "attacker",
    "role": "admin"
}

token = jwt.encode(payload, "secret", algorithm="HS256")

print(token)