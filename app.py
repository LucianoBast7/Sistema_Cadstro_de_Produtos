import sqlite3
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

sys.stdout.reconfigure(encoding='utf-8')

conectar_banco_dados = sqlite3.connect('tabelas.sql')
cursor = conectar_banco_dados.cursor()

# Função para criar tabelas no banco de dados
def criar_tabelas():
    # Criação da tabela de produtos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        quantidade_minima INTEGER NOT NULL,
        descricao TEXT
    )
    """)
    
    # Criação da tabela de usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_usuario TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        perfil TEXT NOT NULL
    )
    """)
    
    # Salva as mudanças no banco de dados
    conectar_banco_dados.commit()

# Chama a função para criar as tabelas ao iniciar o programa
criar_tabelas()

# Funções de manipulação de banco de dados
def inserir_produto(nome, quantidade, quantidade_minima, descricao):
    cursor.execute("""
    INSERT INTO produtos (nome, quantidade, quantidade_minima, descricao)
    VALUES (?, ?, ?, ?)""", (nome, quantidade, quantidade_minima, descricao))
    conectar_banco_dados.commit()

def atualizar_quantidade(id_produto, nova_quantidade):
    cursor.execute("""
    UPDATE produtos
    SET quantidade = ?
    WHERE id_produto = ?""", (nova_quantidade, id_produto))
    conectar_banco_dados.commit()

def buscar_todos_produtos():
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    return produtos

def buscar_produtos_abaixo_minimo():
    cursor.execute("SELECT * FROM produtos WHERE quantidade < quantidade_minima")
    produtos = cursor.fetchall()
    return produtos

def inserir_usuario(nome_usuario, senha, perfil):
    cursor.execute("""
    INSERT INTO usuarios (nome_usuario, senha, perfil)
    VALUES (?, ?, ?)""", (nome_usuario, senha, perfil))
    conectar_banco_dados.commit()

def validar_login(nome_usuario, senha, janela_login):
    cursor.execute("""
    SELECT * FROM usuarios WHERE nome_usuario = ? AND senha = ?""", (nome_usuario, senha))
    usuario = cursor.fetchone()

    if usuario:
        messagebox.showinfo("Sucesso", "Login bem-sucedido!")
        janela_login.destroy()
        janela_principal(usuario[3])  # Passa o perfil do usuário para a tela principal
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")

# Interface Gráfica
def janela_login():
    login = tk.Tk()
    login.title("Login")
    login.geometry("300x200")

    tk.Label(login, text="Usuário:").pack(pady=5)
    entry_usuario = tk.Entry(login)
    entry_usuario.pack(pady=5)

    tk.Label(login, text="Senha").pack(pady=5)
    entry_senha = tk.Entry(login, show="*")
    entry_senha.pack(pady=5)

    botao_entrar = tk.Button(login, text="Entrar", command=lambda: validar_login(entry_usuario.get(), entry_senha.get(), login))
    botao_entrar.pack(pady=10)

    login.mainloop()

def salvar_produto(entry_nome, entry_quantidade, entry_quantidade_minima, entry_descricao):
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()
    quantidade_minima = entry_quantidade_minima.get()
    descricao = entry_descricao.get()

    if not nome or not quantidade or not quantidade_minima or not descricao:
        messagebox.showwarning("Atenção", "Todos os campos são obrigatórios.")
        return

    if not quantidade.isdigit() or not quantidade_minima.isdigit():
        messagebox.showwarning("Atenção", "Quantidade e Quantidade Mínima devem ser números.")
        return

    inserir_produto(nome, int(quantidade), int(quantidade_minima), descricao)
    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

    # Limpa os campos após salvar
    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_quantidade_minima.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)

