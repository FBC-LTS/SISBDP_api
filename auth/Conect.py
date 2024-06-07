from decimal import Decimal
import mysql.connector
import os
import dotenv
import logging
import pandas as pd
import datetime
from passlib.context import CryptContext
from .Modulos.Validador import validar_dado as vd
from .Modulos.Conversor import re_converter_data
from .Exceptions import SemDadosException, NotFound

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
            df['preco'] = df['preco'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
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
    
    def get_produto(self, tipo, id):
        try:
            comando = f"""
            SELECT * FROM {tipo}s WHERE id_{tipo} = '{id}'
            """
            self.__cursor.execute(comando)
            resultado = self.__cursor.fetchall()
            if self.__cursor.description == None:
                raise NotFound()
            df = pd.DataFrame(resultado, columns=[i[0] for i in self.__cursor.description])
            df['preco'] = df['preco'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
            msg=f"EXEC - GET PRODUTO: SUCCESS\n100"
            logging.info(
                    msg
                )
            return df, msg
        
        except NotFound as e:
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
        VALUES ('{nome}', '{categoria}', '{quantidade}', '{preco:.2f}');
        """

        try:
            self.__cursor.execute(comando)
            self.__conexao.commit()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def __post_servico(self, nome:str, preco:float, obs:str):
        
        comando = f"""
        INSERT INTO servicos (nome_servico, preco_servico, observacao_servico)
        VALUES ('{nome}', '{preco:.2f}', '{obs}');
        """

        try:
            self.__cursor.execute(comando)
            self.__conexao.commit()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def delete_generico(self, tipo, id):
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
        colunas = vd.remove_vazias(dados)
        colunas = remove_colunas_desnecessarias(colunas, tipo)
       
        comando = f"UPDATE {tipo}s\nSET"
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
        return self.__executa_comando(comando)
    

    def get_generico(self, tabela):
        comando = f"SELECT * FROM {tabela};"
        df = self.__executa_comando(comando)
        if f'preco_{tabela[:-1]}' in df.keys():
            df[f'preco_{tabela[:-1]}'] = df[f'preco_{tabela[:-1]}'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
        
        return df.to_dict('records')
    
    def post_generico(self, tabela, dados):
        comando = f"INSERT INTO {tabela}s ("

        for dado in dados.items():
            comando += f' {dado[0]}_{tabela},'
        comando = comando[:-1]
        comando += ") VALUES ("

        for dado in dados.items():
            comando += f' \'{dado[1]}\','
        comando = comando[:-1]
        comando += ');'


        try:
            self.__cursor.execute(comando)
            self.__conexao.commit()
            return True
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return False
        
    
    def patch_cliente(self, dados, id):
        colunas = vd.remove_vazias(dados)
        if len(colunas.keys()) < 0:
            return 2

        comando = f"UPDATE clientes\nSET"
        for chave in colunas:
            comando += f" {chave}_cliente = '{colunas[chave]}'"
        comando += f"\nWHERE id_cliente = '{id}';"

        try:
            self.__cursor.execute(comando)
            self.__conexao.commit()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return False
        return True
    

    def get_vendas(self, id=-1):
        comando = f"SELECT * FROM vendas;"
        if id > 0:
            comando = f"SELECT * FROM vendas WHERE id_venda = {id};"
        df = self.__executa_comando(comando)
        df['cliente'] = df['fk_id_cliente'].apply(lambda x: self.__resolve_fk_venda("cliente",x))
        df['usuario'] = df['fk_id_usuario'].apply(lambda x: self.__resolve_fk_venda("usuario",x))
        df = df.drop(columns=['fk_id_cliente', 'fk_id_usuario'])
        df['desconto_venda'] = df['desconto_venda'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
        df['total_venda'] = df['total_venda'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
        df['data_venda'] = df['data_venda'].apply(lambda x: re_converter_data(str(x), '%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M:%S') if isinstance(x, pd.Timestamp) else x)
        df['itens'] = df['id_venda'].apply(self.__seleciona_itens)

        return df.to_dict('records'), True


    def __seleciona_itens(self, id_venda):
        comando = f"""SELECT *, 'produto' AS tipo FROM itens_produtos WHERE fk_id_venda = {id_venda}
                    UNION
                    SELECT *, 'servico' AS tipo FROM itens_servicos WHERE fk_id_venda = {id_venda};"""
        self.__cursor.execute(comando)
        resultado = self.__cursor.fetchall()
        if self.__cursor.description == None:
            raise SemDadosException()
        df_itens = pd.DataFrame(resultado, columns=[i[0] for i in self.__cursor.description])
        list_itens = df_itens.to_dict('records')
        list_itens = self.__formatar_itens(list_itens)
        return list_itens
        

    def __formatar_itens(self, list_itens):
        itens_formatados = []
        for item in list_itens:
            obj_item = {}
            obj_item['tipo'] = item['tipo'] # type: ignore
            obj_item['quantidade_pedida'] = item[f'quantidade_produtos'] # type: ignore

            obj_item['id'] = item[f"fk_id_{obj_item['tipo']}"] # type: ignore
            comando = f"""SELECT nome_{obj_item['tipo']} AS nome, 
                    preco_{obj_item['tipo']} AS preco """
            comando += f"""FROM {obj_item['tipo']}s
                        WHERE id_{obj_item['tipo']} = '{obj_item['id']}'"""
            
            self.__cursor.execute(comando)
            resultado = self.__cursor.fetchall()
            if self.__cursor.description == None:
                raise SemDadosException()
            df_item = pd.DataFrame(resultado, columns=[i[0] for i in self.__cursor.description])
            q_item = df_item.to_dict('records')[0]

            for key in q_item.keys():
                if isinstance(q_item[key], Decimal):
                    q_item[key] = float(q_item[key])
                obj_item[key] = q_item[key]
            
            
            
            itens_formatados.append(obj_item)
            return itens_formatados



    def __resolve_fk_venda(self, tabela, id):
        comando = f"""
        SELECT nome_{tabela} FROM {tabela}s WHERE id_{tabela} = '{id}'
        """
        self.__cursor.execute(comando)
        resultado = self.__cursor.fetchall()
        if self.__cursor.description == None:
            raise SemDadosException()
        return {"id":id, "nome":pd.DataFrame(resultado)[0][0]}

    def __re_set_quantidade(self, id, quantidade):
        comando = f"""SELECT quantidade_produto as quantidade"""
        comando += f""" FROM produtos
                        WHERE id_produto = '{id}'"""
        df = self.__executa_comando(comando)
        quantidade_banco = df['quantidade'][0]
        estoque = quantidade <= quantidade_banco
        if not estoque:
            return False
        nova_quantidade = quantidade_banco - quantidade

        comando = f"UPDATE produtos \nSET quantidade_produto = '{nova_quantidade}'\nWHERE id_produto = '{id}';"

        try:
            self.__cursor.execute(comando)
            self.__conexao.commit()
            return True
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            raise e
        


    
    def __calcular_preco(self, tabela, valor_atual, produto_id, quantidade):
        comando = f"""SELECT preco_produto as preco
                      FROM {tabela}
                      WHERE id_{tabela[:-1]} = '{produto_id}'"""
        df = self.__executa_comando(comando)
        df['preco'] = df['preco'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
        preco = df['preco'][0]
        valor_atual += preco * quantidade
        print(valor_atual)
        return valor_atual
        
    def __calcular_desconto(self, total:float, desconto:float):
        # Calcula o valor do desconto
        valor_desconto = total * desconto
        # Calcula o total após a aplicação do desconto
        total_com_desconto = total - valor_desconto
        
        return total_com_desconto
    
    def __registra_venda(self, total, data, desconto, cliente, usuario):
        comando = f"""
        INSERT INTO vendas (total_venda, data_venda, desconto_venda, fk_id_cliente, fk_id_usuario)
        VALUES ({total}, '{str(data)}', '{str(desconto)}', '{str(cliente)}', '{str(usuario)}');
        """
        try:
            self.__cursor.execute(comando)
            self.__conexao.commit()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return False
        id_venda = self.__cursor.lastrowid
        return id_venda
    
    def __registrar_items(self, tipo, quantidade, id_venda, id_item):
        comando = f"""
        INSERT INTO itens_{tipo}s (quantidade_produtos, fk_id_{tipo}, fk_id_venda)
        VALUES ('{str(quantidade)}', '{str(id_item)}','{str(id_venda)}');
        """
        try:
            self.__cursor.execute(comando)
            self.__conexao.commit()
            return True
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return False
        
    

    def post_venda(self, dados):
        #id_venda, total_venda, data_venda, desconto_venda, fk_id_cliente, fk_id_usuario
        carrinho = dados['carrinho']
        produtos = "produtos" in carrinho.keys()
        servicos = "servicos" in carrinho.keys()
        total = 0
        if produtos:
            for produto in carrinho['produtos']:
                total = self.__calcular_preco('produtos', total, produto['id'], produto['quantidade'])
                self.__re_set_quantidade(produto['id'], produto['quantidade'])
        if servicos:
            for servico in carrinho['servicos']:
                total = self.__calcular_preco('servicos', total, servico['id'], servico['quantidade'])
        
        data = datetime.datetime.now(datetime.timezone.utc)
        data = data.strftime("%Y-%m-%d %H:%M:%S")
        if dados['desconto_venda']:
            total = self.__calcular_desconto(total, dados['desconto_venda'])
        
        id_venda = self.__registra_venda(total, data, dados['desconto_venda'], dados['id_cliente'], dados['id_vendedor'])
        if not id_venda:
            return False
        if produtos:
            for produto in carrinho['produtos']:
                self.__registrar_items("produto", produto['quantidade'], id_venda, produto['id'])
        if servicos:
            for servico in carrinho['servicos']:
                self.__registrar_items("servico", servico['quantidade'], id_venda, servico['id'])
        return True


    def __executa_comando(self, comando):
        self.__cursor.execute(comando)
        resultado = self.__cursor.fetchall()
        if self.__cursor.description == None:
            raise SemDadosException()
        df = pd.DataFrame(resultado, columns=[i[0] for i in self.__cursor.description])
        return df
