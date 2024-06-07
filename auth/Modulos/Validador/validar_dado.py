import re
from datetime import datetime
import logging
from ...Modulos.Conversor import re_converter_data
import json

def gestor_codigos(codigo_erro):
    mapa = {
        "100": "SUCESSO",
        "010": "ERRO TIPO, precisa ser \"produto\" ou \"servico\"",
        "011": "ERRO NOME, minimo 3 caracteres",
        "012": "ERRO PRECO",
        "013": "ERRO CATEGORIA, NOT NULL, minimo 3 caracteres",
        "014": "ERRO QUANTIDADE, NOT NULL",
        "015": "ERRO OBSERVAÇÃO, MAX 400 caracteres",
        "016": "ERRO E-MAIL",
        "017": "ERRO SENHA",
        "018": "ERRO NUMERO",

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
    tipos = ["produto", "servico"]
    if tipo not in tipos:
        return "010"
    if tipo == "produto":
        return validar_produto(nome, preco, categoria, quantidade)
    return validar_servico(nome, preco, obs)

def validar_produto(nome, preco, categoria, quantidade):
    if not validar_nome(nome):
        return "011"
    if not validar_preco(preco):
        return "012"
    if not validar_categoria(categoria):
        return "013"
    if not validar_quantidade(quantidade):
        return "014"
    return "100"

def validar_servico(nome, preco, obs):
    if not validar_nome(nome):
        return "011"
    if not validar_preco(preco):
        return "012"
    if not validar_obs(obs):
        return "015"
    return "100"

def validar_nome(nome):
    if len(nome) < 3:
        return False
    return True

def validar_categoria(categoria):
    if len(categoria) < 3:
        return False
    return True
    
def validar_quantidade(quantidade):
    if type(quantidade) != int or quantidade < 0:
        return False
    return True

def validar_preco(preco):
    if type(preco) != float or preco < 0:
        return False
    return True

def validar_obs(obs):
    if len(obs) > 400:
        return False
    return True

def validar_data_nasc(data_nasc):
    try:
        datetime.strptime(data_nasc, '%d/%m/%Y')
        return True
    except Exception as e:
        return False

def validar_query_cliente(validacao, query):
    res = True
    keys = []
    for dado in validacao.items():
        vazio = query[dado[0]] == ""
        
        if vazio:
            query.pop(dado[0])
            continue

        if dado[0] == "nascimento":
            query[dado[0]] = re_converter_data(query[dado[0]], '%d/%m/%Y', formato_novo="%Y-%m-%d")
        res = res and dado[1]
        if not dado[1]:
            keys.append(dado[0])

    return (keys, res, query)

def remove_vazias(dados):
    colunas = {}
    for chave in dados:
        if type(dados[chave]) == str and len(dados[chave]) > 3:
            colunas[chave] = dados[chave]
        if type(dados[chave]) == int and dados[chave] > 0:
            colunas[chave] = dados[chave]
        if type(dados[chave]) == float and dados[chave] > 0:
            colunas[chave] = dados[chave]
    return colunas

def esta_entre(valor, menor, maior):
    return valor >= menor and valor <= maior

def validar_carrinho(carrinho):
    try:
        carrinho_json = json.loads(carrinho)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return False
    except Exception as e:
        print(e)
        return False
    valida = True
    valida = valida_listas(valida, 'produtos', carrinho_json)
    valida = valida_listas(valida, 'servicos', carrinho_json)

    return valida

def valida_listas(valida, chave, dicionario):
    if not valida:
        return False
    if chave in dicionario.keys():
        lista = dicionario[chave]
        print(lista)
        valida = valida and e_lista(lista)
        print(valida)
        valida = valida and not lista_vazia(lista)
        print(valida)
        valida = valida and itens_tem_attr(lista, "id")
        print(valida)
    return valida

def e_lista(valor):
    return type(valor) == list

def lista_vazia(lista):
    return len(lista) <= 0

def itens_tem_attr(lista, chave):
    valida = True
    for item in lista:
        valida = valida and tem_chave_no_dicionario(item, chave)
    return valida

def tem_chave_no_dicionario(item, chave):
    return chave in item.keys()