def janela_cad_produto():
    cadastro = tk.Toplevel()
    cadastro.title("Cadastro de Produto")
    cadastro.geometry("400x300")

    tk.Label(cadastro, text="Nome do Produto:").pack(pady=5)
    entry_nome = tk.Entry(cadastro)
    entry_nome.pack(pady=5)

    tk.Label(cadastro, text="Quantidade:").pack(pady=5)
    entry_quantidade = tk.Entry(cadastro)
    entry_quantidade.pack(pady=5)

    tk.Label(cadastro, text="Quantidade Mínima:").pack(pady=5)
    entry_quantidade_minima = tk.Entry(cadastro)
    entry_quantidade_minima.pack(pady=5)

    tk.Label(cadastro, text="Descrição:").pack(pady=5)
    entry_descricao = tk.Entry(cadastro)
    entry_descricao.pack(pady=5)

    botao_salvar = tk.Button(cadastro, text="Salvar Produto", command=lambda: salvar_produto(entry_nome, entry_quantidade, entry_quantidade_minima, entry_descricao))
    botao_salvar.pack(pady=10)

def visualizar_estoque():
    janela_estoque = tk.Toplevel()
    janela_estoque.title("Estoque")
    janela_estoque.geometry("600x400")

    tk.Label(janela_estoque, text="Produtos em Estoque", font=("Arial", 14)).pack(pady=10)

    frame_tabela = tk.Frame(janela_estoque)
    frame_tabela.pack()

    tabela = ttk.Treeview(frame_tabela, columns=("ID", "Nome", "Quantidade", "Min", "Descrição"), show="headings")

    tabela.heading("ID", text="ID")
    tabela.heading("Nome", text="Nome")
    tabela.heading("Quantidade", text="Quantidade")
    tabela.heading("Min", text="Qtd. Mínima")
    tabela.heading("Descrição", text="Descrição")

    tabela.column("ID", width=50)
    tabela.column("Nome", width=150)
    tabela.column("Quantidade", width=100)
    tabela.column("Min", width=100)
    tabela.column("Descrição", width=200)

    tabela.pack(fill="both", expand=True)

    produtos = buscar_todos_produtos()
    for produto in produtos:
        tabela.insert("", "end", values=(produto[0], produto[1], produto[2], produto[3], produto[4]))

# Função para exibir alerta de produtos abaixo do mínimo
def exibir_alerta():
    alerta = tk.Toplevel()
    alerta.title("Alertas de Estoque")
    alerta.geometry("500x300")

    tk.Label(alerta, text="Produtos abaixo da quantidade mínima", font=("Arial", 14), fg="red").pack(pady=10)

    produtos = buscar_produtos_abaixo_minimo()
    for produto in produtos:
        tk.Label(alerta, text=f"ID: {produto[0]}, Nome: {produto[1]}, Quantidade: {produto[2]}").pack()

# Função para cadastro de usuário
def janela_cad_usuario():
    cadastro = tk.Toplevel()
    cadastro.title("Cadastro de Usuário")
    cadastro.geometry("400x300")

    tk.Label(cadastro, text="Nome do Usuário:").pack(pady=5)
    entry_nome = tk.Entry(cadastro)
    entry_nome.pack(pady=5)

    tk.Label(cadastro, text="Senha").pack(pady=5)
    entry_senha = tk.Entry(cadastro, show="*")
    entry_senha.pack(pady=5)

    tk.Label(cadastro, text="Perfil (Administrador/Comum):").pack(pady=5)
    entry_perfil = tk.Entry(cadastro)
    entry_perfil.pack(pady=5)

    botao_salvar = tk.Button(cadastro, text="Cadastrar Usuário", command=lambda: inserir_usuario(entry_nome.get(), entry_senha.get(), entry_perfil.get()))
    botao_salvar.pack(pady=10)

def inserir_usuario(nome_usuario, senha, perfil):
    if not nome_usuario or not senha or not perfil:
        messagebox.showwarning("Atenção", "Todos os campos são obrigatórios.")
        return

    cursor.execute("""
    INSERT INTO usuarios (nome_usuario, senha, perfil)
    VALUES (?, ?, ?)""", (nome_usuario, senha, perfil))
    conectar_banco_dados.commit()
    messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

