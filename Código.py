import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, "usuarios.json")

# -----------------------------
# Lista de RAs fixos dos professores
# -----------------------------
ras_professores = ["202590001", "202590002"]

# -----------------------------
# Janela principal (movida para o topo)
# -----------------------------
janela = tk.Tk()
janela.geometry("1000x500")
janela.resizable(False, False)
janela.title("Sistema Acadêmico")

# -----------------------------
# Funções de banco JSON
# -----------------------------


def carregar_dados():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def salvar_dados(dados):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def gerar_ra():
    """Gera um RA para alunos (5 dígitos aleatórios + ano)"""
    ano = datetime.datetime.now().year
    numero = f"{random.randint(0, 99999):05d}"
    return f"{ano}{numero}"


# -----------------------------
# Cadastro de aluno
# -----------------------------
def validar_cadastro(nome, email, senha):
    dados = carregar_dados()
    for usuario in dados:
        if usuario["email"] == email:
            return "Erro: E-mail já cadastrado."

    ra = gerar_ra()
    novo_usuario = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "ra": ra
    }
    dados.append(novo_usuario)
    salvar_dados(dados)
    return f"Cadastro realizado com sucesso!\nSeu RA: {ra}"

# -----------------------------
# Login
# -----------------------------


def validar_login(ra, senha):
    dados = carregar_dados()
    for usuario in dados:
        if usuario["ra"] == ra and usuario["senha"] == senha:
            return True, usuario
    return False, None

# -----------------------------
# Funções das Telas
# -----------------------------


def limpar_janela():
    """Limpa todos os widgets da janela principal."""
    for widget in janela.winfo_children():
        widget.destroy()

# ---
# --- FUNÇÃO MODIFICADA
# ---


def abrir_tela_professor(usuario):
    """Tela para professor registrar nota e faltas"""
    limpar_janela()
    janela.title(f"Área do Professor - {usuario['nome']}")

    tk.Label(janela, text="Lançar Notas/Faltas").pack(pady=10)

    # --- Campo de seleção de matéria (COM AJUSTE DE LARGURA) ---
    tk.Label(janela, text="Escolha a matéria:").pack(pady=(10, 0))
    materias = [
        "Engenharia de software ágil",
        "Programação estruturada em C",
        "Análise e projeto de sistemas",
        "Algoritmo e estrutura de dados python",
    ]

    # Calcula a largura ideal para o combobox de matérias
    try:
        largura_materias = max(len(m) for m in materias)
    except ValueError:
        largura_materias = 30  # Padrão

    combo_materias = ttk.Combobox(janela, values=materias, state="readonly",
                                  width=largura_materias)
    combo_materias.pack(pady=5)
    combo_materias.current(0)

    label_resultado = tk.Label(janela, text="")
    label_resultado.pack(pady=5)

    def mostrar_materia():
        materia_escolhida = combo_materias.get()
        label_resultado.config(
            text=f"Matéria selecionada: {materia_escolhida}")

    tk.Button(janela, text="Confirmar Matéria",
              command=mostrar_materia).pack(pady=5)
    # --- Fim do campo de matéria ---

    # --- CAMPO DE SELEÇÃO DE ALUNO (NOVO) ---
    tk.Label(janela, text="Selecione o Aluno:").pack(pady=(10, 0))

    # Carrega dados para listar alunos
    dados_completos = carregar_dados()

    # Filtra e formata a lista de alunos
    lista_alunos_formatada = []
    for user in dados_completos:
        if user["ra"] not in ras_professores:
            lista_alunos_formatada.append(f"{user['ra']} - {user['nome']}")

    # Calcula a largura ideal para o combobox de alunos
    try:
        # Garante uma largura mínima de 30
        largura_alunos = max(max(len(a) for a in lista_alunos_formatada), 30)
    except ValueError:
        largura_alunos = 30  # Padrão se não houver alunos

    combo_alunos = ttk.Combobox(janela, values=sorted(lista_alunos_formatada),
                                state="readonly", width=largura_alunos)
    combo_alunos.pack(pady=5)

    # --- O 'Entry' de RA foi removido ---

    tk.Label(janela, text="Nota NP1:").pack(pady=(10, 0))
    entry_nota1 = tk.Entry(janela, width=30)
    entry_nota1.pack(pady=5)

    tk.Label(janela, text="Nota NP2:").pack(pady=(10, 0))
    entry_nota2 = tk.Entry(janela, width=30)
    entry_nota2.pack(pady=5)

    tk.Label(janela, text="Faltas:").pack(pady=(10, 0))
    entry_faltas = tk.Entry(janela, width=30)
    entry_faltas.pack(pady=5)

    # --- Função interna de registrar nota/falta (MODIFICADA) ---

    def registrar_nota_falta():
        # Pega o aluno pelo Combobox
        aluno_selecionado_str = combo_alunos.get().strip()

        nota1 = entry_nota1.get().strip()
        nota2 = entry_nota2.get().strip()
        faltas = entry_faltas.get().strip()
        materia = combo_materias.get()

        # Validação
        if not aluno_selecionado_str or not nota1 or not nota2 or not faltas:
            messagebox.showerror(
                "Erro", "Selecione um aluno e preencha todos os campos.")
            return

        # Extrai o RA da string "RA - Nome"
        try:
            ra_aluno = aluno_selecionado_str.split(" - ")[0]
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao processar seleção do aluno: {e}")
            return

        # O resto da lógica de salvar continua igual
        dados = carregar_dados()
        aluno_encontrado = False
        for user in dados:
            if user["ra"] == ra_aluno and user["ra"] not in ras_professores:
                user[f"nota1_{materia}"] = nota1
                user[f"nota2_{materia}"] = nota2
                user[f"faltas_{materia}"] = faltas
                salvar_dados(dados)
                messagebox.showinfo(
                    "Sucesso", f"Notas e faltas atualizadas para {user['nome']}.")
                aluno_encontrado = True

                # Limpa os campos
                combo_alunos.set("")  # Limpa o combobox do aluno
                entry_nota1.delete(0, 'end')
                entry_nota2.delete(0, 'end')
                entry_faltas.delete(0, 'end')
                return

        if not aluno_encontrado:
            messagebox.showerror(
                "Erro", "Aluno não encontrado ou RA inválido.")

    tk.Button(janela, text="Registrar",
              command=registrar_nota_falta).pack(pady=10)
    tk.Button(janela, text="Sair (Logout)",
              command=abrir_tela_login).pack(pady=5)
