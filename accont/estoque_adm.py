from tkinter import *
import pymysql
from tkinter import messagebox
from tkinter import ttk
from datetime import date
from datetime import datetime
import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import matplotlib.pyplot as plt

from accont import estoque_compromissos

class JanelaAdm():
    def __init__(self):
        self.telaAdm = Tk()
        self.telaAdm['bg'] = '#191970'

        # TÍTULO DA JANELA
        Label(self.telaAdm, text="Entrada do estoque", width=15, bg='#BDBDBD').grid(row=0, column=0, columnspan=2, padx=5,pady=5)

        # <<<<<=== SOBRE O CADASTRO DE PRODUTOS ===>>>>>

        # INSERIR O NOME DO PRODUTO
        Label(self.telaAdm, text="Nome do produto", width=20, bg='#BDBDBD').grid(row=1, column=0, padx=5, pady=5)
        self.produto_nome = Entry(self.telaAdm)
        self.produto_nome.grid(row=1, column=1, padx=5, pady=5)

        # INSERIR O PREÇO DO PRODUTO
        Label(self.telaAdm, text="Preço do produto", width=20, bg='#BDBDBD').grid(row=2, column=0, padx=5, pady=5)
        self.produto_preco = Entry(self.telaAdm)
        self.produto_preco.grid(row=2, column=1, padx=5, pady=5)

        # INSERIR A QUANTIDADE DE PRODUTO
        Label(self.telaAdm, text="Quantidade", width=20, bg='#BDBDBD').grid(row=3, column=0, padx=5, pady=5)
        self.produto_quantidade = Entry(self.telaAdm)
        self.produto_quantidade.grid(row=3, column=1, padx=5, pady=5)

        # SOBRE A SAIDA
        Label(self.telaAdm, text="Saida do estoque", width=15, bg='#BDBDBD').grid(row=0, column=5, columnspan=2, padx=5,
                                                                                 pady=5)

        # BOTÃO PARA VER OS GRÁFICOS
        Button(self.telaAdm, text='Gráfico preço', width=15, bg='#B0E0E6', command = self.grafico_preco).grid(row=4, column=5, padx=5, pady=5)
        Button(self.telaAdm, text='Gráfico unidade', width=15, bg='#B0E0E6', command = self.grafico_quantidade).grid(row=4, column=6, padx=5, pady=5)
        Button(self.telaAdm, text='Gráfico total', width=15, bg='#B0E0E6', command = self.grafico_total).grid(row=5, column=5, columnspan = 2,padx=5, pady=5)


        # INSERIR O ID DO PRODUTO QUE SAIU
        Label(self.telaAdm, text="ID_produto", width=20, bg='#BDBDBD').grid(row=1, column=5, padx=5, pady=5)
        self.id_produto_saida = Entry(self.telaAdm)
        self.id_produto_saida.grid(row=1, column=6, padx=5, pady=5)

        # INSERIR A QUANTIDADE DO PRODUTO QUE SAIU
        Label(self.telaAdm, text="Quantidade", width=20, bg='#BDBDBD').grid(row=2, column=5, padx=5, pady=5)
        self.quantidade_produto_saida = Entry(self.telaAdm)
        self.quantidade_produto_saida.grid(row=2, column=6, padx=5, pady=5)

        # BOTÃO PARA CADASTRAR A SAIDA DOS PRODUTOS
        Button(self.telaAdm, text='Confirmar', width=15, bg='#088A08',
               command = self.delete_inteligente).grid(row=3, column=6, padx=5, pady=5)

        # BOTÃO PARA CHECAR A SAIDA DOS PRODUTOS
        Button(self.telaAdm, text='Checar saidas', width=15, bg='#FFB6C1',
               command = self.saidas_registro).grid(row=3, column=5, padx=5, pady=5)

        # BOTÃO PARA CADASTRAR
        Button(self.telaAdm, text='Cadastrar', width=15, bg='#088A08', command = self.cadastrar_produtos).grid(row=4, column=0, padx=5, pady=5)

        # BOTÃO PARA DELETAR PRODUTO
        Button(self.telaAdm, text='Deletar produto', width=15, bg='#DF0101', command = self.deletar_produtos).grid(row=4, column=1, padx=5, pady=5)

        # BOTÃO PARA ATUALIZAR
        Button(self.telaAdm, text='Atualizar', width=15, bg='#DF7401', command = self.att).grid(row=5, column=1,padx=5, pady=5)

        # BOTÃO PARA VER COMPROMISSOS
        Button(self.telaAdm, text='Ver compromissos', width=15, bg='#F4FA58',
               command = estoque_compromissos.Compromissos).grid(row=5,column=0, padx=5, pady=5)

        self.visualizar_produtos()


    def att(self):
        self.visualizar_produtos_backend()


    def visualizar_produtos(self):
        # VISUALIZAR ALUNOS
        self.tree = ttk.Treeview(self.telaAdm, selectmode='browse', column=("column1", "column2", 'column3', 'column4', 'column5', 'column6'), show='headings')

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


            self.tree.insert('', END, values = ver_produto_estoque, iid=linha['id_produto'], tag='1')

            ver_produto_estoque.clear()


    def cadastrar_produtos(self):
        nome = str(self.produto_nome.get()).strip().upper()
        preco = float(self.produto_preco.get())
        quantidade = int(self.produto_quantidade.get())
        total = preco * quantidade
        data = date.today()

        if len(nome) < 100:
            if len(str(preco)) != 0 and preco > 0:
                if len(str(quantidade)) != 0 and quantidade >= 0:
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
                            cursor.execute(f"INSERT INTO estoque(nome, preco, quantidade, total, data_cadastro) VALUES ('{nome}', '{preco}', '{quantidade}', '{total}','{data}')")
                            conexao.commit()
                            messagebox.showinfo("CADASTRO", "Produto cadastrado com sucesso")

                    except:
                        messagebox.showinfo("ERRO", "Erro na hora de efetuar cadastro")
                else:
                    messagebox.showinfo("ERRO", "O cargo tem mais de 100 caracteres")
            else:
                messagebox.showinfo("ERRO", "A senha tem mais de 100 caracteres")
        else:
            messagebox.showinfo("ERRO", "O login tem mais de 100 caracteres")


    def deletar_produtos(self):
        id_delete = int(self.tree.selection()[0])
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
                cursor.execute(f"DELETE FROM estoque WHERE id_produto = '{id_delete}'")
                conexao.commit()
                messagebox.showinfo("DELETADO", "Mercadoria deletada com sucesso")
        except:
            messagebox.showinfo("ERRO", "Erro na hora de deletar mercadoria")


    def delete_inteligente(self):
        id = int(self.id_produto_saida.get())
        quantidade = int(self.quantidade_produto_saida.get())
        preco = self.produto_preco.get()
        total = 0
        horario = datetime.today()
        data = date.today()
        quantidade_registro = quantidade
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
                cursor.execute(f"UPDATE estoque SET quantidade = '{quantidade}', total = '{total}' WHERE id_produto = '{id}'")
                conexao.commit()
                messagebox.showinfo("DELETADO", "Mercadoria alterada com sucesso")
        except:
            messagebox.showinfo("ERRO", "Erro na hora de deletar mercadoria")

        try:
            with conexao.cursor() as cursor:
                cursor.execute(f"SELECT * FROM estoque")
                resultado = cursor.fetchall()
        except:
            messagebox.showinfo("ERRO", "Erro na hora de efetuar cadastro")

        produto = ''
        for a in range(0, len(resultado)):
            if resultado[a]['id_produto'] == id:
                produto = resultado[a]['nome']
                break


        try:
            with conexao.cursor() as cursor:
                cursor.execute(f"INSERT INTO saidas(data_saida, horario_saida, id_produto, produto,quantidade) VALUES ('{data}', '{horario}', '{id}', '{produto}','{quantidade_registro}')")
                conexao.commit()
        except:
            messagebox.showinfo("ERRO", "Erro na hora de efetuar cadastro")


    def saidas_registro(self):
        self.telaSaidas = Toplevel()
        self.telaSaidas['bg'] = '#191970'
        self.telaSaidas.resizable(False, False)
        self.telaSaidas.title('Visualizar saidas')

        self.tree_saidas = ttk.Treeview(self.telaSaidas, selectmode="browse", column=("column1", "column2", "column3", "column4", "column5"),
                                        show='headings')

        self.tree_saidas.column("column1", width=100, minwidth=500, stretch=NO)
        self.tree_saidas.heading('#1', text='Data saida')

        self.tree_saidas.column("column2", width=100, minwidth=500, stretch=NO)
        self.tree_saidas.heading('#2', text='Horario saida')

        self.tree_saidas.column("column3", width=100, minwidth=500, stretch=NO)
        self.tree_saidas.heading('#3', text='id_produto')

        self.tree_saidas.column("column4", width=100, minwidth=500, stretch=NO)
        self.tree_saidas.heading('#4', text='Produto')

        self.tree_saidas.column("column5", width=80, minwidth=500, stretch=NO)
        self.tree_saidas.heading('#5', text='Quantidade')

        self.tree_saidas.grid(row=0, column=0, padx=10, pady=10)

        self.saidas_registro_backend()

        self.tree_saidas.mainloop()


    def saidas_registro_backend(self):
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
                cursor.execute(f"SELECT * FROM saidas")
                resultado = cursor.fetchall()
        except:
            messagebox.showinfo("ERRO", "Erro na hora de efetuar cadastro")

        self.tree_saidas.delete(*self.tree_saidas.get_children())

        saidas_registro = list()
        for linha in resultado:
            saidas_registro.append(linha['data_saida'])
            saidas_registro.append(linha['horario_saida'])
            saidas_registro.append(linha['id_produto'])
            saidas_registro.append(linha['produto'])
            saidas_registro.append(linha['quantidade'])


            self.tree_saidas.insert('', END, values=saidas_registro, tag='1')

            saidas_registro.clear()


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
        plt.barh(nome, preco, color = 'royalblue')
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
        plt.barh(nome, quantidade, color = 'royalblue')
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
        plt.barh(nome, total, color = 'royalblue')
        plt.title("Potencial de lucro do produto")
        plt.xlabel("Total em $")
        plt.ylabel("Produto")
        plt.show()