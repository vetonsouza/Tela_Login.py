import tkinter as tk
from tkinter import messagebox
import random
import smtplib
import sqlite3

# Função para enviar o código de verificação
def enviar_codigo(email):
    global codigo_gerado
    codigo_gerado = random.randint(100000, 999999)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login("seu_email@gmail.com", "sua_senha")
            servidor.sendmail("seu_email@gmail.com", email, f"Seu código de verificação é: {codigo_gerado}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao enviar o e-mail: {e}")

# Função para verificar login
def verificar_login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()
    email = entrada_email.get()

    if usuario == "admin" and senha == "1234":  # Dados fixos para exemplo
        enviar_codigo(email)
        messagebox.showinfo("Passo 2", "Código de verificação enviado para seu e-mail.")
        verificar_codigo_window()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")

# Função para salvar dados no banco de dados SQLite
def salvar_dados_no_banco(nome, email):
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()

    # Criar tabela caso não exista
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)
    cursor.execute("""
    INSERT INTO usuarios (nome, email)
    VALUES (?, ?)
    """, (nome, email))

    conexao.commit()
    conexao.close()

# Função para validar o código
def verificar_codigo():
    codigo_digitado = int(entrada_codigo.get())
    if codigo_digitado == codigo_gerado:
        nome = entrada_usuario.get()
        email = entrada_email.get()
        salvar_dados_no_banco(nome, email)
        messagebox.showinfo("Sucesso", "Login bem-sucedido e dados salvos!")
    else:
        messagebox.showerror("Erro", "Código de verificação incorreto!")

# Janela para inserção do código
def verificar_codigo_window():
    janela_codigo = tk.Toplevel(janela_principal)
    janela_codigo.title("Verificação em Duas Etapas")

    tk.Label(janela_codigo, text="Digite o código de verificação:").pack()
    global entrada_codigo
    entrada_codigo = tk.Entry(janela_codigo)
    entrada_codigo.pack()

    tk.Button(janela_codigo, text="Validar", command=verificar_codigo).pack()

# Interface gráfica de login
janela_principal = tk.Tk()
janela_principal.title("Tela de Login")

tk.Label(janela_principal, text="Usuário:").pack()
entrada_usuario = tk.Entry(janela_principal)
entrada_usuario.pack()

tk.Label(janela_principal, text="Senha:").pack()
entrada_senha = tk.Entry(janela_principal, show="*")
entrada_senha.pack()

tk.Label(janela_principal, text="E-mail:").pack()
entrada_email = tk.Entry(janela_principal)
entrada_email.pack()

tk.Button(janela_principal, text="Login", command=verificar_login).pack()

janela_principal.mainloop()
