create database db_barbearia;
use db_barbearia;

CREATE TABLE produtos
(
    id_produto bigint unsigned not null auto_increment, 
    nome_produto text not null,
    categoria_produto text not null,
    quantidade_produto int not null,
    preco_produto DECIMAL(10,2) not null,
    PRIMARY KEY (id_produto)
);

CREATE TABLE clientes 
(
    id_cliente bigint unsigned not null auto_increment,
    nascimento_cliente date not null,
    email_cliente text not null,
    telefone_cliente text not null,
    observacao_cliente text,
    PRIMARY KEY (id_cliente)
);

CREATE TABLE usuarios 
(
    id_usuario bigint unsigned not null auto_increment,
    nome_usuario text not null,
    telefone_usuario text not null,
    email_usuario text not null,
    senha_usuario text not null,
    PRIMARY KEY (id_usuario)
);

CREATE TABLE servicos
 (
    id_servico bigint unsigned not null auto_increment,
    nome_servico text not null,
    preco_servico decimal(10,2) not null,
    observacao_servico text,
    PRIMARY KEY (id_servico)
);

CREATE TABLE imagens
(
    id_imagem bigint unsigned not null auto_increment,
    imagem blob,
    url_imagem text,
    PRIMARY KEY (id_imagem)
);

CREATE TABLE gastos
(
    id_gasto bigint unsigned not null auto_increment,
    nome_gasto text not null,
    preco_gasto decimal not null,
    descricao_gasto text,
    data_gasto datetime,
    PRIMARY KEY (id_gasto)
);

CREATE TABLE galeria 
(
    id_corte bigint unsigned not null auto_increment,
    nome_corte text not null,
    descricao_corte text,
    fk_id_imagem bigint unsigned,
    PRIMARY KEY (id_corte),
    FOREIGN KEY (fk_id_imagem) REFERENCES imagens(id_imagem)
);

CREATE TABLE agendamentos
(
    id_agendamento bigint unsigned not null auto_increment,
    data_agendamento datetime not null,
    fk_id_cliente bigint unsigned,
    fk_id_usuario bigint unsigned, 
    PRIMARY KEY (id_agendamento),
    FOREIGN KEY (fk_id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (fk_id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE itens_servicos
(
    fk_id_servico bigint unsigned,
    fk_id_venda bigint unsigned,
    FOREIGN KEY (fk_id_servico) REFERENCES servicos(id_servico),
    FOREIGN KEY (fk_id_venda) REFERENCES vendas(id_venda)
);

CREATE TABLE vendas
(
    id_venda bigint unsigned not null auto_increment,
    total_venda decimal not null,
    data_venda datetime not null,
    desconto_venda decimal,
    fk_id_cliente bigint unsigned,
    fk_id_usuario bigint unsigned, 
    PRIMARY KEY (id_venda),
    FOREIGN KEY (fk_id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (fk_id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE itens_produtos
(
    fk_id_produto bigint unsigned,
    fk_id_venda bigint unsigned,
    FOREIGN KEY (fk_id_produto) REFERENCES produtos(id_produto),
    FOREIGN KEY (fk_id_venda) REFERENCES vendas(id_venda)
);