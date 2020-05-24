GRANT ALL ON *.* TO root@'%' IDENTIFIED BY 'root';
create database crowd;
use crowd;
create table estoque(
   id_estoque INT NOT NULL AUTO_INCREMENT,
   valor decimal(15,2),
   quantidade INT(250),
   categoria VARCHAR(100) NOT NULL,
   produto VARCHAR(40) NOT NULL,
   user_id INT(250),
   PRIMARY KEY (id_estoque)
);


create table venda(
   id_venda INT NOT NULL AUTO_INCREMENT,
   valor decimal(15,2),
   quantidade INT(250),
   categoria VARCHAR(100) NOT NULL,
   produto VARCHAR(40) NOT NULL,
   user_id int(250),
   date_now datetime NOT NULL, 
   PRIMARY KEY (id_venda)
);

create table produtos(
   id_produto INT NOT NULL AUTO_INCREMENT,
   produto VARCHAR(250),
   valor decimal(15,2),
   descricao VARCHAR(100),
   quantidade INT(250),
   categoria VARCHAR(100) NOT NULL,
   id_user int(250),
   PRIMARY KEY (id_produto)
);

create table user(
   id_user INT NOT NULL AUTO_INCREMENT,
   nome VARCHAR(250),
   sobrenome VARCHAR(100),
   cpf INT(13),
   telefone INT(250),
   email VARCHAR(250),
   cep VARCHAR(250),
   password VARCHAR(100) NOT NULL,
   PRIMARY KEY (id_user)
);
