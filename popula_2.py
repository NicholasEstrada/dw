import pandas as pd
import csv
import uuid
import mysql.connector as msql
from mysql.connector import Error

empdata = csv.DictReader(open("C:\\Users\\Nicholas\\Desktop\\dw\\Retail_datas.csv", encoding='utf-8'))
# empdata.head()

try:
    conn = msql.connect(host='localhost', database='dw', user='root', password='', charset="utf8") #give ur username, password
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
except Error as e:
    print("Error while connecting to MySQL", e)


insert_dimenCliente = "insert IGNORE into dw.Dimen_Cliente (Cliente, Pais) "
insert_dimenCliente += "values (%s, %s)"

insert_dimenProduto = "insert into dw.Dimen_Produto (produtoId, Estoque, Descricao, Preco_item, Faixa_preco) "
insert_dimenProduto += "values (%s, %s, %s, %s, %s)"

insert_dimenData = "insert into dw.Dimen_Data (Cod_data, Data_venda, Dia_sem, Mes, Semestre, Ano) "
insert_dimenData += "values (%s, %s, %s, %s, %s, %s)"

insert_fatoVendas = "insert into dw.Fato_Vendas (fatoId, Cod_Vendas, Quantidade, Cod_data, Cliente, Valor_venda, produtoId) "
insert_fatoVendas += "values (%s, %s, %s, %s, %s, %s, %s)"


try:
    for row in empdata:

        clienteRow = (
            row['Cliente'],
            row['Pais']
        )        
        cursor.execute(insert_dimenCliente, clienteRow)
        conn.commit()
        print('Número: {}, Post Id: {}'.format(row['Cliente'],row['Pais']))

        produtoId = uuid.uuid4()
        produtoRow = (
            '{}'.format(produtoId), row['Estoque'], row['Descricao'], row['Preco_item'],row['Faixa_preco']
        )
        cursor.execute(insert_dimenProduto, produtoRow)
        conn.commit()
        print('Número: {}, Post Id: {} # {} # {}'.format(produtoId, row['Estoque'], row['Descricao'], row['Preco_item'],row['Faixa_preco']))

        dataId = uuid.uuid4()
        dataRow = (
            '{}'.format(dataId), row['Data_venda'], row['Dia_sem'], row['Mes'], row['Semestre'], row['Ano']
        )
        
        cursor.execute(insert_dimenData, dataRow)
        conn.commit()
        print('Número: {}, Post Id: {} # {} # {} # {}'.format(row['Data_venda'], row['Dia_sem'], row['Mes'], row['Semestre'], row['Ano']))
        
        fatoId = uuid.uuid4()
        valor_venda = int(row['Quantidade']) * float(row['Preco_item'])
        fatoRow = (
            '{}'.format(fatoId), row['Cod_Venda'], row['Quantidade'], '{}'.format(dataId), row['Cliente'], valor_venda, '{}'.format(produtoId)
        )
        cursor.execute(insert_fatoVendas, fatoRow) #fatoId, Cod_Vendas, Quantidade, Cod_data, Cliente, Valor_venda
        conn.commit()
        print('Número: {}, Post Id: {} # {} # {} # {} # {} # {}R'.format(fatoId , row['Cod_Venda'],row['Quantidade'], dataId, row['Cliente'], valor_venda, produtoId))

        
except Error as e:
    print("Erro ao inserir dados: %s" % e)

