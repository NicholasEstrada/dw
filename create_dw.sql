DROP DATABASE dw;
CREATE DATABASE dw;

USE dw;

CREATE TABLE Dimen_Cliente
(
	Cliente int NOT NULL,
	Pais text NOT NULL,
	Constraint PK_Cliente Primary Key (Cliente) 
);

CREATE TABLE Dimen_Produto
(
	produtoId varchar(255) NOT NULL,
    Estoque varchar(255) NOT NULL,
    Descricao text NOT NULL,
    Preco_item float NOT NULL, 
    Faixa_preco float NOT NULL,
    Constraint PK_Produto Primary Key (produtoId)
);

CREATE TABLE Dimen_Data
(
    Cod_data varchar(255) NOT NULL,
    Data_venda int NOT NULL,
    Dia_sem text NOT NULL,
    Mes int NOT NULL,
    Semestre int NOT NULL,
    Ano int NOT NULL,
    Constraint PK_Data Primary Key (Cod_data)
);

CREATE TABLE Fato_Vendas 
(
	fatoId varchar(255) NOT NULL,
    Cod_Vendas int NOT NULL, 
	Cliente int NOT NULL,
	Cod_data varchar(255) NOT NULL,
	produtoId varchar(255) NOT NULL,
	Quantidade int NOT NULL,
	Valor_venda float NOT NULL,
	Constraint PK_Fato Primary Key (fatoId),
	Constraint FK_Cliente Foreign Key (Cliente)
	references Dimen_Cliente (Cliente),
    Constraint FK_Data Foreign Key (Cod_data)
    references Dimen_Data (Cod_data),
    Constraint FK_Estoque Foreign Key (produtoId)
    references Dimen_Produto (produtoId)
);
