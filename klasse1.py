import random
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- Classe de Botões ---
class BotaoPersonalizado(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
            relief=tk.GROOVE, activebackground="#1976D2", activeforeground="white",
            height=1, width=20
        )

# --- CLASSE BASE PARA AS TELAS ---
class TelaBase(tk.Frame):
    def __init__(self, master, titulo_texto, **kwargs):
        super().__init__(master, bg="#FFFFFF", **kwargs)
        label = tk.Label(self, text=titulo_texto, font=("Arial", 18, "bold"), bg="#FFFFFF")
        label.pack(pady=40)
        btn_voltar = tk.Button(self, text="← Voltar ao Menu", font=("Arial", 10), 
                               command=master.mostrar_menu, bg="#757575", fg="white", relief=tk.FLAT)
        btn_voltar.pack(pady=10)

# --- CLASSE DA JANELA PRINCIPAL (Centraliza o Banco de Dados) ---
class Aplicativo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador Escolar")
        self.geometry("1000x700") # Ajustado para visualização confortável, mude para 1920x1080 se preferir
        self.configure(bg="#F5F5F5")
        
        # 💾 BANCO DE DADOS TEMPORÁRIO (Acessível por todas as telas)
        self.dados_alunos = [] 
        self.dados_professores = [] # 👉 CORREÇÃO 1: Faltava inicializar esta lista aqui
        self.series_predefinidas = ["1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano"]
        
        self.tela_atual = None
        self.mostrar_menu()

    def mostrar_menu(self):
        if self.tela_atual:
            self.tela_atual.destroy()
            
        self.tela_atual = tk.Frame(self, bg="#F5F5F5")
        self.tela_atual.pack(fill="both", expand=True)
        
        for i in range(5):
            self.tela_atual.rowconfigure(i, weight=1)
        self.tela_atual.columnconfigure(0, weight=1)

        b1 = BotaoPersonalizado(self.tela_atual, text="Sortear Turmas", command=lambda: self.mudar_tela("Sorteio de Turmas"))
        b1.grid(row=0, column=0, sticky="", padx=2, pady=(100, 1))

        b2 = BotaoPersonalizado(self.tela_atual, text="Turmas", command=lambda: self.mudar_tela("Gerenciar Turmas"))
        b2.grid(row=1, column=0, sticky="", padx=2, pady=1)

        b3 = BotaoPersonalizado(self.tela_atual, text="Alunos", command=lambda: self.mudar_tela("Cadastro de Alunos"))
        b3.grid(row=2, column=0, sticky="", padx=2, pady=1)

        b4 = BotaoPersonalizado(self.tela_atual, text="Professores", command=lambda: self.mudar_tela("Cadastro de Professores"))
        b4.grid(row=3, column=0, sticky="", padx=2, pady=1)

        b5 = BotaoPersonalizado(self.tela_atual, text="Sair", command=self.destroy)
        b5.grid(row=4, column=0, sticky="", padx=2, pady=(1, 100))

    def mudar_tela(self, titulo_nova_tela):
        if self.tela_atual:
            self.tela_atual.destroy()
            
        if titulo_nova_tela == "Cadastro de Alunos":
            self.tela_atual = TelaCadastroAlunos(self)
        elif titulo_nova_tela == "Cadastro de Professores":
            self.tela_atual = TelaCadastroProfessores(self)
        elif titulo_nova_tela == "Sorteio de Turmas":
            self.tela_atual = TelaSorteio(self)
        else:
            self.tela_atual = TelaBase(self, titulo_texto=titulo_nova_tela)
            
        self.tela_atual.pack(fill="both", expand=True)

