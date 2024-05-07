import mysql.connector 


conexao = mysql.connector.connect(
    host ='localhost',
    user ='root',
    password ='3634',
    database ='db_barbearia',
)

cursor = conexao.cursor()

#CRUD

nome = "Corte Social"
dados_imagem = "Masculino-ondulado"
descricao = "Cortes-2024"
url = "https://www.sospedro.com.br/2023/12/cortes-de-cabelo-masculino.html"

# Executando a inserção no banco de dados
comando = f'INSERT INTO cortes (nome, dados_imagem, descricao, url) VALUES ("{nome}", "{dados_imagem}", "{descricao}", "{url}")'
cursor.execute(comando)
conexao.commit() # edita o banco de dados!



cursor.close()
conexao.close()

# CREATE
# nome = "Max"
# email = "lucimar7324@hotmail.com"
# telefone = "9999-9999"
# nascimento = "2013.05.13"
# observacao = "Cliente cadastrado!"

# comando = f'INSERT INTO clientes (nome, email, telefone, nascimento, observacao) VALUES ("{nome}", "{email}", "{telefone}", "{nascimento}", "{observacao}")'
# cursor.execute(comando)
# conexao.commit() # edita o banco de dados!

#READ
# comando = f'SELECT * FROM clientes'
# cursor.execute(comando)
# resultado = cursor.fetchall()# ler o banco de dados!
# print(resultado)

#UPDATE
# nome = "Max"
# nascimento = "1984.05.29"
# comando = f'UPDATE clientes SET nascimento = "{nascimento}" WHERE nome = "{nome}"'
# cursor.execute(comando)
# conexao.commit() # edita o banco de dados!

# DELETE
# nascimento = "1984.05.29"
# comando = f'DELETE FROM clientes WHERE nascimento = "{nascimento}"'
# cursor.execute(comando)
# conexao.commit() # edita o banco de dados!