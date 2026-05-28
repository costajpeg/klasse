import random
import os
import tkinter as tk #biblioteca pra fazer a interface
from tkinter import ttk #biblioteca pra fazer a interface, mas eh "Themed", cheia de modernices
from tkinter import messagebox #para mensagens e alertas
from abc import ABC, abstractmethod #biblioteca abstrata

class Pessoa(ABC): #classe abstrata pois herda ABC
    def __init__(self, nome):
        self.__nome = nome #atributo privado

    @abstractmethod
    def mostrar_dados(self):
        pass

    def get_nome(self):
        return self.__nome #atributo privado

    def __validar_nome(self):  #método privado
        return len(self.__nome) > 0

class Aluno(Pessoa): #classe com herança
    def __init__(self, nome, serie):
        super().__init__(nome)
        self.serie = serie

    def mostrar_dados(self, extra=None): #polimorfismo mesmo metodo parametros diferentes
    #simula sobrecarga usando parametro opcional
        if extra: #verifica se foi passada uma informação "extra"
            return f"Aluno: {self.get_nome()} | Série: {self.serie} | {extra}"
        return f"Aluno: {self.get_nome()} | Série: {self.serie}"
    
class Professor(Pessoa): #classe com herança
    def __init__(self, nome, matricula):
        super().__init__(nome)
        self.matricula = matricula

    def mostrar_dados(self, extra=None): #polimorfismo mesmo metodo parametros diferentes
    #simula sobrecarga usando parametro opcional
        if extra: #verifica se foi passada uma informação "extra"
            return f"Professor: {self.get_nome()} | Matrícula: {self.matricula} | {extra}"
        return f"Professor: {self.get_nome()} | Matrícula: {self.matricula}"

class BotaoPersonalizado(tk.Button): #classe 1
    def __init__(self, master=None, **kwargs): #kwargs keywords arguments recebe argumentos nomeados sem precisar declarar um de cada vez
        super().__init__(master, **kwargs)
        self.config(font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief=tk.GROOVE, activebackground="#1976D2", activeforeground="white", height=1, width=20)

class TelaBase(tk.Frame): #classe 2
#usamos tk.Frame para as telas, pois ele deixa com q agrupamos botoes, tabelas, textos, em uma msm janela
#tk.Frame eh tipo uma "caixinha"/container
    def __init__(self, master, titulo_texto, **kwargs):
        super().__init__(master, bg="#FFFFFF", **kwargs)
        label = tk.Label(self, text=titulo_texto, font=("Arial", 18, "bold"), bg="#FFFFFF")
        label.pack(pady=40)
        btn_voltar = tk.Button(self, text="← Voltar ao Menu", font=("Arial", 10), 
                               command=master.mostrar_menu, bg="#757575", fg="white", relief=tk.FLAT)
        btn_voltar.pack(pady=10)

class Aplicativo(tk.Tk): #classe 3 tk.Tk eh a janela principal
#superclasse
    def __init__(self):
        super().__init__()
        self.title("KLASSE")
        self.geometry("1000x700")
        self.configure(bg="#F5F5F5")
        
        self.dados_alunos = [] 
        self.dados_professores = []
        self.series_predefinidas = ["1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano", "6º Ano", "7º Ano", "8º Ano", "9º Ano"]
        self.dados_turmas = []

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

        b1 = BotaoPersonalizado(self.tela_atual, text="Professores", command=lambda: self.mudar_tela("Cadastro de Professores"))
        b1.grid(row=0, column=0, sticky="", padx=2, pady=(100, 1))

        b2 = BotaoPersonalizado(self.tela_atual, text="Alunos", command=lambda: self.mudar_tela("Cadastro de Alunos"))
        b2.grid(row=1, column=0, sticky="", padx=2, pady=1)

        b3 = BotaoPersonalizado(self.tela_atual, text="Turmas", command=lambda: self.mudar_tela("Turmas cadastradas"))
        b3.grid(row=2, column=0, sticky="", padx=2, pady=1)

        b4 = BotaoPersonalizado(self.tela_atual, text="Sortear Turmas", command=lambda: self.mudar_tela("Sorteio de Turmas"))
        b4.grid(row=3, column=0, sticky="", padx=2, pady=1)

        b5 = BotaoPersonalizado(self.tela_atual, text="Sair", command=self.destroy)
        b5.grid(row=4, column=0, sticky="", padx=2, pady=(1, 100))

    def mudar_tela(self, titulo_nova_tela):
        if self.tela_atual:
            self.tela_atual.destroy()
            
        if titulo_nova_tela == "Cadastro de Professores":
            self.tela_atual = TelaCadastroProfessores(self)
        elif titulo_nova_tela == "Cadastro de Alunos":
            self.tela_atual = TelaCadastroAlunos(self)
        elif titulo_nova_tela == "Turmas cadastradas":
            self.tela_atual = TelaTurmas(self)
        elif titulo_nova_tela == "Sorteio de Turmas":
            self.tela_atual = TelaSorteio(self)
        else:
            self.tela_atual = TelaBase(self, titulo_texto=titulo_nova_tela)
            
        self.tela_atual.pack(fill="both", expand=True)

