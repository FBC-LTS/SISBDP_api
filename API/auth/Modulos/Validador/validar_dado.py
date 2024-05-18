import re

def gestor_codigos(codigo_erro):
    mapa = {
        "100": "SUCESSO",
        "010": "ERRO TIPO, precisa ser \"produto\" ou \"servico\"",
        "011": "ERRO NOME, minimo 3 caracteres",
        "012": "ERRO PRECO",
        "013": "ERRO CATEGORIA, NOT NULL, minimo 3 caracteres",
        "014": "ERRO QUANTIDADE, NOT NULL",
        "015": "ERRO OBSERVAÇÃO, MAX 400 caracteres"
    }
    if str(codigo_erro) in mapa.keys():
        return mapa[str(codigo_erro)]
    return f"O ERRO {codigo_erro} NÃO É REGISTRADO"

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
    
def validar_produtos(tipo, nome, preco, categoria, quantidade, obs):
    """
    100 SUCESSO
    010 ERRO TIPO\n
    011 ERRO NOME\n
    012 ERRO PRECO\n
    013 ERRO CATEGORIA\n
    014 ERRO QUANTIDADE\n
    015 ERRO OBSERVAÇÃO\n
    """
    tipos = ["produto", "servico"]
    if tipo not in tipos:
        return "010"
    if tipo == "produto":
        return validar_produto(nome, preco, categoria, quantidade)
    return validar_servico(nome, preco, obs)

def validar_produto(nome, preco, categoria, quantidade):
    if len(nome) < 3:
        return "011"
    if type(preco) != float or preco < 0:
        return "012"
    if len(categoria) < 2:
        return "013"
    if type(quantidade) != int or quantidade < 0:
        return "014"
    return "100"

def validar_servico(nome, preco, obs):
    if len(nome) < 3:
        return "011"
    if type(preco) != float or preco < 0:
        return "012"
    if len(obs) > 400:
        return "015"
    return "100"

