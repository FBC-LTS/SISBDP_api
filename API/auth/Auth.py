import pandas as pd
import jwt
import json
import datetime
import os
import dotenv
from datetime import timedelta
from .Conect import Conect
from .Modulos.Validador.validar_dado import validar_email
from .TokenAuth import TokenAuth


dotenv.load_dotenv(dotenv.find_dotenv())

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
DAYS_EXPIRE = int(os.getenv("DAYS_EXPIRE") or 30)

class Auth(Conect):
    def __init__(self, email, senha) -> None:
        super().__init__()
        super().conectar()

    
        self.email = email
        self.__pwd_context = self.pwd_context
        self.autenticado = self.__atuenticar(email, senha)
        self.token_auth = TokenAuth()

    def __atuenticar(self, email, senha):
        autenticado = False
        df = pd.DataFrame()
        if validar_email(email):
            df = super().get_user(email)
            
        if not df.empty:
            resultado = df.to_dict()

            if self.__verifica_senha(senha, resultado['senha_usuario'][0]):
                self.usuario = resultado['nome_usuario'][0]
                autenticado = True
  
        
        return autenticado


    def __verifica_senha(self, senha_plana, senha_hashed):
        return self.__pwd_context.verify(senha_plana, senha_hashed)
    
    def token(self):
        tokens = self.token_auth.buscar_tokens()

        if self.email in tokens.keys():
            token = tokens[self.email]
            if self.token_auth.validar(token):
                return token
            
        token = self.__gerar_tokens(tokens)
        return token

    def __gerar_tokens(self, dados):
        exp = datetime.datetime.now(datetime.UTC) + timedelta(days=DAYS_EXPIRE)
        payload = {
            "usuario": self.usuario,
            "exp": exp
        }
        token = jwt.encode(
            payload, SECRET_KEY, ALGORITHM
        ) 
        dados[self.email] = token
        with open('keys.json', 'w') as f:
            json.dump(dados, f)
        return token
    