class TelaCadastroAlunos(tk.Frame):  #classe 4
    def __init__(self, master): #master eh a janela principal
        super().__init__(master, bg="#FFFFFF")
        self.master = master
        
        lbl_titulo = tk.Label(self, text="Painel de Cadastro de Alunos", font=("Arial", 18, "bold"), bg="#FFFFFF")
        lbl_titulo.pack(pady=20)

        container_divisao = tk.Frame(self, bg="#FFFFFF")
        container_divisao.pack(fill="both", expand=True, padx=40)

        container_divisao.columnconfigure(0, weight=1)
        container_divisao.columnconfigure(1, weight=1)
        container_divisao.rowconfigure(0, weight=1)

        #LADO ESQUERDO
        lado_esquerdo = tk.LabelFrame(container_divisao, text=" Novo Cadastro ", font=("Arial", 12, "bold"), bg="#FFFFFF", padx=20, pady=20)
        lado_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 20)) #margem apenas na direita para separar as metades
        #sticky define para qual direçao o componente ficara alinhado (north south east west)
        tk.Label(lado_esquerdo, text="Nome do Aluno:", bg="#FFFFFF", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
        self.txt_nome = tk.Entry(lado_esquerdo, font=("Arial", 11), width=35)
        self.txt_nome.pack(fill="x", pady=(0, 15))

        tk.Label(lado_esquerdo, text="Selecione a Série:", bg="#FFFFFF", font=("Arial", 11)).pack(anchor="w", pady=(0, 2))
        self.cb_serie = ttk.Combobox(lado_esquerdo, values=self.master.series_predefinidas, font=("Arial", 11), state="readonly")
        self.cb_serie.pack(fill="x", pady=(0, 25))
        self.cb_serie.current(0)

        btn_salvar = tk.Button(lado_esquerdo, text="Adicionar Aluno", command=self.adicionar_aluno, bg="#4CAF50", fg="white", relief=tk.FLAT, font=("Arial", 11, "bold"), height=2)
        btn_salvar.pack(fill="x")

        #LADO DIREITO
        lado_direito = tk.LabelFrame(container_divisao, text=" Alunos Registrados ", font=("Arial", 12, "bold"), bg="#FFFFFF", padx=20, pady=20)
        lado_direito.grid(row=0, column=1, sticky="nsew", padx=(20, 0))

        colunas = ("id", "nome", "serie")
        self.tabela = ttk.Treeview(lado_direito, columns=colunas, show="headings") #tabelas
        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome do Aluno")
        self.tabela.heading("serie", text="Série")
        
        self.tabela.column("id", width=60, minwidth=60, anchor="center")
        self.tabela.column("nome", width=250, minwidth=150, anchor="w")
        self.tabela.column("serie", width=100, minwidth=100, anchor="center")
        
        self.tabela.pack(fill="both", expand=True)

        for aluno in self.master.dados_alunos:
            self.tabela.insert("", "end", values=(aluno["id"], aluno["nome"], aluno["serie"]))

        #BOTAO VOLTAR
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

class TelaCadastroProfessores(tk.Frame):  #classe 5
    def __init__(self, master):
        super().__init__(master, bg="#FFFFFF")
        self.master = master
        
        lbl_titulo = tk.Label(self, text="Painel de Cadastro de Professores", font=("Arial", 18, "bold"), bg="#FFFFFF")
        #cria textos
        lbl_titulo.pack(pady=20)

        container_divisao = tk.Frame(self, bg="#FFFFFF") #fazer a divisao de colunas
        container_divisao.pack(fill="both", expand=True, padx=40)

        container_divisao.columnconfigure(0, weight=1)
        container_divisao.columnconfigure(1, weight=1)
        container_divisao.rowconfigure(0, weight=1)

        #LADO ESQUERDO
        lado_esquerdo = tk.LabelFrame(container_divisao, text=" Novo Cadastro de Professor", font=("Arial", 12, "bold"), bg="#FFFFFF", padx=20, pady=20)
        lado_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 20)) 

        tk.Label(lado_esquerdo, text="Nome completo:", bg="#FFFFFF", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
        self.txt_nome = tk.Entry(lado_esquerdo, font=("Arial", 11), width=35)
        self.txt_nome.pack(fill="x", pady=(0, 15))

        tk.Label(lado_esquerdo, text="Matrícula de funcionário:", bg="#FFFFFF", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
        self.txt_matricula = tk.Entry(lado_esquerdo, font=("Arial", 11), width=35) # 👉 CORREÇÃO: Nome corrigido
        self.txt_matricula.pack(fill="x", pady=(0, 15))

        tk.Label(lado_esquerdo, text="E-mail:", bg="#FFFFFF", font=("Arial", 11)).pack(anchor="w", pady=(10, 2))
        self.txt_email = tk.Entry(lado_esquerdo, font=("Arial", 11), width=35)
        self.txt_email.pack(fill="x", pady=(0, 15))

        btn_salvar = tk.Button(lado_esquerdo, text="Adicionar Professor", command=self.adicionar_professor, bg="#4CAF50", fg="white", relief=tk.FLAT, font=("Arial", 11, "bold"), height=2)
        btn_salvar.pack(fill="x")

        #LADO DIREITO
        lado_direito = tk.LabelFrame(container_divisao, text="Professores cadastrados ", font=("Arial", 12, "bold"), bg="#FFFFFF", padx=20, pady=20)
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

        for professor in self.master.dados_professores:
            self.tabela.insert("", "end", values=(professor["id"], professor["nome"], professor["matricula"], professor["email"])) # 👉 CORREÇÃO: "professor" com 'r'

        btn_voltar = tk.Button(self, text="← Voltar ao Menu Principal", font=("Arial", 11), command=master.mostrar_menu, bg="#757575", fg="white", relief=tk.FLAT, width=25, height=1)
        btn_voltar.pack(pady=25)

    def adicionar_professor(self):
        nome = self.txt_nome.get().strip() #get pega o texto digitado e strip remove espaços extras do começo e fim
        matricula = self.txt_matricula.get().strip()
        email = self.txt_email.get().strip()

        if nome and matricula and email:
            novo_id = len(self.master.dados_professores) + 1 
            
            self.master.dados_professores.append({"id": novo_id, "nome": nome, "matricula": matricula, "email": email})
            
            self.tabela.insert("", "end", values=(novo_id, nome, matricula, email))
            

            self.txt_nome.delete(0, tk.END)
            self.txt_matricula.delete(0, tk.END)
            self.txt_email.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos do professor.")

class TelaSorteio(tk.Frame):  #classe 6
    def __init__(self, master):
        super().__init__(master, bg="#FFFFFF")
        self.master = master

        tk.Label(self, text="Sorteador de Turmas", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=15)

        frame_config = tk.Frame(self, bg="#FFFFFF")
        frame_config.pack(pady=10, padx=20, fill="x")
        #pady espaço vertical, padx horizontal e fill eh pro componente de esticar
        frame_config.columnconfigure(0, weight=1) #numero da coluna, o quanto ela pode crescer
        frame_config.columnconfigure(1, weight=1)
        frame_config.columnconfigure(2, weight=1)

        bloco_serie = tk.Frame(frame_config, bg="#FFFFFF")
        bloco_serie.grid(row=0, column=0, sticky="n", padx=10)
        
        tk.Label(bloco_serie, text="1. Escolha a Série:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(anchor="w", pady=2)
        self.cb_serie_sorteio = ttk.Combobox(bloco_serie, values=self.master.series_predefinidas, state="readonly", width=15)
        self.cb_serie_sorteio.pack(fill="x", pady=5)
        self.cb_serie_sorteio.current(0)

        tk.Label(bloco_serie, text="2. Dividir em quantas turmas?", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(anchor="w", pady=(15, 2))
        self.txt_qtd_turmas = tk.Entry(bloco_serie, width=5, font=("Arial", 10))
        self.txt_qtd_turmas.insert(0, "2") 
        self.txt_qtd_turmas.pack(anchor="w", pady=5)

        bloco_prof = tk.Frame(frame_config, bg="#FFFFFF")
        bloco_prof.grid(row=0, column=1, sticky="n", padx=10)
        
        tk.Label(bloco_prof, text="3. Selecione os Professores:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(anchor="w", pady=2)
        
        #listbox criaos selecionaveis
        self.listbox_professores = tk.Listbox(bloco_prof, selectmode="multiple", height=5, width=30, font=("Arial", 10))
        self.listbox_professores.pack(side="left", fill="both", expand=True)
        
        #scrollbar cria a rolagem
        scrollbar = tk.Scrollbar(bloco_prof, orient="vertical", command=self.listbox_professores.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox_professores.config(yscrollcommand=scrollbar.set)

        nomes_professores = [prof["nome"] for prof in self.master.dados_professores]
        if not nomes_professores:
            self.listbox_professores.insert(tk.END, "Nenhum professor cadastrado")
            self.listbox_professores.config(state="disabled") 
        else:
            for nome in nomes_professores:
                self.listbox_professores.insert(tk.END, nome)

        bloco_botao = tk.Frame(frame_config, bg="#FFFFFF")
        bloco_botao.grid(row=0, column=2, padx=10)
        
        btn_sortear = tk.Button(bloco_botao, text="Realizar Sorteio", command=self.realizar_sorteio, bg="#FF9800", fg="white", relief=tk.FLAT, font=("Arial", 11, "bold"), padx=10, pady=5)
        btn_sortear.pack()

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
        self.txt_resultado.insert(tk.END, f"RESULTADO DO SORTEIO DE TURMAS {serie_alvo.upper()}\n")
        self.txt_resultado.insert(tk.END, f"Total de alunos na série: {len(alunos_filtrados)}\n")
        self.txt_resultado.insert(tk.END, "\n" + "="*60 + "\n\n")
        
        letras_turmas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        self.master.dados_turmas.clear()
        for idx, lista_alunos in enumerate(turmas_resultado):
            nome_turma = f"Turma {serie_alvo} {letras_turmas[idx % 26]}"
            prof_da_turma = professores_selecionados[idx % len(professores_selecionados)]
            

            self.txt_resultado.insert(tk.END, f"📌 {nome_turma} ({len(lista_alunos)} alunos)\n")
            self.txt_resultado.insert(tk.END, f"  Professor regente: {prof_da_turma}\n")
            self.txt_resultado.insert(tk.END, f"  Integrantes:\n")
            
            turma = {"nome": nome_turma, "serie": serie_alvo, "professor": prof_da_turma, "alunos": lista_alunos}
            self.master.dados_turmas.append(turma)

            if not lista_alunos:
                self.txt_resultado.insert(tk.END, "  (Nenhum aluno nesta turma)\n")
            for aluno in lista_alunos:
                self.txt_resultado.insert(tk.END, f"  - {aluno}\n")
            self.txt_resultado.insert(tk.END, "\n" + "-"*40 + "\n\n")

class TelaTurmas(tk.Frame):  #classe 7
    def __init__(self, master):
        super().__init__(master, bg="#FFFFFF")
        self.master = master

        tk.Label(self, text= "Turmas", font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=20)

        txt = tk.Text(self, font=("Arial", 11))
        txt.pack(fill="both", expand=True, padx=20, pady=20)
    
        if not master.dados_turmas:
            txt.insert(tk.END, "Nenhuma turma foi sorteada ainda.")

        else:
            for turma in master.dados_turmas:
                txt.insert(tk.END, f"{turma['nome']}\n")
                txt.insert(tk.END, f"Professor: {turma['professor']}\n")
                txt.insert(tk.END, "\nAlunos: \n\n")

                for aluno in turma["alunos"]:
                    txt.insert(tk.END, f" - {aluno}\n")

                txt.insert(tk.END, "\n" + "-"*40 + "\n\n")

        btn_voltar = tk.Button(self, text="← Voltar", command=master.mostrar_menu)
        btn_voltar.pack(pady=10)

if __name__ == "__main__":
    aluno_teste = Aluno("Alice", "5º Ano")
    professor_teste = Professor("Antônio", "12345")

    print(aluno_teste.mostrar_dados("Aluno destaque")) #chamada de método
    print(professor_teste.mostrar_dados("Professor homenageado")) #chamada de método

    app = Aplicativo()
    app.mainloop() #janela aberta e executa a interface
