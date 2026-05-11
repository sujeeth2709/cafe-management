

def create_access_token(data: dict) -> str:
    raise NotImplementedError("JWT not used in this project. See routers/auth.py.")

def decode_access_token(token: str) -> dict:
    raise NotImplementedError("JWT not used in this project. See routers/_auth_helper.py.")

# Alias in case any old code calls decode_token
decode_token = decode_access_token
