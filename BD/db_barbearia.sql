create database db_barbearia;
use db_barbearia;

CREATE TABLE produtos
 (
    id_produto int unsigned not null auto_increment, 
    nome_produto varchar(50) not null,
    categoria_produto varchar(50) not null,
    quantidade_produto int not null,
    preco_produto DECIMAL(10,2),
    PRIMARY KEY (id_produto)
);

CREATE TABLE itens_produtos
(
    FOREIGN KEY (fk_id_produto) REFERENCES produtos(id_produto),
    FOREIGN KEY (fk_id_venda) REFERENCES vendas(id_venda)
);

CREATE TABLE clientes 
(
    id_cliente int unsigned not null auto_increment,
    nascimento_cliente date not null,
    email_cliente varchar(255) not null,
    telefone_cliente varchar(50) not null,
    observacao_cliente text,
    PRIMARY KEY (id_cliente)
);

CREATE TABLE usuarios 
(
    id_usuario int unsigned not null auto_increment,
    nome_usuario varchar(50) not null,
    telefone_usuario int not null,
    email_usuario varchar(255) not null,
    senha_usuario varchar(50) not null,
    PRIMARY KEY (id_usuario)
);

CREATE TABLE vendas 
(
    id_venda int unsigned not null auto_increment,
    total_venda decimal not null,
    data_venda date not null,
    hora_venda time not null,
    desconto_venda decimal not null,
    PRIMARY KEY (id_venda),
    FOREIGN KEY (fk_id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (fk_id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE servicos
 (
    id_servico int not null auto_increment,
    nome_servico varchar(50) not null,
    preco_servico decimal(10,2) not null,
    observacao_servico text,
    PRIMARY KEY (id_servico)
);

CREATE TABLE itens_servicos
(
    FOREIGN KEY (fk_id_servico) REFERENCES servicos(id_servico),
    FOREIGN KEY (fk_id_venda) REFERENCES vendas(id_venda)
);


CREATE TABLE agendamentos
(
    id_agendamento int not null auto_increment,
    data_agendamento DATE not null,
    Horario_agendamento TIME not null,
    PRIMARY KEY (id_agendamento),
    FOREIGN KEY (fk_id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (fk_id_cliente) REFERENCES clientes(id_cliente)
    );

CREATE TABLE galeria 
(
    id_corte int unsigned not null auto_increment,
    nome_corte varchar(50) not null,
    descricao_corte varchar(50) not null,
    url text,
    PRIMARY KEY (id_corte),
    FOREIGN KEY (fk_id_imagem) REFERENCES imagens(id_imagem)
);

CREATE TABLE imagens
(
    id_imagem int unsigned not null auto_increment,
    imagem blob,
    PRIMARY KEY (id_imagem)
);

CREATE TABLE gastos
(
    id_gasto int unsigned not null auto_increment,
    nome_gasto varchar(50) not null,
    preco_gasto decimal not null,
    descricao_gasto text,
    data_gasto date,
    PRIMARY KEY (id_gasto)
);