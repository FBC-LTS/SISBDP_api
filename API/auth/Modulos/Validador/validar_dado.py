import re

def validar_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$'
    if re.match(regex, email):
        return True
    else:
        return False

def validar_senha(senha):
    regex = r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'
    if re.match(regex, senha):
        return True
    else:
        return False

def validar_numero(numero):
    regex = r'^\d{10,15}$'
    if re.match(regex, numero):
        return True
    else:
        return False