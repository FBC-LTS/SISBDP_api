create database db_barbearia;
use db_barbearia;

CREATE TABLE produtos
 (
    id int unsigned not null auto_increment, 
    nome varchar(50) not null,
    categoria varchar(30) not null,
    quantidade int not null,
    preco DECIMAL(10,2),
    PRIMARY KEY (id)
);

CREATE TABLE clientes 
(
    id int unsigned not null auto_increment,
    nascimento date not null,
    idade varchar(50) not null,
    email varchar(255) not null,
    telefone varchar(20) not null,
    PRIMARY KEY (id)
);

CREATE TABLE usuarios 
(
    id int unsigned not null auto_increment,
    nome varchar(50) not null,
    telefone int not null,
    email varchar(50) not null,
    senha varchar(50) notnull,
    PRIMARY KEY (id)
);

CREATE TABLE vendas 
(
    id int unsigned not null auto_increment PRIMARY KEY,
    total decimal not null,
    data date not null,
    hora time not null,
    desconto decimal not null,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE servico
 (
    id int not null auto_increment,
    nome varchar(30) not null,
    preco decimal(10,2) not null,
    observacao varchar(50) not null,
    PRIMARY KEY (id)
);

CREATE TABLE agendamentos
(
    id int not null auto_increment,
    Data DATE not null,
    Horario TIME not null,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    );

CREATE TABLE cortes 
(
    id int unsigned not null auto_increment,
    nome varchar(30) not null,
    dados_imagem longblob,
    descricao varchar(50) not null,
    url varchar(255),
    PRIMARY KEY (id)
);

CREATE TABLE gastos
(
    id int unsigned not null auto_increment,
    nome varchar(30) not null,
    preco decimal not null,
    descricao varchar(50) not null,
    data date,
    PRIMARY KEY (id)
);
