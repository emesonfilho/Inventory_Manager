from tkinter import *
import pymysql
from tkinter import messagebox
from tkinter import ttk
from datetime import date

import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import matplotlib.pyplot as plt

from accont import estoque_compromissos

class JanelaUser():
    def __init__(self):
        self.telaUser = Tk()
        self.telaUser['bg'] = '#191970'

        # SOBRE A SAIDA
        Label(self.telaUser, text="Saida do estoque", width=15, bg='#BDBDBD').grid(row=0, column=0, columnspan=2, padx=5,
                                                                                   pady=5)

        # BOTÕES PARA PLOTAR OS GRÁFICOS
        Button(self.telaUser, text='Gráfico preço', width=15, bg='#D2691E', command = self.grafico_preco).grid(row=5, column=0, padx=5, pady=5)
        Button(self.telaUser, text='Gráfico unidade', width=15, bg='#D2691E', command=self.grafico_quantidade).grid(row=5, column=1, padx=5, pady=5)
        Button(self.telaUser, text='Gráfico total', width=15, bg='#D2691E', command=self.grafico_total).grid(row=6, column=0, padx=5, pady=5)

        # INSERIR O ID DO PRODUTO QUE SAIU
        Label(self.telaUser, text="ID_produto", width=20, bg='#BDBDBD').grid(row=1, column=0, padx=5, pady=5)
        self.id_produto_saida = Entry(self.telaUser)
        self.id_produto_saida.grid(row=1, column=1, padx=5, pady=5)

        # INSERIR A QUANTIDADE DO PRODUTO QUE SAIU
        Label(self.telaUser, text="Quantidade", width=20, bg='#BDBDBD').grid(row=2, column=0, padx=5, pady=5)
        self.quantidade_produto_saida = Entry(self.telaUser)
        self.quantidade_produto_saida.grid(row=2, column=1, padx=5, pady=5)

        # BOTÃO PARA CADASTRAR A SAIDA DOS PRODUTOS
        Button(self.telaUser, text='Confirmar', width=15, bg='#088A08',
               command=self.delete_inteligente).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # BOTÃO PARA ATUALIZAR
        Button(self.telaUser, text='Atualizar', width=15, bg='#DF7401', command=self.att).grid(row=6, column=1, padx=5,pady=5)

        # BOTÃO PARA VER COMPROMISSOS
        Button(self.telaUser, text='Ver compromissos', width=15, bg='#F4FA58',
               command=estoque_compromissos.Compromissos).grid(row=7, column=0, columnspan = 2,padx=5, pady=5)

        self.visualizar_produtos()

    def att(self):
        self.visualizar_produtos_backend()

    def visualizar_produtos(self):
        # VISUALIZAR ALUNOS
        self.tree = ttk.Treeview(self.telaUser, selectmode='browse',
                                 column=("column1", "column2", 'column3', 'column4', 'column5', 'column6'),
                                 show='headings')

        self.tree.column('column1', width=55, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='id_produto')

        self.tree.column('column2', width=160, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Nome')

        self.tree.column('column3', width=100, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Preço')

        self.tree.column('column4', width=100, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Quantidade')

        self.tree.column('column5', width=100, minwidth=500, stretch=NO)
        self.tree.heading('#5', text='Total')

        self.tree.column('column6', width=100, minwidth=500, stretch=NO)
        self.tree.heading('#6', text='Data do cadastro')

        self.tree.grid(row=0, column=2, padx=10, pady=5, columnspan=3, rowspan=10)

        self.visualizar_produtos_backend()

    def visualizar_produtos_backend(self):
        try:
            conexao = pymysql.connect(

                host='localhost',
                user='root',
                password='',
                db='padaria',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showinfo("ERRO", "Erro na hora de conectar ao banco de dados")

        try:
            with conexao.cursor() as cursor:
                cursor.execute(f"SELECT * FROM estoque")
                resultado = cursor.fetchall()
        except:
            messagebox.showinfo("ERRO", "Erro na hora de efetuar cadastro")

        self.tree.delete(*self.tree.get_children())

        ver_produto_estoque = list()
        for linha in resultado:
            ver_produto_estoque.append(linha['id_produto'])
            ver_produto_estoque.append(linha['nome'])
            ver_produto_estoque.append(linha['preco'])
            ver_produto_estoque.append(linha['quantidade'])
            ver_produto_estoque.append(linha['total'])
            ver_produto_estoque.append(linha['data_cadastro'])

            self.tree.insert('', END, values=ver_produto_estoque, iid=linha['id_produto'], tag='1')

            ver_produto_estoque.clear()

    def delete_inteligente(self):
        id = int(self.id_produto_saida.get())
        quantidade = int(self.quantidade_produto_saida.get())

        total = 0
        try:
            conexao = pymysql.connect(

                host='localhost',
                user='root',
                password='',
                db='padaria',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showinfo("ERRO", "Erro na hora de conectar ao banco de dados")

        try:
            with conexao.cursor() as cursor:
                cursor.execute(f"SELECT * FROM estoque")
                resultado = cursor.fetchall()
        except:
            messagebox.showinfo("ERRO", "Erro na hora de efetuar cadastro")

        for a in resultado:
            if a['id_produto'] == id:
                quantidade = a['quantidade'] - quantidade
                total = quantidade * a['preco']

        try:
            with conexao.cursor() as cursor:
                cursor.execute(
                    f"UPDATE estoque SET quantidade = '{quantidade}', total = '{total}' WHERE id_produto = '{id}'")
                conexao.commit()
                messagebox.showinfo("DELETADO", "Mercadoria alterada com sucesso")
        except:
            messagebox.showinfo("ERRO", "Erro na hora de deletar mercadoria")

    def grafico_preco(self):
        try:
            conexao = pymysql.connect(

                host='localhost',
                user='root',
                password='',
                db='padaria',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showinfo("ERRO", "Erro na hora de conectar ao banco de dados")

        try:
            with conexao.cursor() as cursor:
                cursor.execute(f"SELECT * FROM estoque")
                resultado = cursor.fetchall()
        except:
            messagebox.showinfo("ERRO", "Erro na hora de efetuar cadastro")

        nome = list()
        preco = list()

        for a in range(0, len(resultado)):
            if resultado[a]['nome'] not in nome:
                nome.append(resultado[a]['nome'])
                preco.append(resultado[a]['preco'])

        plt.style.use("ggplot")
        plt.barh(nome, preco, color='royalblue')
        plt.title("Preço de cada produto")
        plt.xlabel("Preço unitário")
        plt.ylabel("Produto")
        plt.show()

    def grafico_quantidade(self):
        try:
            conexao = pymysql.connect(

                host='localhost',
                user='root',
                password='',
                db='padaria',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showinfo("ERRO", "Erro na hora de conectar ao banco de dados")

        try:
            with conexao.cursor() as cursor:
                cursor.execute(f"SELECT * FROM estoque")
                resultado = cursor.fetchall()
        except:
            messagebox.showinfo("ERRO", "Erro na hora de efetuar cadastro")

        nome = list()
        quantidade = list()

        for a in range(0, len(resultado)):
            if resultado[a]['nome'] not in nome:
                nome.append(resultado[a]['nome'])
                quantidade.append(resultado[a]['quantidade'])

        plt.style.use("ggplot")
        plt.barh(nome, quantidade, color='royalblue')
        plt.title("Quantidade do produto")
        plt.xlabel("Quantidade de unidades")
        plt.ylabel("Produto")
        plt.show()

    def grafico_total(self):
        try:
            conexao = pymysql.connect(

                host='localhost',
                user='root',
                password='',
                db='padaria',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showinfo("ERRO", "Erro na hora de conectar ao banco de dados")

        try:
            with conexao.cursor() as cursor:
                cursor.execute(f"SELECT * FROM estoque")
                resultado = cursor.fetchall()
        except:
            messagebox.showinfo("ERRO", "Erro na hora de efetuar cadastro")

        nome = list()
        total = list()

        for a in range(0, len(resultado)):
            if resultado[a]['nome'] not in nome:
                nome.append(resultado[a]['nome'])
                total.append(resultado[a]['total'])

        plt.style.use("ggplot")
        plt.barh(nome, total, color='royalblue')
        plt.title("Potencial de lucro do produto")
        plt.xlabel("Total em $")
        plt.ylabel("Produto")
        plt.show()

