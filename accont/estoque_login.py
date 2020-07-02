from tkinter import *
import pymysql
from tkinter import messagebox
from tkinter import ttk
from datetime import date

from accont import estoque_adm
from accont import estoque_user


class JanelaLogin():
    def __init__(self):
        self.telaLogin = Tk()
        self.telaLogin.title("Login")
        self.telaLogin['bg'] = '#191970'

        #Título da página
        Label(self.telaLogin, text = "Faça o login", width = 10, bg = '#BDBDBD').grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)

        #PARTE REFERENTE AO LOGIN DO USUÁRIO
        Label(self.telaLogin, text = "Usurário", width = 10, bg = '#BDBDBD').grid(row = 1, column = 0, padx = 5, pady = 5)
        self.login = Entry(self.telaLogin)
        self.login.grid(row = 1, column = 1)

        #PARTE REFERENTE A SENHA DO USUÁRIO
        Label(self.telaLogin, text = "Senha", width = 10, bg = '#BDBDBD').grid(row = 2, column = 0, padx = 5, pady = 5)
        self.senha = Entry(self.telaLogin)
        self.senha.grid(row=2, column=1)

        # Criando botão para logar
        Button(self.telaLogin,text = 'Logar' ,width = 8, bg = '#088A08', command = self.logarBackend).grid(row = 9, column = 0, padx = 5, pady = 5)


        #Criando botão para cadastro
        Button(self.telaLogin,text = 'Cadastrar' ,width = 8, bg = '#DF7401', command = self.cadastrarUsuario).grid(row = 9, column = 1, padx = 5, pady = 5)

        self.telaLogin.mainloop()

    def cadastrarUsuario(self):
        # PARTE FRONTEND DE INSERIR NOVOS USUÁRIOS
        Label(self.telaLogin, text="Cargo", width=10, bg='#BDBDBD').grid(row=3, column=0, padx=5, pady=5)

        # ENTRADA DE CARGOS
        self.cargo = Entry(self.telaLogin)
        self.cargo.grid(row=3, column=1)

        # BOTÃO PARA FINALIZAR O CADASTRO
        Button(self.telaLogin, text='Confirmar cadastro', width=15, bg='#AEB404',command=self.cadastroUsuarioBackend).grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        # SOBRE A SEGURANÇA PARA CADASTRO
        Label(self.telaLogin, text="Chave de segurança", width=20, bg='#BDBDBD').grid(row=7, column=0, padx=10, pady=5)
        # ENTRADA DO COD DE SEGURANÇA
        self.cod_seguranca = Entry(self.telaLogin)
        self.cod_seguranca.grid(row=7, column=1, padx=5, pady=5)

        # SOBRE A SEGURANÇA PARA CADASTRO
        Label(self.telaLogin, text="Nível", width=20, bg='#BDBDBD').grid(row=5, column=0, padx=10, pady=5)
        # ENTRADA DO COD DE SEGURANÇA
        self.nivel_funcionario = Entry(self.telaLogin)
        self.nivel_funcionario.grid(row=5, column=1, padx=5, pady=5)


    def logarBackend(self):
        resultado = list()

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
                cursor.execute(f"SELECT * FROM login")
                resultado = cursor.fetchall()
        except:
            messagebox.showinfo("ERRO", "Erro na tentativa de login")

        usuario = self.login.get()
        senha = self.senha.get()
        usuario_master = False
        autenticar = False

        for a in range(0, len(resultado)):
            if resultado[a]['usuario'] == usuario and resultado[a]['senha'] == senha:
                if resultado[a]['nivel'] == 100:
                    usuario_master = True
                elif resultado[a]['nivel'] != 100:
                    usuario_master = False
                autenticar = True
                break
            else:
                autenticar = False
        if autenticar == False:
            messagebox.showinfo('login', 'Email ou senha invalido')
        elif autenticar == True:
            self.telaLogin.destroy()
            if usuario_master == True:
                estoque_adm.JanelaAdm()
            elif usuario_master == False:
                estoque_user.JanelaUser()


    def cadastroUsuarioBackend(self):
        chave_de_seguranca = '88319322'
        usuario = str(self.login.get()).strip()
        senha = str(self.senha.get()).upper().upper().strip()
        cargo = str(self.cargo.get()).upper().upper().strip()
        nivel = int(self.nivel_funcionario.get())

        if self.cod_seguranca.get() == chave_de_seguranca:
            if len(self.login.get()) < 100:
                if len(self.senha.get()) < 30:
                    if len(self.cargo.get()) < 100:
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
                                cursor.execute(
                                    f"INSERT INTO login(usuario, senha, cargo, nivel) VALUES ('{usuario}', '{senha}', '{cargo}', '{nivel}')")
                                conexao.commit()
                                messagebox.showinfo("CADASTRO", "Usuário cadastrado com sucesso")

                        except:
                            messagebox.showinfo("ERRO", "Erro na hora de efetuar cadastro")
                    else:
                        messagebox.showinfo("ERRO", "O cargo tem mais de 100 caracteres")
                else:
                    messagebox.showinfo("ERRO", "A senha tem mais de 100 caracteres")
            else:
                messagebox.showinfo("ERRO", "O login tem mais de 100 caracteres")
        else:
            messagebox.showinfo("ERRO", "Código de segurança invalido")

JanelaLogin()