# ---
# --- FIM DA FUNÇÃO MODIFICADA
# ---


def abrir_tela_aluno(usuario):
    """Tela para aluno ver suas informações"""
    limpar_janela()
    janela.title(f"Área do Aluno - {usuario['nome']}")

    tk.Label(janela, text="Minhas Informações").pack(pady=10)
    tk.Label(janela, text=f"Nome: {usuario['nome']}").pack(pady=5)
    tk.Label(janela, text=f"RA: {usuario['ra']}").pack(pady=5)
    tk.Label(janela, text=f"Curso: Análise e Desenvolvimento de Sistemas").pack(
        pady=5)

    # Criar Treeview para exibir as notas
    colunas = ("Matéria", "NP1", "NP2", "Faltas", "Média", "Situação")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        # ajusta largura e centraliza
        tree.column(col, width=100, anchor="center")

    tree.pack(pady=10, fill="x")

    # Adiciona os dados das matérias
    materias_info = [k.replace("nota1_", "")
                     for k in usuario.keys() if k.startswith("nota1_")]
    if materias_info:
        for mat in materias_info:
            nota1 = usuario.get(f"nota1_{mat}", "0")
            nota2 = usuario.get(f"nota2_{mat}", "0")
            faltas = usuario.get(f"faltas_{mat}", "0")

            try:
                media = (float(nota1) + float(nota2)) / 2
                faltas_int = int(faltas)
                if faltas_int > 15:
                    situacao = "Reprovado (faltas)"
                elif media >= 7:
                    situacao = "Aprovado"
                else:
                    situacao = "Reprovado (nota)"
                media_str = f"{media:.1f}"
            except ValueError:
                media_str = "-"
                situacao = "Dados incompletos"

            tree.insert("", "end", values=(
                mat, nota1, nota2, faltas, media_str, situacao))
    else:
        tree.insert("", "end", values=(
            "Nenhuma nota lançada", "-", "-", "-", "-", "-"))

    tk.Button(janela, text="Sair (Logout)",
              command=abrir_tela_login).pack(pady=15)


def abrir_tela_login():
    """Tela de login RA + senha"""
    limpar_janela()
    janela.title("Sistema Acadêmico - Login")

    tk.Label(janela, text="Login").pack(pady=10)

    tk.Label(janela, text="RA:").pack(pady=(10, 0))
    entry_ra_login = tk.Entry(janela, width=30)
    entry_ra_login.pack(pady=5)

    tk.Label(janela, text="Senha:").pack(pady=(10, 0))
    entry_senha_login = tk.Entry(janela, show="*", width=30)
    entry_senha_login.pack(pady=5)

    def login_usuario():
        ra = entry_ra_login.get().strip()
        senha = entry_senha_login.get().strip()

        sucesso, usuario = validar_login(ra, senha)
        if sucesso:
            if ra in ras_professores:
                abrir_tela_professor(usuario)
            else:
                abrir_tela_aluno(usuario)
        else:
            messagebox.showerror("Erro", "RA ou senha incorretos.")

    tk.Button(janela, text="Entrar", command=login_usuario).pack(pady=15)
    tk.Button(janela, text="Ainda não tenho cadastro",
              command=abrir_tela_cadastro).pack(pady=5)


def abrir_tela_cadastro():
    """Tela de cadastro de aluno"""
    limpar_janela()
    janela.title("Sistema Acadêmico - Cadastro")

    tk.Label(janela, text="Cadastro de Aluno").pack(pady=10)

    tk.Label(janela, text="Nome:").pack(pady=(10, 0))
    entry_nome = tk.Entry(janela, width=30)
    entry_nome.pack(pady=5)

    tk.Label(janela, text="E-mail:").pack(pady=(10, 0))
    entry_email = tk.Entry(janela, width=30)
    entry_email.pack(pady=5)

    tk.Label(janela, text="Senha:").pack(pady=(10, 0))
    entry_senha = tk.Entry(janela, show="*", width=30)
    entry_senha.pack(pady=5)

    def cadastrar_usuario():
        nome = entry_nome.get().strip()
        email = entry_email.get().strip()
        senha = entry_senha.get().strip()

        if not nome or not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        msg = validar_cadastro(nome, email, senha)
        if "sucesso" in msg.lower():
            messagebox.showinfo("Sucesso", msg)
            abrir_tela_login()
        else:
            messagebox.showerror("Erro", msg)

    tk.Button(janela, text="Cadastrar",
              command=cadastrar_usuario).pack(pady=15)
    tk.Button(janela, text="Já tenho conta (Ir para Login)",
              command=abrir_tela_login).pack(pady=5)


# -----------------------------
# Execução
# -----------------------------
abrir_tela_cadastro()
janela.mainloop()
