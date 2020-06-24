GRANT ALL ON *.* TO root@'%' IDENTIFIED BY 'root';
create database crowd;
use crowd;
create table estoque(
   id_estoque INT NOT NULL AUTO_INCREMENT,
   valor decimal(15,2),
   quantidade INT(250),
   categoria VARCHAR(100) NOT NULL,
   produto VARCHAR(40) NOT NULL,
   id_user INT(250),
   PRIMARY KEY (id_estoque)
);


create table venda(
   id_venda INT NOT NULL AUTO_INCREMENT,
   valor decimal(15,2),
   quantidade INT(250),
   categoria VARCHAR(100) NOT NULL,
   produto VARCHAR(40) NOT NULL,
   id_user int(250),
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
   cpf VARCHAR(255),
   telefone VARCHAR(250),
   email VARCHAR(250),
   cep VARCHAR(250),
   caixa decimal(15,2),
   password VARCHAR(100) NOT NULL,
   m_cred INT(255),
   lucro_perc INT(10),
   invest INT(255),
   dividendo INT(255),
   wallet decimal(15,2) DEFAULT 0,
   perfil INT (10),
   PRIMARY KEY (id_user)
);

create table wallet_adm (
  m_cred INT(255),
  invest  INT(255),
  dividendo INT(255)
);
INSERT INTO `crowd`.`user` (`id_user`, `nome`, `sobrenome`, `cpf`, `telefone`, `email`, `cep`, `caixa`, `password`, `m_cred`, `lucro_perc`, `wallet`) VALUES ('1', 'administrador', 'adm', 'adm', '000000000000', 'adm@adm', '06315370', '0', 'SmhAdzI0MDkxNA==\'', '0', '104', '0');

