import jwt
from functools import wraps
from flask import request

def validate_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        token = request.headers.get('token')
        if not token:
            return 'Não permitido', 403

        try:
            dados = jwt.decode(token, "SENHA_TOKEN", algorithms=["HS256"])
            request.user = dados

        except Exception:
            return 'Token invalido ou expirado', 403

        return f(*args, **kwargs)
    return decorated_function