# Funções para atualizar e excluir produtos
def atualizar_produto_window():
    atualizar = tk.Toplevel()
    atualizar.title("Atualizar Produto")
    atualizar.geometry("400x200")

    tk.Label(atualizar, text="ID do Produto:").pack(pady=5)
    entry_id = tk.Entry(atualizar)
    entry_id.pack(pady=5)

    tk.Label(atualizar, text="Nova Quantidade:").pack(pady=5)
    entry_nova_quantidade = tk.Entry(atualizar)
    entry_nova_quantidade.pack(pady=5)

    botao_atualizar = tk.Button(atualizar, text="Atualizar Quantidade", command=lambda: atualizar_produto(entry_id.get(), entry_nova_quantidade.get(), entry_id, entry_nova_quantidade))
    botao_atualizar.pack(pady=10)

def atualizar_produto(id_produto, nova_quantidade, entry_id, entry_nova_quantidade):
    if not id_produto or not nova_quantidade:
        messagebox.showwarning("Atenção", "Todos os campos são obrigatórios.")
        return

    if not nova_quantidade.isdigit():
        messagebox.showwarning("Atenção", "Nova Quantidade deve ser um número.")
        return

    cursor.execute("SELECT * FROM produtos WHERE id_produto = ?", (id_produto,))
    produto = cursor.fetchone()
    
    if produto:
        atualizar_quantidade(id_produto, int(nova_quantidade))
        messagebox.showinfo("Sucesso", f"Produto ID {id_produto} atualizado com sucesso!")
    else:
        messagebox.showerror("Erro", "Produto não encontrado.")

    # Limpa os campos após a atualização
    entry_id.delete(0, tk.END)
    entry_nova_quantidade.delete(0, tk.END)

def excluir_produto_window():
    excluir = tk.Toplevel()
    excluir.title("Excluir Produto")
    excluir.geometry("300x150")

    tk.Label(excluir, text="ID do Produto:").pack(pady=5)
    entry_id = tk.Entry(excluir)
    entry_id.pack(pady=5)

    botao_excluir = tk.Button(excluir, text="Excluir Produto", command=lambda: excluir_produto(entry_id.get(), entry_id))
    botao_excluir.pack(pady=10)

def excluir_produto(id_produto, entry_id):
    if not id_produto:
        messagebox.showwarning("Atenção", "O campo ID é obrigatório.")
        return

    cursor.execute("SELECT * FROM produtos WHERE id_produto = ?", (id_produto,))
    produto = cursor.fetchone()
    
    if produto:
        cursor.execute("DELETE FROM produtos WHERE id_produto = ?", (id_produto,))
        conectar_banco_dados.commit()
        messagebox.showinfo("Sucesso", f"Produto ID {id_produto} excluído com sucesso!")
    else:
        messagebox.showerror("Erro", "Produto não encontrado.")

    # Limpa o campo após a exclusão
    entry_id.delete(0, tk.END)

# Janela Principal
def janela_principal(perfil):
    root = tk.Tk()
    root.title("Controle de Estoque")
    root.geometry("500x400")

    label_titulo = tk.Label(root, text="Sistema de Controle de Estoque", font=("Arial", 18))
    label_titulo.pack(pady=10)

    botao_cad_produto = tk.Button(root, text="Cadastrar Produto", command=janela_cad_produto)
    botao_cad_produto.pack(pady=10)

    botao_visua_estoque = tk.Button(root, text="Visualizar Estoque", command=visualizar_estoque)
    botao_visua_estoque.pack(pady=10)

    botao_alerta = tk.Button(root, text="Exibir Alertas", command=exibir_alerta)
    botao_alerta.pack(pady=10)

    if perfil == "Administrador":
        botao_cad_usuario = tk.Button(root, text="Cadastrar Usuário", command=janela_cad_usuario)
        botao_cad_usuario.pack(pady=10)

        botao_atualizar_produto = tk.Button(root, text="Atualizar Produto", command=atualizar_produto_window)
        botao_atualizar_produto.pack(pady=10)

        botao_excluir_produto = tk.Button(root, text="Excluir Produto", command=excluir_produto_window)
        botao_excluir_produto.pack(pady=10)

    root.mainloop()

janela_login()
