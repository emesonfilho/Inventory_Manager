from tkinter import *
import pymysql
from tkinter import messagebox
from tkinter import ttk
from datetime import date
from datetime import datetime


class Compromissos():
    def __init__(self):
        self.compromissos = Toplevel()
        self.compromissos['bg'] = '#191970'
        self.compromissos.title('Compromissos')

        # EVENTO QUE VAI ACONTECER
        Label(self.compromissos, text="Evento", width=15, bg='#BDBDBD').grid(row=0, column=0,
                                                                                    padx=5, pady=5)
        self.evento = Entry(self.compromissos)
        self.evento.grid(row=0, column=1, padx=5, pady=5)

        # QUANDO O EVENTO QUE VAI ACONTECER
        Label(self.compromissos, text="Data", width=15, bg='#BDBDBD').grid(row=1, column=0,
                                                                             padx=5, pady=5)
        self.data = Entry(self.compromissos)
        self.data.grid(row=1, column=1, padx=5, pady=5)

        # BOTÃO PARA CADASTRAR
        Button(self.compromissos, text='Cadastrar', width=15, bg='#088A08', command = self.cadastrar_evento).grid(row=2,
                                                                                                             column=0,
                                                                                                             padx=5,
                                                                                                             pady=5)

        # BOTÃO PARA DELETAR PRODUTO
        Button(self.compromissos, text='Deletar', width=15, bg='#DF0101', command = self.deletar_eventos).grid(row=2,
                                                                                                                 column=1,
                                                                                                                 padx=5,
                                                                                                                 pady=5)

        # BOTÃO PARA ATUALIZAR A LISTA DE EVENTOS
        Button(self.compromissos, text='Atualizar', width=15, bg='#088A08', command=self.ver_compromissos_backEnd).grid(row=3,
                                                                                                                column=0,
                                                                                                                columnspan = 2,
                                                                                                                padx=5,
                                                                                                                pady=5)
        self.ver_compromissos()


    def ver_compromissos(self):
        self.compromissos.resizable(False, False)
        self.tree_eventos = ttk.Treeview(self.compromissos, selectmode="browse", column=("column1", "column2", "column3"),
                                         show='headings')

        self.tree_eventos.column("column1", width=40, minwidth=500, stretch=NO)
        self.tree_eventos.heading('#1', text='ID')

        self.tree_eventos.column("column2", width=500, minwidth=500, stretch=NO)
        self.tree_eventos.heading('#2', text='Evento')

        self.tree_eventos.column("column3", width=100, minwidth=500, stretch=NO)
        self.tree_eventos.heading('#3', text='Data')

        self.tree_eventos.grid(row=0, column=3, padx=10, pady=10, columnspan=3, rowspan=10)

        self.ver_compromissos_backEnd()
        self.compromissos.mainloop()


    def ver_compromissos_backEnd(self):
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
                cursor.execute(f"SELECT * FROM compromissos")
                resultado = cursor.fetchall()
        except:
            messagebox.showinfo("ERRO", "Erro na hora de efetuar cadastro")

        self.tree_eventos.delete(*self.tree_eventos.get_children())

        ver_compromissos = list()
        for linha in resultado:
            ver_compromissos.append(linha['id_compromisso'])
            ver_compromissos.append(linha['evento'])
            ver_compromissos.append(linha['data_evento'])


            self.tree_eventos.insert('', END, values= ver_compromissos, iid=linha['id_compromisso'], tag='1')

            ver_compromissos.clear()


    def cadastrar_evento(self):
        evento = str(self.evento.get()).strip().upper()
        data = str(self.data.get()).strip()


        if len(evento) < 1000:
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
                    cursor.execute(f"INSERT INTO compromissos(evento, data_evento) VALUES ('{evento}', '{data}')")
                    conexao.commit()
                    messagebox.showinfo("CADASTRO", "Compromisso cadastrado com sucesso")

            except:
                messagebox.showinfo("ERRO", "Erro na hora de efetuar cadastro")
        else:
            messagebox.showinfo("ERRO", "O evento tem mais de 1000 caracteres")


    def deletar_eventos(self):
        id_delete = int(self.tree_eventos.selection()[0])
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
                cursor.execute(f"DELETE FROM compromissos WHERE id_compromisso = '{id_delete}'")
                conexao.commit()
                messagebox.showinfo("DELETADO", "Compromisso deletada com sucesso")
        except:
            messagebox.showinfo("ERRO", "Erro na hora de deletar Compromisso")

