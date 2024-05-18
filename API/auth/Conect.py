import mysql.connector
import os
import dotenv
import logging
import pandas as pd
from passlib.context import CryptContext
from .Modulos.Validador import validar_dado as vd
from .Exceptions import SemDadosException

class Conect:
    def __init__(self) -> None:
        # carregando informações de conexão
        dotenv.load_dotenv(dotenv.find_dotenv())

        self.__host = os.getenv("host")
        self.__user = os.getenv("user")
        self.__password = os.getenv("password")
        self.__database = os.getenv("database")
        self.__port = os.getenv("port")
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    def conectar(self):
        try:
            # conecção
            conexao = mysql.connector.connect(
                host = self.__host,
                user = self.__user,
                password = self.__password,
                database = self.__database,
                port = self.__port
            )
            if conexao.is_connected():
                db_Info = conexao.get_server_info()
                logging.info(
                    msg=f"Conectado ao servidor MySQL versão {db_Info}"
                )
                self.__conexao = conexao 
                self.__cursor = self.__conexao.cursor()

        except Exception as e:
            logging.error(
                msg=f"Erro ao conectar ao MySQL.\n{e}"
            )
            return None


        finally:
            if self.__conexao.is_connected():
                return True
            return False


    def get_produtos(self):
        try:    
            comando = f"""
            SELECT id_produto AS id, nome_produto AS nome, preco_produto AS preco, quantidade_produto, categoria_produto, NULL AS observacao_servico, 'produto' AS tipo
            FROM produtos
            UNION ALL
            SELECT id_servico AS id, nome_servico AS nome, preco_servico AS preco, NULL AS quantidade_produto, NULL AS categoria_produto, observacao_servico, 'servico' AS tipo
            FROM servicos;
            """
            self.__cursor.execute(comando)
            resultado = self.__cursor.fetchall()
            if self.__cursor.description == None:
                raise SemDadosException()
            df = pd.DataFrame(resultado, columns=[i[0] for i in self.__cursor.description])
            msg=f"EXEC - GET PRODUTOS: SUCCESS\n100"
            logging.info(
                    msg
                )
            
            return df, msg
        except SemDadosException as e:
            msg=f"EXEC - GET PRODUTOS:\nERROR: SEM DADOS NO SERVIDOR\n004"
            
            logging.error(msg)

            return pd.DataFrame(), msg
        except Exception as e:
            msg=f"EXEC - GET PRODUTOS:\nERROR: {e}\n000"
            
            logging.error(msg)
            return pd.DataFrame(), msg
        
    def post_produtos(self, dados, tipo):
        if tipo == "produto":
            self.__post_produto(dados["nome"], dados["categoria"], dados["quantidade"], dados["preco"])
        if tipo == "servico":
            self.__post_servico(dados["nome"], dados["preco"], dados["observacao"])
        
    def __post_produto(self, nome:str, categoria:str, quantidade:int, preco:float):
        
        comando = f"""
        INSERT INTO produtos (nome_produto, categoria_produto, quantidade_produto, preco_produto)
        VALUES ('{nome}', '{categoria}', '{quantidade}', '{preco}');
        """

        try:
            self.__cursor.execute(comando)
            self.__conexao.commit()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def __post_servico(self, nome:str, preco:float, obs:str):
        
        comando = f"""
        INSERT INTO servicos (nome_servico, preco_servico, observacao_servico)
        VALUES ('{nome}', '{preco}', '{obs}');
        """

        try:
            self.__cursor.execute(comando)
            self.__conexao.commit()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def delete_produtos(self, tipo, id):
        comando = f"""
        DELETE FROM {tipo + "s"} WHERE id_{tipo} = '{id}';
        """
        try:
            self.__cursor.execute(comando)
            self.__conexao.commit()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")


    def patch_produtos(self, tipo:str, dados:dict, id:int):
        def remove_colunas_desnecessarias(colunas, tipo):
            if tipo == 'servico':
                if "categoria" in colunas.keys():
                    colunas.pop("categoria")
                if "quantidade" in colunas.keys():
                    colunas.pop("quantidade")
            if tipo == 'produtos':
                if "categoria" in colunas.keys():
                    colunas.pop("observacao")
            return colunas
        colunas = {}
        for chave in dados:
            if type(dados[chave]) == str and len(dados[chave]) > 3:
                colunas[chave] = dados[chave]
            if type(dados[chave]) == int and dados[chave] > 0:
                colunas[chave] = dados[chave]
            if type(dados[chave]) == float and dados[chave] > 0:
                colunas[chave] = dados[chave]
        colunas = remove_colunas_desnecessarias(colunas, tipo)
       
        comando = f"UPDATE {tipo + "s"}\nSET"
        for chave in colunas:
            comando += f" {chave+'_'+tipo} = '{colunas[chave]}'"
        comando += f"\nWHERE id_{tipo} = '{id}';"
        try:
            self.__cursor.execute(comando)
            self.__conexao.commit()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        

    def __valida_dados_sensiveis(self, numero, email, senha):

            b_email = vd.validar_email(email)
            b_numero = vd.validar_numero(numero)
            b_senha = vd.validar_senha(senha)
            b_registro = False
            if b_email:
                registro = self.get_user(email)
                b_registro = registro.empty
            
            b_total = b_email and b_senha and b_numero and b_registro
            validade = [
                b_email,
                b_numero,
                b_senha,
                b_registro,
                b_total
            ]


            return validade
    

    def post_usuario(self, nome:str, telefone:str, email:str, senha:str):
        def __get_senha_hash(senha):
            return self.pwd_context.hash(senha)
        
        validade = self.__valida_dados_sensiveis(numero=telefone, email=email, senha=senha)
        if not validade[-1]:
            return validade

        hash_senha = __get_senha_hash(senha)
        comando = f"""
        INSERT INTO usuarios (nome_usuario, telefone_usuario, email_usuario, senha_usuario)
        VALUES ('{str(nome)}', '{str(telefone)}', '{str(email)}', '{str(hash_senha)}');
        """

        try:
            self.__cursor.execute(comando)
            self.__conexao.commit()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        return validade

    def get_user(self, email):
        comando = f"""
        SELECT * FROM usuarios WHERE email_usuario = '{email}'
        """
        self.__cursor.execute(comando)
        resultado = self.__cursor.fetchall()
        if self.__cursor.description == None:
            raise SemDadosException()
        df = pd.DataFrame(resultado, columns=[i[0] for i in self.__cursor.description])
        return df