# --- TELA 1: Cadastro de Alunos Dividida ao Meio (Lado a Lado) ---
class TelaCadastroAlunos(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFFFFF")
        self.master = master
        
        # 1. Título Geral no Topo da Tela
        lbl_titulo = tk.Label(self, text="Painel de Cadastro de Alunos", font=("Arial", 18, "bold"), bg="#FFFFFF")
        lbl_titulo.pack(pady=20)

        # Container principal para segurar os dois lados
        container_divisao = tk.Frame(self, bg="#FFFFFF")
        container_divisao.pack(fill="both", expand=True, padx=40)

        # Configura as colunas do container para dividirem o espaço igualmente (50% para cada lado)
        container_divisao.columnconfigure(0, weight=1)
        container_divisao.columnconfigure(1, weight=1)
        container_divisao.rowconfigure(0, weight=1)

        # ==========================================
        # ⬅️ LADO ESQUERDO: Formulário de Cadastro
        # ==========================================
        lado_esquerdo = tk.LabelFrame(container_divisao, text=" Novo Cadastro ", font=("Arial", 12, "bold"), bg="#FFFFFF", padx=20, pady=20)
        lado_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 20)) # Margem apenas na direita para separar as metades

        # Alinhando os elementos verticalmente dentro do formulário
        tk.Label(lado_esquerdo, text="Nome do Aluno:", bg="#FFFFFF", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
        self.txt_nome = tk.Entry(lado_esquerdo, font=("Arial", 11), width=35)
        self.txt_nome.pack(fill="x", pady=(0, 15))

        tk.Label(lado_esquerdo, text="Selecione a Série:", bg="#FFFFFF", font=("Arial", 11)).pack(anchor="w", pady=(0, 2))
        self.cb_serie = ttk.Combobox(lado_esquerdo, values=self.master.series_predefinidas, font=("Arial", 11), state="readonly")
        self.cb_serie.pack(fill="x", pady=(0, 25))
        self.cb_serie.current(0)

        btn_salvar = tk.Button(lado_esquerdo, text="➕ Adicionar Aluno", command=self.adicionar_aluno, bg="#4CAF50", fg="white", relief=tk.FLAT, font=("Arial", 11, "bold"), height=2)
        btn_salvar.pack(fill="x")

        # ==========================================
        # ➡️ LADO DIREITO: Tabela de Alunos Cadastrados
        # ==========================================
        lado_direito = tk.LabelFrame(container_divisao, text=" Alunos Registrados ", font=("Arial", 12, "bold"), bg="#FFFFFF", padx=20, pady=20)
        lado_direito.grid(row=0, column=1, sticky="nsew", padx=(20, 0))

        colunas = ("id", "nome", "serie")
        self.tabela = ttk.Treeview(lado_direito, columns=colunas, show="headings")
        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome do Aluno")
        self.tabela.heading("serie", text="Série")
        
        self.tabela.column("id", width=60, minwidth=60, anchor="center")
        self.tabela.column("nome", width=250, minwidth=150, anchor="w")
        self.tabela.column("serie", width=100, minwidth=100, anchor="center")
        
        # Coloca a tabela preenchendo o lado direito
        self.tabela.pack(fill="both", expand=True)

        # Carrega os alunos que já foram salvos anteriormente
        for aluno in self.master.dados_alunos:
            self.tabela.insert("", "end", values=(aluno["id"], aluno["nome"], aluno["serie"]))

        # ==========================================
        # 🔘 BOTÃO VOLTAR (Fica centralizado no rodapé da página)
        # ==========================================
        btn_voltar = tk.Button(self, text="← Voltar ao Menu Principal", font=("Arial", 11), command=master.mostrar_menu, bg="#757575", fg="white", relief=tk.FLAT, width=25, height=1)
        btn_voltar.pack(pady=25)

    def adicionar_aluno(self):
        nome = self.txt_nome.get().strip()
        serie = self.cb_serie.get()

        if nome:
            novo_id = len(self.master.dados_alunos) + 1
            self.master.dados_alunos.append({"id": novo_id, "nome": nome, "serie": serie})
            self.tabela.insert("", "end", values=(novo_id, nome, serie))
            self.txt_nome.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Por favor, digite o nome do aluno.")

# --- TELA 2: Cadastro de Professores Dividida ao Meio (Lado a Lado) ---
class TelaCadastroProfessores(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFFFFF")
        self.master = master
        
        # 1. Título Geral no Topo da Tela
        lbl_titulo = tk.Label(self, text="Painel de Cadastro de Professores", font=("Arial", 18, "bold"), bg="#FFFFFF")
        lbl_titulo.pack(pady=20)

        # Container principal para segurar os dois lados
        container_divisao = tk.Frame(self, bg="#FFFFFF")
        container_divisao.pack(fill="both", expand=True, padx=40)

        # Configura as colunas do container para dividirem o espaço igualmente (50% para cada lado)
        container_divisao.columnconfigure(0, weight=1)
        container_divisao.columnconfigure(1, weight=1)
        container_divisao.rowconfigure(0, weight=1)

        # ==========================================
        # ⬅️ LADO ESQUERDO: Formulário de Cadastro
        # ==========================================
        lado_esquerdo = tk.LabelFrame(container_divisao, text=" Novo Cadastro de Professor", font=("Arial", 12, "bold"), bg="#FFFFFF", padx=20, pady=20)
        lado_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 20)) 

        # Alinhando os elementos verticalmente dentro do formulário
        tk.Label(lado_esquerdo, text="Nome completo:", bg="#FFFFFF", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
        self.txt_nome = tk.Entry(lado_esquerdo, font=("Arial", 11), width=35)
        self.txt_nome.pack(fill="x", pady=(0, 15))

        tk.Label(lado_esquerdo, text="Matrícula de funcionário:", bg="#FFFFFF", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
        self.txt_matricula = tk.Entry(lado_esquerdo, font=("Arial", 11), width=35) # 👉 CORREÇÃO: Nome corrigido
        self.txt_matricula.pack(fill="x", pady=(0, 15))

        tk.Label(lado_esquerdo, text="E-mail:", bg="#FFFFFF", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
        self.txt_email = tk.Entry(lado_esquerdo, font=("Arial", 11), width=35) # 👉 CORREÇÃO: Nome corrigido
        self.txt_email.pack(fill="x", pady=(0, 15))

        btn_salvar = tk.Button(lado_esquerdo, text="➕ Adicionar Professor", command=self.adicionar_professor, bg="#4CAF50", fg="white", relief=tk.FLAT, font=("Arial", 11, "bold"), height=2)
        btn_salvar.pack(fill="x")

        # ==========================================
        # ➡️ LADO DIREITO: Tabela de Professores Cadastrados
        # ==========================================
        lado_direito = tk.LabelFrame(container_divisao, text=" Professores cadastrados ", font=("Arial", 12, "bold"), bg="#FFFFFF", padx=20, pady=20)
        lado_direito.grid(row=0, column=1, sticky="nsew", padx=(20, 0))

        colunas = ("id", "nome", "matricula", "email")
        self.tabela = ttk.Treeview(lado_direito, columns=colunas, show="headings")
        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome do Professor")
        self.tabela.heading("matricula", text="Matrícula")
        self.tabela.heading("email", text="E-mail")
        
        self.tabela.column("id", width=60, minwidth=60, anchor="center")
        self.tabela.column("nome", width=250, minwidth=150, anchor="w")
        self.tabela.column("matricula", width=100, minwidth=100, anchor="w")
        self.tabela.column("email", width=250, minwidth=150, anchor="center")
        
        self.tabela.pack(fill="both", expand=True)

        # Carrega os professores que já foram salvos anteriormente
        for professor in self.master.dados_professores: # 👉 CORREÇÃO: nome da lista corrigido
            self.tabela.insert("", "end", values=(professor["id"], professor["nome"], professor["matricula"], professor["email"])) # 👉 CORREÇÃO: "professor" com 'r'

        # ==========================================
        # 🔘 BOTÃO VOLTAR
        # ==========================================
        btn_voltar = tk.Button(self, text="← Voltar ao Menu Principal", font=("Arial", 11), command=master.mostrar_menu, bg="#757575", fg="white", relief=tk.FLAT, width=25, height=1)
        btn_voltar.pack(pady=25)

    def adicionar_professor(self):
        # 👉 CORREÇÃO: Buscando os valores corretos dos 3 campos
        nome = self.txt_nome.get().strip()
        matricula = self.txt_matricula.get().strip()
        email = self.txt_email.get().strip()

        if nome and matricula and email:
            novo_id = len(self.master.dados_professores) + 1 # 👉 CORREÇÃO: Nome corrigido da lista global
            
            # Salva na lista global da janela principal
            self.master.dados_professores.append({"id": novo_id, "nome": nome, "matricula": matricula, "email": email})
            
            # Insere visualmente na tabela
            self.tabela.insert("", "end", values=(novo_id, nome, matricula, email))
            
            # Limpa todos os campos para o próximo cadastro
            self.txt_nome.delete(0, tk.END)
            self.txt_matricula.delete(0, tk.END)
            self.txt_email.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos do professor.")


# --- TELA 2: Sorteio Dinâmico sem Repetição com Vários Professores ---
class TelaSorteio(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFFFFF")
        self.master = master

        tk.Label(self, text="Sorteador de Turmas", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=15)

        # Container principal para as configurações (usando grid para organizar os blocos)
        frame_config = tk.Frame(self, bg="#FFFFFF")
        frame_config.pack(pady=10, padx=20, fill="x")
        
        frame_config.columnconfigure(0, weight=1)
        frame_config.columnconfigure(1, weight=1)
        frame_config.columnconfigure(2, weight=1)

        # 1️⃣ BLOCO DA SÉRIE (Coluna 0)
        bloco_serie = tk.Frame(frame_config, bg="#FFFFFF")
        bloco_serie.grid(row=0, column=0, sticky="n", padx=10)
        
        tk.Label(bloco_serie, text="1. Escolha a Série:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(anchor="w", pady=2)
        self.cb_serie_sorteio = ttk.Combobox(bloco_serie, values=self.master.series_predefinidas, state="readonly", width=15)
        self.cb_serie_sorteio.pack(fill="x", pady=5)
        self.cb_serie_sorteio.current(0)

        # 2️⃣ BLOCO DA QUANTIDADE DE TURMAS (Abaixo do bloco da série)
        tk.Label(bloco_serie, text="2. Dividir em quantas turmas?", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(anchor="w", pady=(15, 2))
        self.txt_qtd_turmas = tk.Entry(bloco_serie, width=5, font=("Arial", 10))
        self.txt_qtd_turmas.insert(0, "2") 
        self.txt_qtd_turmas.pack(anchor="w", pady=5)

        # 3️⃣ BLOCO DOS PROFESSORES (Coluna 1)
        bloco_prof = tk.Frame(frame_config, bg="#FFFFFF")
        bloco_prof.grid(row=0, column=1, sticky="n", padx=10)
        
        tk.Label(bloco_prof, text="3. Selecione os Professores (Ctrl+Clique):", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(anchor="w", pady=2)
        
        # selectmode="multiple" permite escolher vários professores
        self.listbox_professores = tk.Listbox(bloco_prof, selectmode="multiple", height=5, width=30, font=("Arial", 10))
        self.listbox_professores.pack(side="left", fill="both", expand=True)
        
        # Barra de rolagem para a lista de professores se houverem muitos
        scrollbar = tk.Scrollbar(bloco_prof, orient="vertical", command=self.listbox_professores.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox_professores.config(yscrollcommand=scrollbar.set)

        # Carrega os professores cadastrados na Listbox
        nomes_professores = [prof["nome"] for prof in self.master.dados_professores]
        if not nomes_professores:
            self.listbox_professores.insert(tk.END, "Nenhum professor cadastrado")
            self.listbox_professores.config(state="disabled") 
        else:
            for nome in nomes_professores:
                self.listbox_professores.insert(tk.END, nome)

        # 4️⃣ BLOCO DO BOTÃO (Coluna 2)
        bloco_botao = tk.Frame(frame_config, bg="#FFFFFF")
        bloco_botao.grid(row=0, column=2, padx=10)
        
        # 👉 CORREÇÃO: Trocado 'padding=10' por 'padx=10, pady=5' para aceitar propriedades padrão do tk.Button
        btn_sortear = tk.Button(bloco_botao, text="🎲 Realizar Sorteio", command=self.realizar_sorteio, bg="#FF9800", fg="white", relief=tk.FLAT, font=("Arial", 11, "bold"), padx=10, pady=5)
        btn_sortear.pack()

        # Caixa de texto grande para exibir o resultado do sorteio
        self.txt_resultado = tk.Text(self, width=60, height=15, font=("Arial", 11), relief=tk.SOLID, borderwidth=1)
        self.txt_resultado.pack(pady=15, padx=20, fill="both", expand=True)

        btn_voltar = tk.Button(self, text="← Voltar ao Menu", font=("Arial", 10), command=master.mostrar_menu, bg="#757575", fg="white", relief=tk.FLAT)
        btn_voltar.pack(pady=10)

    def realizar_sorteio(self):
        serie_alvo = self.cb_serie_sorteio.get()
        
        try:
            num_turmas = int(self.txt_qtd_turmas.get())
        except ValueError:
            messagebox.showerror("Erro", "Insira um número válido de turmas.")
            return

        indices_selecionados = self.listbox_professores.curselection()
        professores_selecionados = [self.listbox_professores.get(i) for i in indices_selecionados]

        if "Nenhum professor cadastrado" in professores_selecionados or not professores_selecionados:
            messagebox.showwarning("Aviso", "Por favor, selecione ao menos um professor para o sorteio.")
            return

        alunos_filtrados = [aluno["nome"] for aluno in self.master.dados_alunos if aluno["serie"] == serie_alvo]

        if not alunos_filtrados:
            messagebox.showwarning("Aviso", f"Não há alunos cadastrados no {serie_alvo}.")
            return
            
        if num_turmas <= 0:
            messagebox.showwarning("Aviso", "O número de turmas deve ser maior que 0.")
            return

        random.shuffle(alunos_filtrados)
        random.shuffle(professores_selecionados)

        turmas_resultado = [[] for _ in range(num_turmas)]

        for i, aluno in enumerate(alunos_filtrados):
            indice_turma = i % num_turmas
            turmas_resultado[indice_turma].append(aluno)

        self.txt_resultado.delete("1.0", tk.END)
        self.txt_resultado.insert(tk.END, f"--- RESULTADO DO SORTEIO DE TURMAS - {serie_alvo.upper()} ---\n")
        self.txt_resultado.insert(tk.END, f"📊 Total de alunos na série: {len(alunos_filtrados)}\n")
        self.txt_resultado.insert(tk.END, "\n" + "="*60 + "\n\n")
        
        letras_turmas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for idx, lista_alunos in enumerate(turmas_resultado):
            nome_turma = f"Turma {letras_turmas[idx % 26]}"
            prof_da_turma = professores_selecionados[idx % len(professores_selecionados)]
            
            self.txt_resultado.insert(tk.END, f"📌 {nome_turma} ({len(lista_alunos)} alunos)\n")
            self.txt_resultado.insert(tk.END, f"👨‍🏫 Professor Regente: {prof_da_turma}\n")
            self.txt_resultado.insert(tk.END, f"  Integrantes:\n")
            
            if not lista_alunos:
                self.txt_resultado.insert(tk.END, "  (Nenhum aluno nesta turma)\n")
            for aluno in lista_alunos:
                self.txt_resultado.insert(tk.END, f"  - {aluno}\n")
            self.txt_resultado.insert(tk.END, "\n" + "-"*40 + "\n\n")


if __name__ == "__main__":
    app = Aplicativo()
    app.mainloop()



'''class BotaoPersonalizado(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            font=("Arial", 12, "bold"),
            bg="#D0AD75",      # Cor de fundo
            fg="#98613C",
            relief=tk.FLAT,
            activebackground="#1976D2",
            activeforeground="white"
        )

# --- Funções para abrir as novas telas ---

def abrir_tela_sorteio():
    # Toplevel cria uma nova janela independente
    tela = tk.Toplevel(janela)
    tela.title("Sorteio de Turmas")
    tela.geometry("400x300")
    
    # Conteúdo da tela
    label = tk.Label(tela, text="Painel de Sorteio", font=("Arial", 16))
    label.pack(pady=50)

def abrir_tela_turmas():
    tela = tk.Toplevel(janela)
    tela.title("Gerenciar Turmas")
    tela.geometry("400x300")
    
    label = tk.Label(tela, text="Lista de Turmas", font=("Arial", 16))
    label.pack(pady=50)

def abrir_tela_alunos():
    tela = tk.Toplevel(janela)
    tela.title("Cadastro de Alunos")
    tela.geometry("1920x1080")
    
    label = tk.Label(tela, text="Painel do Aluno", font=("Arial", 16))
    label.pack(pady=50)

def abrir_tela_professores():
    tela = tk.Toplevel(janela)
    tela.title("Cadastro de Professores")
    tela.geometry("400x300")
    
    label = tk.Label(tela, text="Painel do Professor", font=("Arial", 16))
    label.pack(pady=50)

# --- Configuração da Janela Principal ---
janela = tk.Tk()
janela.title("Gerenciador Escolar")
janela.geometry("500x400")
janela.configure(bg="#F5F5F5")

# Configuração da grade (grid)
janela.rowconfigure(0, weight=1)
janela.rowconfigure(1, weight=1)
janela.columnconfigure(0, weight=1)
janela.columnconfigure(1, weight=1)

# --- Criação dos Botões apontando para as funções ---
b1 = BotaoPersonalizado(janela, text="Sortear Turmas", command=abrir_tela_sorteio)
b1.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

b2 = BotaoPersonalizado(janela, text="Turmas", command=abrir_tela_turmas)
b2.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

b3 = BotaoPersonalizado(janela, text="Alunos", command=abrir_tela_alunos)
b3.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

b4 = BotaoPersonalizado(janela, text="Professores", command=abrir_tela_professores)
b4.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

janela.mainloop()
'''


