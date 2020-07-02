from tkinter import *
import pymysql
from tkinter import messagebox
from tkinter import ttk
from datetime import date

class JanelaLogin():
    def __init__(self):
        self.telaLogin = Tk()
        self.telaLogin.title("Login")
        self.telaLogin['bg'] = '#151515'

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
                db='accont',
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
                JanelaAdm()
            elif usuario_master == False:
                JanelaUser()


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
                                db='accont',
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


class JanelaAdm():
    def __init__(self):
        self.telaAdm = Tk()
        self.telaAdm['bg'] = '#151515'

        # TÍTULO DA JANELA
        Label(self.telaAdm, text="Sobre os alunos", width=15, bg='#BDBDBD').grid(row=0, column=0, columnspan=2, padx=5,pady=5)

        # <<<<<=== SOBRE O CADASTRO DE ALUNOS ===>>>>>

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

        # BOTÃO PARA CADASTRAR
        Button(self.telaAdm, text='Cadastrar', width=15, bg='#088A08', command = self.cadastrar_produtos).grid(row=4, column=0, padx=5, pady=5)

        # BOTÃO PARA DELETAR PRODUTO
        Button(self.telaAdm, text='Deletar produto', width=15, bg='#DF0101', command = self.deletar_produtos).grid(row=4, column=1, padx=5, pady=5)

        # BOTÃO PARA DELETAR FUNCIONÁRIO
        Button(self.telaAdm, text='Deletar venda', width=15, bg='#DF0101').grid(row=5, column=1, padx=5, pady=5)

        # BOTÃO PARA ATUALIZAR
        Button(self.telaAdm, text='Atualizar', width=15, bg='#DF7401', command = self.att).grid(row=5, column=0,padx=5, pady=5)

        # BOTÃO PARA VER COMPROMISSOS
        Button(self.telaAdm, text='Ver compromissos', width=15, bg='#F4FA58').grid(row=6,column=0, columnspan=2, padx=5, pady=5)

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
                db='accont',
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
                            db='accont',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor
                        )
                    except:
                        messagebox.showinfo("ERRO", "Erro na hora de conectar ao banco de dados")
                    try:
                        with conexao.cursor() as cursor:
                            cursor.execute(f"INSERT INTO estoque(nome, preco, quantidade, total,data_cadastro) VALUES ('{nome}', '{preco}', '{quantidade}', '{total}','{data}')")
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
                db='accont',
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


class JanelaUser():
    def __init__(self):
        self.telaUser = Tk()
        self.telaUser['bg'] = '#151515'

        #TÍTULO DA PAG
        Label(self.telaUser, text="Cadastro de alunos", width=20, bg='#BDBDBD').grid(row=0, column=0, columnspan = 2,padx=5, pady=5)

        #ID DO ALUNO
        Label(self.telaUser, text="id_aluno", width=20, bg='#BDBDBD').grid(row=1, column=0, padx=5, pady=5)
        self.id_aluno = Entry(self.telaUser)
        self.id_aluno.grid(row=1, column=1, padx=5, pady=5)

        #TIPO DE PROVA
        Label(self.telaUser, text="Tipo da prova", width=20, bg='#BDBDBD').grid(row=2, column=0, padx=5, pady=5)
        self.tipo_prova = Entry(self.telaUser)
        self.tipo_prova.grid(row=2, column=1, padx=5, pady=5)

        #MATÉRIA DA PROVA
        Label(self.telaUser, text="Matéria da prova", width=20, bg='#BDBDBD').grid(row=3, column=0, padx=5, pady=5)
        self.materia_prova = Entry(self.telaUser)
        self.materia_prova.grid(row=3, column=1, padx=5, pady=5)

        # NOTA DA PROVA
        Label(self.telaUser, text="Nota da prova", width=20, bg='#BDBDBD').grid(row=4, column=0, padx=5, pady=5)
        self.nota_prova = Entry(self.telaUser)
        self.nota_prova.grid(row=4, column=1, padx=5, pady=5)

        # DATA DA PROVA
        Label(self.telaUser, text="Data da prova", width=20, bg='#BDBDBD').grid(row=5, column=0, padx=5, pady=5)
        self.data_prova = Entry(self.telaUser)
        self.data_prova.grid(row=5, column=1, padx=5, pady=5)

        # BOTÃO PARA CADASTRAR OS DADOS
        Button(self.telaUser, text='Cadastrar provas', width=20, bg='#088A08').grid(row=6, column=0, padx=5, pady=5)

        # BOTÃO PARA DELETAR DADOS
        Button(self.telaUser, text='Deletar provas', width=20, bg='#DF0101').grid(row=6, column=1, padx=5, pady=5)

        #BOTÃO PARA VER INFORMAÇÕES SOBRE O ALUNO
        Button(self.telaUser,text = 'Informações provas' ,width = 20, bg = '#DF7401').grid(row = 7, column = 0,padx = 5, pady = 5)


JanelaLogin()

