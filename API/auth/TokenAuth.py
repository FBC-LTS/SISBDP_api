import json
import os
import dotenv
import datetime
import jwt

dotenv.load_dotenv(dotenv.find_dotenv())

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = str(os.getenv("ALGORITHM") or "HS256")
DAYS_EXPIRE = int(os.getenv("DAYS_EXPIRE") or 30)


class TokenAuth:
    def __init__(self, token = None) -> None:
        if token:
            self.validar(token)


    def buscar_tokens(self):
        with open('keys.json', 'r') as f:
            dados = json.load(f)

        return dados
    

    def validar(self, token):
        self.valido = False
        try:
            payload = jwt.decode(token, SECRET_KEY, ALGORITHM) # type: ignore
        except jwt.DecodeError:
            return None
        
        tempo_atual = datetime.datetime.now(datetime.timezone.utc)
        tempo_token = datetime.datetime.fromtimestamp(payload["exp"]).replace(tzinfo=datetime.timezone.utc)
        if tempo_atual > tempo_token:
            return False
        self.valido = True
        return True