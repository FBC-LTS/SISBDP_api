import mysql.connector
import os
import dotenv
import logging
import pandas as pd
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