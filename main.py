import random 
import os
import math
import threading
import tkinter as tk 
from tkinter import Image, ttk
from tkinter import messagebox
from abc import ABC, abstractmethod # obria a classe filha a criar o meodo mostrar_dados
# ABC transforma a classe abstrata
#  SISTEMA DE SOM

import sys # importa o modulo sys para identificar o sistema (linux....)

_PASTA_SONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "sounds")  # define o caminho da pasta 

def _caminho_som(arquivo): # monta o caminho
    return os.path.join(_PASTA_SONS, arquivo)

def tocar_som(arquivo: str): # responsavel por tocar um som
    """Toca um arquivo .wav em thread separada. Ex: tocar_som('click.wav')"""
    def _play():# executa a reproduçao do audio 
        try:
            caminho = _caminho_som(arquivo) 
            if not os.path.isfile(caminho): # se n exisiter encerra a funçao
                return
            if sys.platform == "win32": # verifica se é windows
                import winsound #importa a biblioteca nativa de sons 
                winsound.PlaySound(caminho, winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                # Linux/Mac fallback com subprocess (aplay / afplay)
                import subprocess 
                player = "afplay" if sys.platform == "darwin" else "aplay"
                subprocess.Popen([player, caminho],
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
        except Exception:
            pass
    threading.Thread(target=_play, daemon=True).start()


# Nomes dos arquivos de som — ajuste se quiser outros nomes
SOM_HOVER  = "hover.wav"
SOM_CLICK  = "click.wav"
SOM_SAIR   = "click.wav"
SOM_VOLTAR = "click.wav"
SOM_SALVAR = "success.wav"
SOM_ERRO   = "error.wav"

#  PALETA DE CORES 

COR_PAREDE       = "#F5E6A0"   # amarelo creme (parede principal)
COR_PAREDE_SOMB  = "#E8D880"   # sombra/rodapé da parede
COR_RODAPE_FAIXA = "#D4A030"   # faixa marrom-dourada acima do chão
COR_QUADRO       = "#3A6B28"   # verde lousa
COR_MOLDURA      = "#6B3A10"   # moldura marrom escuro
COR_MOLDURA_INT  = "#8A5018"   # moldura interna mais clara
COR_RODAPE       = "#C8824A"   # chão laranja-tijolo
COR_TIJOLO       = "#D49050"   # tijolo claro
COR_TIJOLO_BORDA = "#A05828"   # borda tijolo
COR_TITULO       = "#D4A860"   # dourado (texto no quadro)
# Botões arredondados dourado/bege 
COR_BTN_BG       = "#C8903A"   #
COR_BTN_BORDA    = "#8A5810"   
COR_BTN_TEXTO    = "#3A1A00"
COR_BTN_HOVER    = "#E0A848"
COR_BTN_SAIR     = "#8A2020"
COR_BTN_SAIR_BD  = "#501010"
COR_BTN_SAIR_FG  = "#FFAAAA"
COR_BTN_SAIR_HV  = "#AA3030"
COR_VOLTAR_BG    = "#AA3030"
# Mural de recados
COR_MURAL_BG     = "#C89848"
COR_MURAL_CORK   = "#E0B860"

# Fontes
FONTE_PIXEL     = ("Courier", 11, "bold")  
FONTE_TITULO_PX = ("Courier", 18, "bold")
FONTE_BTN       = ("Courier", 10, "bold")
FONTE_LABEL     = ("Courier", 10)

# ─────────────────────────────
#  SISTEMA PADRÃO DE UI
# ─────────────────────────────

LARGURA_TELA = 1000
ALTURA_TELA = 700

PAINEL_BG = COR_PAREDE
PAINEL_BORDA = COR_MOLDURA
PAINEL_TEXTO = COR_MOLDURA

PAINEL_PADX = 20
PAINEL_PADY = 20

#Cria o painel 
def criar_painel(master, titulo=None):
    frame = tk.LabelFrame( 
        master,
        text=f" {titulo} " if titulo else "",
        font=FONTE_PIXEL,
        bg=PAINEL_BG,
        fg=PAINEL_TEXTO,  # cor texto 
        bd=3, # espessura da borda 
        relief=tk.RIDGE, # estilo de borda 
        padx=PAINEL_PADX, # espaçamento interno horizontal
        pady=PAINEL_PADY  # espaçamento interno vertical
    )
    return frame # retorna o painel criado 


def criar_container_duplo(master):
    container = tk.Frame(master, bg=PAINEL_BG)
    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=1)
    container.rowconfigure(0, weight=1)
    return container


def botao_padrao(master, texto, comando):
    return tk.Button(
        master,
        text=texto,
        command=comando,
        font=FONTE_BTN,
        bg=COR_BTN_BG,
        fg=COR_BTN_TEXTO,
        activebackground=COR_BTN_HOVER,
        activeforeground="white",
        relief=tk.FLAT,
        bd=0,
        height=2,
        cursor="hand2"
    )

#  CLASSES DE DOMÍNIO
class Pessoa(ABC):
    def __init__(self, nome):
        self.__nome = nome

    @abstractmethod
    def mostrar_dados(self):
        pass

    def get_nome(self):
        return self.__nome


class Aluno(Pessoa):
    def __init__(self, nome, serie):
        super().__init__(nome)
        self.serie = serie

    def mostrar_dados(self, extra=None):
        base = f"Aluno: {self.get_nome()} | Série: {self.serie}"
        return f"{base} | {extra}" if extra else base


class Professor(Pessoa):
    def __init__(self, nome, matricula):
        super().__init__(nome)
        self.matricula = matricula

    def mostrar_dados(self, extra=None):
        base = f"Professor: {self.get_nome()} | Matrícula: {self.matricula}"
        return f"{base} | {extra}" if extra else base

#  COMPONENTES REUTILIZÁVEIS
def btn_pixel(master, texto, comando, sair=False):
    """Botão estilo pixel art com som 8-bit e hover. Funciona em qualquer widget."""
    bg  = COR_BTN_SAIR    if sair else COR_BTN_BG
    bd  = COR_BTN_SAIR_BD if sair else COR_BTN_BORDA
    fg  = COR_BTN_SAIR_FG if sair else COR_BTN_TEXTO
    hv  = COR_BTN_SAIR_HV if sair else COR_BTN_HOVER
    som = SOM_SAIR         if sair else SOM_CLICK

    outer = tk.Frame(master, bg=bd, padx=3, pady=3)

    def _cmd():
        tocar_som(som)
        outer.after(60, comando)

    btn = tk.Button(
        outer, text=f"<< {texto}",
        font=FONTE_BTN, bg=bg, fg=fg,
        activebackground=hv, activeforeground="#FFFFFF",
        relief=tk.FLAT, bd=0, width=22, height=1,
        cursor="hand2", command=_cmd
    )
    btn.pack()
    btn.bind("<Enter>", lambda e: (btn.config(bg=hv),  tocar_som(SOM_HOVER)))
    btn.bind("<Leave>", lambda e:  btn.config(bg=bg))
    return outer


class BotaoPersonalizado(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            font=FONTE_BTN,
            bg=COR_BTN_BG, fg=COR_BTN_TEXTO,
            relief=tk.FLAT,
            activebackground=COR_BTN_HOVER, activeforeground="white",
            height=1, width=20
        )


class TelaBase(tk.Frame):
    def __init__(self, master, titulo_texto, **kwargs):
        super().__init__(master, bg=COR_PAREDE, **kwargs)
        tk.Label(
            self, text=f"[ {titulo_texto} ]",
            font=FONTE_TITULO_PX,
            bg=COR_PAREDE, fg=COR_TITULO
        ).pack(pady=40) 
        btn_pixel(self, "VOLTAR AO MENU", master.mostrar_menu).pack(pady=10)

#  APLICATIVO 
class Aplicativo(tk.Tk):

    series_predefinidas = [
        "1º Ano", "2º Ano", "3º Ano",
        "4º Ano", "5º Ano", "6º Ano",
        "7º Ano", "8º Ano", "9º Ano",
    ]

    def __init__(self):
        super().__init__()
        self.title("KLASSE")
        self.geometry("1000x700")
        self.configure(bg=COR_PAREDE)
        self.resizable(False, False)
       
        from PIL import Image, ImageTk # para carregar o fundo da sala de aula

        fundo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets",
            "fundo_sala.png"
        )

        img = Image.open(fundo_path)
        img = img.resize((1000, 700), Image.NEAREST)

        self.fundo_img = ImageTk.PhotoImage(img)
        
        

        self.dados_alunos     = []
        self.dados_professores = []
        self.dados_turmas     = []
        self.tela_atual       = None

        self.mostrar_menu()
        
    def criar_fundo(self, tela):
        print("FUNDO:", self.fundo_img)

        canvas = tk.Canvas(
        tela,
        width=1000,
        height=700,
        highlightthickness=0
        )

        canvas.pack(fill="both", expand=True)

        canvas.create_image(
        0,
        0,
        image=self.fundo_img,
        anchor="nw"
    )

        return canvas

    # ── MENU PRINCIPAL ────────────────────────
    def mostrar_menu(self):
        if self.tela_atual:
            self.tela_atual.destroy()

        self.tela_atual = tk.Frame(self, bg=COR_PAREDE)
        self.tela_atual.pack(fill="both", expand=True)

        # janela 1000x700: canvas ocupa 560px de altura, tijolos 140px
        cv = tk.Canvas(
            self.tela_atual,
            width=1000,
            height=700,
            highlightthickness=0
        )
        cv.pack(fill="both", expand=True)

        cv.create_image(
            0,
            0,
            image=self.fundo_img,
            anchor="nw"
        )

        # ── QUADRO-NEGRO CENTRALIZADO ─────────────────────
        mw, mh = 600, 400          # largura e altura do quadro
        mx = (1000 - mw) // 2      # = 260  → centralizado
        my = 70

        # sombra / moldura 3D pixel (3 camadas)
        cv.create_rectangle(mx-12, my-10, mx+mw+12, my+mh+16,
                            fill="#1A0800", outline="")
        cv.create_rectangle(mx-8,  my-6,  mx+mw+8,  my+mh+12,
                            fill=COR_MOLDURA, outline="")
        cv.create_rectangle(mx-4,  my-3,  mx+mw+4,  my+mh+6,
                            fill=COR_MOLDURA_INT, outline="")
        # superfície verde
        from PIL import Image, ImageTk
        quadro_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets",
            "quadro.png"
        )

        img_quadro = Image.open(quadro_path)
        img_quadro = img_quadro.resize((600, 400), Image.NEAREST) # tamanho quadro

        self.quadro_img = ImageTk.PhotoImage(img_quadro)

        cv.create_image(
            mx + mw//2,
            my + mh//2,
            image=self.quadro_img
        )
        # textura de giz
        for gy in range(my+16, my+mh-8, 28):
            for gx in range(mx+8, mx+mw-8, 6):
                if (gx//6 + gy//6) % 5 == 0:
                    cv.create_rectangle(gx, gy, gx+3, gy+1,
                                       fill="#FFFFFF", outline="")

        # ── Logo PNG real (logo_klasse.png) ─────────────────
        cx = mx + mw // 2   # centro horizontal do quadro = 500

        _logo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets", "logo_klasse.png"
        )
        try:
            from PIL import Image as _PILImage, ImageTk as _ImageTk
            _pil = _PILImage.open(_logo_path).convert("RGBA")
            # mantém proporção, encaixa em 260x200 pixels (usa NEAREST para manter look pixel)
            _pil.thumbnail((258, 170), _PILImage.NEAREST) # redimensiona mantendo proporção
            self._logo_img = _ImageTk.PhotoImage(_pil)
            cv.create_image(cx, my + 120, image=self._logo_img, anchor="center")
        except Exception as _e:
            # fallback texto se PIL não estiver disponível
            cv.create_text(cx+3, my+110, text="Klasse",
                           font=("Courier", 28, "bold"), fill="#3A1A00")
            cv.create_text(cx,   my+107, text="Klasse",
                           font=("Courier", 28, "bold"), fill=COR_TITULO)

        # ── Botões: 2×2 grid + Sair central ─────────────────
        pares = [
            ("Turmas", "Turmas cadastradas"),
            ("Sortear Turmas", "Sorteio de Turmas"),
            ("Professores", "Cadastro de Professores"),
            ("Alunos", "Cadastro de Alunos"),
        ]

        col_x = [cx - 150, cx + 150] # colunas à esquerda e direita do centro
        row_y = [my + 210, my + 110]# linhas para os botões, abaixo do logo

        for i, (label, destino) in enumerate(pares):
            b = self._btn_arredondado(cv, label, 
                                      lambda d=destino: self.mudar_tela(d)) #
            cv.create_window(col_x[i % 2], row_y[i // 2], window=b) # posiciona em grid 2x2

        b_sair = self._btn_arredondado(cv, "  Sair  ", self.destroy, sair=True)
        cv.create_window(cx, my + 270, window=b_sair) # centralizado abaixo dos outros botões

        # prateleira do quadro
        shelf_y = my + mh
        cv.create_rectangle(mx-8, shelf_y+6, mx+mw+8, shelf_y+18, # base da prateleira
                            fill=COR_MOLDURA, outline="") # base da prateleira
        for gx, gw in [(mx+14,38),(mx+58,24),(mx+88,16),(mx+112,20)]: # detalhes de madeira pixel
            cv.create_rectangle(gx, shelf_y+8, gx+gw, shelf_y+15, # tábuas da prateleira
                               fill="#F0EBE0", outline="") # tábuas da prateleira

        # ── Rodapé de tijolos ──
        self._desenhar_rodape_tijolos(self.tela_atual)

    def _btn_arredondado(self, master, texto, comando, sair=False):
        """Botão estilo pixel arredondado dourado com som 8-bit."""
        bg  = COR_BTN_SAIR    if sair else COR_BTN_BG
        fg  = COR_BTN_SAIR_FG if sair else COR_BTN_TEXTO
        hv  = COR_BTN_SAIR_HV if sair else COR_BTN_HOVER
        som = SOM_SAIR         if sair else SOM_CLICK

        outer = tk.Frame(master,
                         bg=COR_BTN_SAIR_BD if sair else COR_BTN_BORDA,
                         padx=2, pady=2)

        def _cmd():
            tocar_som(som)
            outer.after(60, comando)

        btn = tk.Button(
            outer, text=texto,
            font=FONTE_BTN, bg=bg, fg=fg,
            activebackground=hv, activeforeground="#FFFFFF",
            relief=tk.FLAT, bd=0,
            padx=18, pady=6,
            cursor="hand2",
            command=_cmd
        )
        btn.pack()
        btn.bind("<Enter>", lambda e: (btn.config(bg=hv), tocar_som(SOM_HOVER)))
        btn.bind("<Leave>", lambda e:  btn.config(bg=bg))
        return outer

    def _desenhar_carteira_pixel(self, canvas):
        """Carteira escolar pixel art fiel ao logo — perspectiva isométrica."""
        # Cada pixel = retângulo 3x3 para escala maior
        def px(x, y, w, h, c):
            canvas.create_rectangle(x, y, x+w, y+h, fill=c, outline="")

        # ── Tampo (perspectiva, borda escura embaixo) ──
        px(20, 30,100, 6,"#C8943A")   # borda frontal escura
        px(16, 22,108,14,"#E8B84E")   # face superior clara
        px(18, 20, 90,10,"#D4A040")   # face superior média
        px(22, 18, 80, 8,"#ECC860")   # brilho topo
        px(26, 16, 68, 6,"#F0D070")   # brilho mais claro
        # cantos arredondados pixel
        px(14, 24,  4, 4,"#C8943A")
        px(122,24,  4, 4,"#C8943A")
        # livro/pasta em cima
        px(34, 14, 62,10,"#A06020")
        px(36, 12, 58, 8,"#C08030")
        px(40, 10, 50, 6,"#D49040")
        px(44,  8, 34, 4,"#B07028")

        # ── Estrutura metálica (barra horizontal) ──
        px(14, 34,112, 5,"#909090")   # barra metal principal
        px(16, 36,108, 2,"#B0B0B0")   # brilho metal
        px(14, 38, 20, 4,"#808080")   # detalhe esquerdo
        px(22, 38,  4, 6,"#707070")
        px(90, 38, 20, 4,"#808080")   # detalhe direito
        px(100,38,  4, 6,"#707070")

        # ── Pernas ──
        # perna frontal esquerda
        px(18, 42, 8,50,"#9A6828")
        px(18, 88,14, 6,"#7A5020")    # pé
        # perna frontal direita
        px(112,42, 8,50,"#9A6828")
        px(108,88,14, 6,"#7A5020")
        # perna traseira esquerda (mais curta — perspectiva)
        px(26, 35, 6,36,"#7A5020")
        # perna traseira direita
        px(106,35, 6,36,"#7A5020")

        # ── Gaveta / detalhes ──
        px(40, 42,60, 2,"#B08040")    # linha gaveta
        px(65, 44, 8, 3,"#D4A040")    # puxador
        px(66, 44, 6, 2,"#F0C060")

    def _desenhar_mural(self, cv, x, y, w, h):
        """Mural de recados pixel art no canvas cv."""
        # moldura
        cv.create_rectangle(x-3,y-3,x+w+3,y+h+3, fill="#8A6018", outline="")
        cv.create_rectangle(x,y,x+w,y+h, fill=COR_MURAL_CORK, outline="")
        # papéis colados
        papeis = [
            (x+3,  y+3,  20,16,"#F5E6A0"),
            (x+3,  y+23, 16,12,"#A8C8F0"),
            (x+24, y+5,  14,10,"#F5E6A0"),
            (x+22, y+20, 14,8, "#F0A0A0"),
            (x+4,  y+38, 18,14,"#F0C080"),
            (x+26, y+34, 14,18,"#C0A0F0"),
        ]
        for px,py,pw,ph,pc in papeis:
            if px+pw < x+w and py+ph < y+h:
                cv.create_rectangle(px,py,px+pw,py+ph,fill=pc,outline="#AAAAAA")
        # tachinhas
        for tx,ty in [(x+3,y+3),(x+3,y+h-4),(x+w-4,y+3),(x+w-4,y+h-4)]:
            cv.create_rectangle(tx,ty,tx+4,ty+4,fill="#E84040",outline="")

    def _desenhar_relogio(self, cv, cx, cy):
        """Relógio em formato de flor estilo pixel."""
        # pétalas (flor dourada)
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            px = cx + int(26 * math.cos(rad))
            py = cy + int(26 * math.sin(rad))
            cv.create_rectangle(px-8, py-8, px+8, py+8,
                               fill="#F0B830", outline="#C08010", width=1)
        # rosto do relógio
        cv.create_oval(cx-18, cy-18, cx+18, cy+18,
                      fill="#FFF8E0", outline="#C08010", width=2)
        # ponteiros (estáticos para simplicidade — sem após-fato em tkinter Canvas)
        import datetime
        now = datetime.datetime.now()
        h_ang = math.radians((now.hour % 12) * 30 + now.minute * 0.5 - 90)
        m_ang = math.radians(now.minute * 6 - 90)
        cv.create_line(cx, cy,
                      cx + int(10 * math.cos(h_ang)),
                      cy + int(10 * math.sin(h_ang)),
                      fill="#3A2800", width=3, capstyle=tk.ROUND)
        cv.create_line(cx, cy,
                      cx + int(14 * math.cos(m_ang)),
                      cy + int(14 * math.sin(m_ang)),
                      fill="#5A4010", width=2, capstyle=tk.ROUND)
        cv.create_oval(cx-3, cy-3, cx+3, cy+3, fill="#3A2800", outline="")

    def _desenhar_rodape_tijolos(self, parent):
        """Desenha a faixa de tijolos no rodapé."""
        altura = 140
        canvas = tk.Canvas(parent, width=1000, height=altura,
                           bg=COR_RODAPE, highlightthickness=0)
        canvas.pack(side="bottom", fill="x")

        lw, lh = 58, 16
        for linha in range(altura // lh + 1):
            y0 = linha * lh
            offset = (lw // 2) if linha % 2 != 0 else 0
            x = -offset
            while x < 1000:
                canvas.create_rectangle(x, y0, x+lw-2, y0+lh-2,
                                       fill=COR_TIJOLO, outline=COR_TIJOLO_BORDA)
                x += lw

    # ── NAVEGAÇÃO ────────────────────────────
    def mudar_tela(self, titulo_nova_tela): 
        if self.tela_atual:
            self.tela_atual.destroy()

        mapa = {
            "Cadastro de Professores": TelaCadastroProfessores,
            "Cadastro de Alunos":      TelaCadastroAlunos,
            "Turmas cadastradas":      TelaTurmas,
            "Sorteio de Turmas":       TelaSorteio,
        }
        cls = mapa.get(titulo_nova_tela)
        self.tela_atual = cls(self) if cls else TelaBase(self, titulo_nova_tela)
        self.tela_atual.pack(fill="both", expand=True)

def mostrar_professores(self):
    self.limpar_tela()

    tela = TelaCadastroProfessores(self)
    tela.pack(fill="both", expand=True)

#  TELA — CADASTRO DE ALUNOS
class TelaCadastroAlunos(tk.Frame): 
    def __init__(self, master):
        super().__init__(master, bg=COR_PAREDE)
        self.master = master
        self.canvas = tk.Canvas(
            self,
            width=1000,
            height=700,
            highlightthickness=0
        )

        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(
            0,
            0,
            image=master.fundo_img,
            anchor="nw"
        )
        titulo = tk.Label(
            self,
            text="Cadastro de Alunos",
            font=FONTE_TITULO_PX,
            bg="#F5E6A0"
        )

        self.canvas.create_window(
            500,
            40,
            window=titulo
        )


        container = criar_container_duplo(self)

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        self.canvas.create_window(
            500,
            320,
            window=container,
            width=900,
            height=500
)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        # Esquerda
        esq = criar_painel(container, "Novo Cadastro")
        esq.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        tk.Label(esq, text="Nome do Aluno:", bg=COR_PAREDE, font=FONTE_LABEL).pack(anchor="w", pady=(10, 2))
        self.txt_nome = tk.Entry(esq, font=FONTE_LABEL, width=35)
        self.txt_nome.pack(fill="x", pady=(0, 15))

        tk.Label(esq, text="Série:", bg=COR_PAREDE, font=FONTE_LABEL).pack(anchor="w", pady=(0, 2))
        self.cb_serie = ttk.Combobox(esq, values=self.master.series_predefinidas, font=FONTE_LABEL, state="readonly")
        self.cb_serie.pack(fill="x", pady=(0, 25))
        self.cb_serie.current(0)

        btn_add = tk.Button(esq, text="Adicionar Aluno", command=self.adicionar_aluno,
                  bg=COR_BTN_BG, fg=COR_BTN_TEXTO, activebackground=COR_BTN_HOVER,
                  activeforeground="white", relief=tk.FLAT, font=FONTE_BTN,
                  height=2, cursor="hand2")
        btn_add.pack(fill="x")
        btn_add.bind("<Enter>", lambda e: (btn_add.config(bg=COR_BTN_HOVER), tocar_som(SOM_HOVER)))
        btn_add.bind("<Leave>", lambda e:  btn_add.config(bg=COR_BTN_BG))
        self.txt_nome.bind("<Return>", lambda e: self.adicionar_aluno())

        # Direita
        dir_ = criar_painel(container, "Alunos Registrados")
        dir_.grid(row=0, column=1, sticky="nsew", padx=(20, 0))

        self.tabela = ttk.Treeview(dir_, columns=("id", "nome", "serie"), show="headings")
        for col, txt, w in [("id","ID",60), ("nome","Nome",250), ("serie","Série",100)]:
            self.tabela.heading(col, text=txt)
            self.tabela.column(col, width=w, minwidth=w)
        self.tabela.pack(fill="both", expand=True)

        for a in self.master.dados_alunos:
            self.tabela.insert("", "end", values=(a["id"], a["nome"], a["serie"]))

        btn_voltar = btn_pixel(
            self,
            "VOLTAR AO MENU",
            master.mostrar_menu,
            sair=True
        )

        self.canvas.create_window(
            500,
            650,
            window=btn_voltar
        )


    def adicionar_aluno(self):
        nome = self.txt_nome.get().strip()
        serie = self.cb_serie.get()
        if nome:
            nid = len(self.master.dados_alunos) + 1
            self.master.dados_alunos.append({"id": nid, "nome": nome, "serie": serie})
            self.tabela.insert("", "end", values=(nid, nome, serie))
            self.txt_nome.delete(0, tk.END)
            tocar_som(SOM_SALVAR)
        else:
            tocar_som(SOM_ERRO)
            messagebox.showwarning("Aviso", "Por favor, digite o nome do aluno.")


#  TELA — CADASTRO DE PROFESSORES
class TelaCadastroProfessores(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.canvas = master.criar_fundo(self)

        

        container_divisao = tk.Frame(
            self,
            bg="#F5E6A0"
        )
        titulo = tk.Label(
            self,
            text="Cadastro de Professores",
            font=FONTE_TITULO_PX,
            bg="#F5E6A0"
        )

        self.canvas.create_window(
            500,
            50,
            window=titulo
        )
        self.canvas.create_window(
            500,
            330,
            window=container_divisao,
            width=900,
            height=500
        )

        container_divisao.columnconfigure(0, weight=1) # para dividir o espaço igualmente entre os dois lados
        container_divisao.columnconfigure(1, weight=1) # para dividir o espaço igualmente entre os dois lados
        container_divisao.rowconfigure(0, weight=1)

        #LADO ESQUERDO
        lado_esquerdo = tk.LabelFrame(container_divisao, text="Cadastro                ", font=FONTE_PIXEL, bg="#F5E6A0", padx=2, pady=2) #
        lado_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 20)) 

        tk.Label(lado_esquerdo, text="Nome completo:", bg="#F5E6A0", font=FONTE_LABEL).pack(anchor="w", pady=(5, 1))
        self.txt_nome = tk.Entry(lado_esquerdo, font=FONTE_LABEL, width=20)
        self.txt_nome.pack(fill="x", pady=(0, 8))

        tk.Label(lado_esquerdo, text="Matrícula:", bg="#F5E6A0", font=FONTE_LABEL).pack(anchor="w", pady=(10, 2))
        self.txt_matricula = tk.Entry(lado_esquerdo, font=FONTE_LABEL, width=20) # 👉 CORREÇÃO: Nome corrigido
        self.txt_matricula.pack(fill="x", pady=(0, 15))

        tk.Label(lado_esquerdo, text="E-mail:", bg="#F5E6A0", font=FONTE_LABEL).pack(anchor="w", pady=(10, 2))
        self.txt_email = tk.Entry(lado_esquerdo, font=FONTE_LABEL, width=20)
        self.txt_email.pack(fill="x", pady=(0, 15))

        btn_salvar = tk.Button(lado_esquerdo, text="Adicionar Professor", command=self.adicionar_professor, bg="#B06C4B", fg="white", relief=tk.FLAT, font=("Segoe UI", 11, "bold"), height=2)
        btn_salvar.pack(fill="x")

        #LADO DIREITO
        lado_direito = tk.LabelFrame(container_divisao, text="Professores cadastrados ", font=FONTE_PIXEL, bg="#F5E6A0", padx=20, pady=20)
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
            self.tabela.insert("", "end", values=(professor["id"], professor["nome"], professor["matricula"], professor["email"]))

        btn_voltar = tk.Button(self, text="<< Voltar ao Menu Principal", font=("Segoe UI", 11), command=master.mostrar_menu, bg="#AA3030", fg="white", relief=tk.FLAT, width=25, height=1)
        self.canvas.create_window(
            500,
            650,
            window=btn_voltar
        )

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

#  TELA — SORTEIO (estilo sala de aula pixel art)
class TelaSorteio(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COR_PAREDE)
        self.master = master
        self._animando = False

        # ── Canvas principal (parede) ──
        self.cv = tk.Canvas(self, width=1000, height=900, # altura do canvas é 560 para deixar espaço para rodapé de tijolos
                            bg=COR_PAREDE, highlightthickness=0)
        self.cv.pack(fill="x")
        from PIL import Image, ImageTk

        fundo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets",
            "fundo_sala.png"
        )

        img = Image.open(fundo_path) # carrega a imagem do fundo da sala de aula
        img = img.resize((1000, 700), Image.NEAREST) # redimensiona mantendo proporção

        self.fundo_sorteio = ImageTk.PhotoImage(img)

        self.cv.create_image( # fundo da sala de aula
            0,  # x
            0,  # y
            image=self.fundo_sorteio,
            anchor="nw"
        )

        # título no topo
        self.cv.create_text(500, 28, text="[ Sorteio de Turmas ]",
                            font=FONTE_TITULO_PX, fill=COR_TITULO)

        # ─ PAINEL DE CONFIGURAÇÃO (esquerda) 
        self._montar_painel_config()

        #  QUADRO-NEGRO com resultado (centro-direita) 
        self._montar_quadro_resultado()
        

        #  Botão Sortear e Voltar 
        def _sortear():
            tocar_som(SOM_CLICK)
            self.after(80, self._iniciar_animacao)

        def _voltar():
            tocar_som(SOM_VOLTAR)
            self.after(60, master.mostrar_menu)

        btn_sortear = tk.Button(
            self.cv,
            text=">> SORTEAR <<",
            font=FONTE_BTN,
            bg=COR_BTN_BG, fg=COR_BTN_TEXTO,
            activebackground=COR_BTN_HOVER, activeforeground="#FFFFFF",
            relief=tk.FLAT, bd=0, padx=16, pady=6,
            cursor="hand2",
            command=_sortear
        )
        btn_sortear.bind("<Enter>", lambda e: (btn_sortear.config(bg=COR_BTN_HOVER), tocar_som(SOM_HOVER)))
        btn_sortear.bind("<Leave>", lambda e:  btn_sortear.config(bg=COR_BTN_BG))
        self.cv.create_window(200, 470, window=btn_sortear)

        voltar = tk.Button(
            self.cv,
            text="<< Voltar",
            font=FONTE_BTN,
            bg=COR_BTN_SAIR, fg=COR_BTN_SAIR_FG,
            activebackground=COR_BTN_SAIR_HV, activeforeground="#FFFFFF",
            relief=tk.FLAT, bd=0, padx=12, pady=6,
            cursor="hand2",
            command=_voltar
        )
        voltar.bind("<Enter>", lambda e: (voltar.config(bg=COR_BTN_SAIR_HV), tocar_som(SOM_HOVER)))
        voltar.bind("<Leave>", lambda e:  voltar.config(bg=COR_BTN_SAIR))
        self.cv.create_window(90, 470, window=voltar)

    #  Painel de configuração 
    def _montar_painel_config(self):
        cv = self.cv
        px, py, pw, ph = 20, 55, 340, 400

        # moldura madeira
        cv.create_rectangle(px-6, py-6, px+pw+6, py+ph+6,
                            fill="#3A1A00", outline="")
        cv.create_rectangle(px-3, py-3, px+pw+3, py+ph+3,
                            fill=COR_MOLDURA, outline="")
        cv.create_rectangle(px, py, px+pw, py+ph,
                            fill="#F0E0C0", outline="")

        cv.create_text(px+pw//2, py+18,
                       text="Configurar Sorteio",
                       font=FONTE_PIXEL, fill=COR_MOLDURA)
        cv.create_line(px+10, py+32, px+pw-10, py+32,
                      fill=COR_MOLDURA, width=2)

        #  Série 
        cv.create_text(px+14, py+52, text="Série:", font=FONTE_LABEL,
                       fill="#3A1A00", anchor="w")
        self.cb_serie = ttk.Combobox(
            cv, values=self.master.series_predefinidas,
            state="readonly", width=12, font=FONTE_LABEL
        )
        self.cb_serie.current(0)
        cv.create_window(px+180, py+52, window=self.cb_serie)

        #  Qtd turmas 
        cv.create_text(px+14, py+90, text="Nº de turmas:",
                       font=FONTE_LABEL, fill="#3A1A00", anchor="w")
        self.spin_turmas = tk.Spinbox(
            cv, from_=1, to=10, width=4,
            font=FONTE_LABEL, justify="center"
        )
        self.spin_turmas.delete(0, "end")
        self.spin_turmas.insert(0, "2")
        cv.create_window(px+260, py+90, window=self.spin_turmas)

        #  Lista professores
        cv.create_text(px+14, py+128, text="Professores:",
                       font=FONTE_LABEL, fill="#3A1A00", anchor="w")

        frame_lb = tk.Frame(cv, bg="#F0E0C0")
        self.lb_prof = tk.Listbox(
            frame_lb, selectmode="multiple",
            height=6, width=28, font=FONTE_LABEL,
            bg="#FFFDF0", fg="#3A1A00",
            selectbackground=COR_BTN_BG, selectforeground=COR_BTN_TEXTO,
            relief=tk.FLAT, bd=1
        )
        sb = tk.Scrollbar(frame_lb, orient="vertical",
                          command=self.lb_prof.yview)
        self.lb_prof.config(yscrollcommand=sb.set)
        self.lb_prof.pack(side="left")
        sb.pack(side="right", fill="y")

        nomes = [p["nome"] for p in self.master.dados_professores]
        if not nomes:
            self.lb_prof.insert(tk.END, "(nenhum cadastrado)")
            self.lb_prof.config(state="disabled")
        else:
            for n in nomes:
                self.lb_prof.insert(tk.END, n)

        cv.create_window(px+pw//2, py+230, window=frame_lb)

        #  Animação: nome rolando 
        cv.create_text(px+14, py+316, text="Sorteando...",
                       font=FONTE_LABEL, fill="#7A5A30", anchor="w")
        self.lbl_anim = cv.create_text(
            px+pw//2, py+346,
            text="", font=("Courier", 13, "bold"),
            fill=COR_QUADRO
        )

    #  Quadro de resultado 
    def _montar_quadro_resultado(self):
        cv = self.cv
        mx, my, mw, mh = 380, 55, 590, 400

        # moldura externa
        cv.create_rectangle(mx-8, my-8, mx+mw+8, my+mh+8,
                            fill="#3A1A00", outline="")
        cv.create_rectangle(mx-4, my-4, mx+mw+4, my+mh+4,
                            fill=COR_MOLDURA, outline="")
        cv.create_rectangle(mx-1, my-1, mx+mw+1, my+mh+1,
                            fill=COR_MOLDURA_INT, outline="")
        # quadro verde
        cv.create_rectangle(mx, my, mx+mw, my+mh,
                            fill=COR_QUADRO, outline="")

        # linhas de giz decorativas
        for y in range(my+20, my+mh, 28):
            for x in range(mx+6, mx+mw-6, 5):
                if (x//5 + y//5) % 5 == 0:
                    cv.create_rectangle(x, y, x+3, y+1,
                                       fill="#FFFFFF", outline="")

        # título no quadro
        cv.create_text(mx+mw//2, my+18,
                       text="Resultado",
                       font=FONTE_PIXEL, fill="#C8F0C8")
        cv.create_line(mx+10, my+32, mx+mw-10, my+32,
                      fill="#4A8A58", width=1)

        # prateleira
        cv.create_rectangle(mx-4, my+mh, mx+mw+4, my+mh+14,
                            fill=COR_MOLDURA, outline="")
        for gx, gw in [(mx+10,30),(mx+46,18),(mx+70,12)]:
            cv.create_rectangle(gx, my+mh+3, gx+gw, my+mh+10,
                               fill="#F0EBE0", outline="")

        # área de texto (widget dentro do canvas)
        self.txt_resultado = tk.Text(
            cv,
            width=52, height=18,
            font=("Courier", 10),
            bg=COR_QUADRO, fg="#C8F0C8",
            insertbackground="#C8F0C8",
            relief=tk.FLAT, bd=0,
            wrap="word",
            state="disabled"
        )
        cv.create_window(mx+mw//2, my+mh//2+20,
                         window=self.txt_resultado)

    #  Animação E sorteio 
    def _iniciar_animacao(self):
        if self._animando:
            return

        serie = self.cb_serie.get()
        try:
            n_turmas = int(self.spin_turmas.get())
            if n_turmas <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Número de turmas inválido.") 
            return

        indices = self.lb_prof.curselection()
        profs = [self.lb_prof.get(i) for i in indices]
        if not profs or "(nenhum cadastrado)" in profs:
            messagebox.showwarning("Aviso", "Selecione ao menos um professor.")
            return

        alunos = [a["nome"] for a in self.master.dados_alunos # filtra os alunos pela série selecionada e pega só os nomes para o sorteio
                  if a["serie"] == serie]
        if not alunos:
            messagebox.showwarning("Aviso", f"Nenhum aluno no {serie}.")
            return

        self._animando = True
        todos = alunos[:]
        random.shuffle(todos)

        # animação de embaralhamento (20 frames)
        self._anim_nomes = todos
        self._anim_profs = profs
        self._anim_ntm   = n_turmas
        self._anim_serie = serie
        self._anim_frame = 0
        self._anim_total = 22
        self._animar_frame()

    def _animar_frame(self): # mostra um nome aleatório e toca um som a cada frame, depois de alguns frames faz o sorteio real
        if self._anim_frame < self._anim_total:
            # mostra nome aleatório na animação
            nome_fake = random.choice(self._anim_nomes)
            self.cv.itemconfig(self.lbl_anim, text=f"> {nome_fake} <") # atualiza o texto do item lbl_anim no canvas para mostrar o nome aleatório
            tocar_som([(random.choice([330,392,440,523]), 0.03)])
            self._anim_frame += 1
            delay = 60 + self._anim_frame * 8   # desacelera
            self.after(delay, self._animar_frame)
        else:
            # sorteio real
            self.cv.itemconfig(self.lbl_anim, text="")
            self._fazer_sorteio()
            self._animando = False
            tocar_som(SOM_CLICK + [(1047, 0.15)])

    def _fazer_sorteio(self): # distribui os alunos sorteados em turmas e exibe o resultado
        alunos = self._anim_nomes[:]
        profs  = self._anim_profs[:]
        random.shuffle(alunos)
        random.shuffle(profs)
        n = self._anim_ntm
        serie = self._anim_serie

        turmas = [[] for _ in range(n)] # cria n listas vazias para as turmas
        for i, a in enumerate(alunos):
            turmas[i % n].append(a)

        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # para nomear as turmas (A, B, C...)
        self.master.dados_turmas.clear()

        linhas = [f"=== {serie.upper()} — {len(alunos)} alunos ===\n\n"]
        for idx, lista in enumerate(turmas):
            nome_turma = f"Turma {letras[idx % 26]}"
            prof = profs[idx % len(profs)]
            self.master.dados_turmas.append({
                "nome": f"Turma {serie} {letras[idx % 26]}",
                "serie": serie, "professor": prof, "alunos": lista
            })
            linhas.append(f"<< {nome_turma}  ({len(lista)} alunos)\n")
            linhas.append(f"   Prof: {prof}\n")
            for a in lista:
                linhas.append(f"   - {a}\n")
            linhas.append("\n")

        self.txt_resultado.config(state="normal") # habilita edição temporariamente para atualizar o texto
        self.txt_resultado.delete("1.0", tk.END)  # limpa o conteúdo anterior
        for l in linhas:
            self.txt_resultado.insert(tk.END, l) # insere cada linha do resultado no widget de texto
        self.txt_resultado.config(state="disabled") # desabilita edição para evitar que o usuário modifique o resultado

    #  Helpers 
    def _mural(self, cv, x, y, w, h): # desenha um mural de recados pixel art
        cv.create_rectangle(x-3,y-3,x+w+3,y+h+3, fill="#8A6018", outline="") # moldura madeira
        cv.create_rectangle(x, y, x+w, y+h, fill=COR_MURAL_CORK, outline="") # fundo cortiça
        for px,py,pw,ph,pc in [ # (posição x, posição y, largura, altura, cor)
            (x+3,y+3,20,14,"#F5E6A0"),(x+3,y+22,14,10,"#A8C8F0"),# papéis colados
            (x+26,y+5,14,10,"#F5E6A0"),(x+24,y+20,14,8,"#F0A0A0"), # papéis colados
            (x+4,y+36,18,14,"#F0C080"),(x+28,y+34,14,16,"#C0A0F0"),
        ]:
            if px+pw < x+w and py+ph < y+h: # só desenha se couber dentro do mural
                cv.create_rectangle(px,py,px+pw,py+ph,# desenha o papel
                                   fill=pc, outline="#AAAAAA") # borda cinza
        for tx,ty in [(x+3,y+3),(x+3,y+h-5),(x+w-5,y+3),(x+w-5,y+h-5)]: # tachinhas vermelhas nos cantos
            cv.create_rectangle(tx,ty,tx+4,ty+4,fill="#E84040",outline="") # tachinha vermelha

    def _rodape(self): # desenha a faixa de tijolos no rodapé
        altura = 90 # altura da faixa de tijolos
        c = tk.Canvas(self, width=1000, height=altura, # canvas separado para não sobrepor o fundo da sala
                      bg=COR_RODAPE, highlightthickness=0) # sem borda
        c.pack(side="bottom", fill="x") # ocupa toda a largura, mas altura fixa
        lw, lh = 10, 10 # largura e altura dos tijolos
        for linha in range(altura // lh + 1): # quantas linhas de tijolos cabem na altura
            y0 = linha * lh # posição vertical da linha
            off = (lw // 2) if linha % 2 != 0 else 0 # alterna o offset para criar o padrão de tijolos
            x = -off # posição horizontal inicial (pode começar negativa  para criar o efeito de tijolos cortados nas bordas)
            while x < 1000: # enquanto não ultrapassar a largura total
                c.create_rectangle(x, y0, x+lw-2, y0+lh-2, # desenha o tijolo (com espaçamento de 2px para a borda)
                                  fill=COR_TIJOLO, outline=COR_TIJOLO_BORDA) # cor de preenchimento e borda
                x += lw # move para a posição do próximo tijolo
# pior parte do codigo

#  TELA — TURMAS
class TelaTurmas(tk.Frame):
    def __init__(self, master): # inicializa a tela de turmas
        super().__init__(master) # chama o construtor da classe pai (tk.Frame) para criar o frame base

        self.master = master

        self.canvas = tk.Canvas(
            self,
            width=1000, # largura do canvas para cobrir toda a tela
            height=700, # altura do canvas para cobrir toda a tela (deixa espaço para rodapé)
            highlightthickness=0 # sem borda para o canvas, para que o fundo da sala seja visível sem interrupções
        )

        self.canvas.pack(fill="both", expand=True) # faz o canvas ocupar toda a área disponível do frame, permitindo que o fundo da sala seja exibido corretamente

        self.canvas.create_image(
            0, # posição x do canto superior esquerdo da imagem (0 para alinhar à esquerda)
            0, # posição y do canto superior esquerdo da imagem (0 para alinhar ao topo)
            image=master.fundo_img, # imagem de fundo da sala de aula, carregada no construtor do aplicativo
            anchor="nw" # ancoragem "nw" (noroeste) para que a imagem seja posicionada a partir do canto superior esquerdo do canvas
        )

        titulo = tk.Label( # título da tela, criado como um widget separado para facilitar a formatação e posicionamento
            self, 
            text="Turmas Cadastradas",
            font=FONTE_TITULO_PX, # fonte personalizada para o título, definida no início do código
            bg="#F5E6A0"
        )


        self.canvas.create_window(
            500, # posição x para centralizar o título horizontalmente (metade da largura do canvas)
            40, # posição y para colocar o título próximo ao topo da tela
            window=titulo
        )
        # QUADRO VERDE
        mx, my, mw, mh = 180, 80, 640, 450

        # moldura externa
        self.canvas.create_rectangle(
            mx-8, my-8,
            mx+mw+8, my+mh+8,
            fill="#3A1A00",
            outline=""
        )

        self.canvas.create_rectangle( # moldura madeira
            mx-4, my-4,
            mx+mw+4, my+mh+4,
            fill=COR_MOLDURA,
            outline=""
        )

        self.canvas.create_rectangle( # moldura interna
            mx-1, my-1,
            mx+mw+1, my+mh+1,
            fill=COR_MOLDURA_INT,
            outline=""
        )

        # quadro verde
        self.canvas.create_rectangle(
            mx, my,
            mx+mw, my+mh,
            fill=COR_QUADRO,
            outline=""
        )

        # efeito giz
        for y in range(my+20, my+mh, 28):
            for x in range(mx+6, mx+mw-6, 5):
                if (x//5 + y//5) % 5 == 0:
                    self.canvas.create_rectangle(
                        x, y,
                        x+3, y+1,
                        fill="#FFFFFF",
                        outline=""
        )
        txt = tk.Text( # widget de texto para exibir as informações das turmas, criado dentro do canvas para que fique posicionado corretamente dentro do quadro verde
            self,
            font=("Courier", 10),
            width=58,
            height=18,
            bg=COR_QUADRO,
            fg="#C8F0C8",
            insertbackground="#C8F0C8",
            relief=tk.FLAT,
            bd=0
        )

        self.canvas.create_window( # posiciona o widget de texto dentro do canvas, centralizado no quadro verde
            500,
            305,
            window=txt
        )

        if not master.dados_turmas: # se a lista de turmas estiver vazia
            txt.insert(tk.END, "Nenhuma turma foi sorteada ainda.") # insere mensagem informando 
        else:
            for t in master.dados_turmas: # para cada turma na lista de turmas do aplicativo, insere as informações da turma no quadro verde
                txt.insert(
                    tk.END,
                    f"{t['nome']}\nProfessor: {t['professor']}\n\nAlunos:\n"
                )

                for a in t["alunos"]: # para cada aluno na lista de alunos da turma, insere o nome do aluno no quadro verde, formatado com um hífen e recuado para criar uma lista visual
                    txt.insert(tk.END, f"  - {a}\n")

                txt.insert(tk.END, "\n" + "-" * 40 + "\n\n")
                
        btn_voltar = btn_pixel( # botão de voltar para o menu principal, criado usando a função btn_pixel para manter o estilo pixel art consistente
            self,
            " Voltar AO MENU ",
            master.mostrar_menu,
            sair=True
        )

        self.canvas.create_window( # posiciona o botão de voltar no rodapé, centralizado horizontalmente
            500,
            650,
            window=btn_voltar
        )
# nao mexer nessa parte pq n sei como q fiz ;/
#  PONTO DE ENTRADA
if __name__ == "__main__": # ponto de entrada do programa, executado quando o script é rodado diretamente
    aluno_teste    = Aluno("Alice", "5º Ano")
    professor_teste = Professor("Antônio", "12345")
    print(aluno_teste.mostrar_dados("Aluno destaque"))
    print(professor_teste.mostrar_dados("Professor homenageado")) # teste de herança e polimorfismo

    app = Aplicativo()
    app.mainloop()


#o klasse é um app em python  com tkinter para gerenciar alunos, prof,e turmas escolares. cadastrando dados, organizando turmas e realizando sorteio de alunos por turmas 

#python: como ling. principal 
#tkinter: para interface grafica 
#pillow: (pil) para carregar imagens 
#winsound: para efeitos sonoros 


#o codigo esta dividido em

#classes de dominio: pessoas do sistema
#componentes reutilizaveis: botoes, cores e estilos
#telas da aplicaçao: cada tela: cada tela é uma classe separada 


#POO

#aluno herda de pessoa entao reutiliza o atributo nome

#mostrar_dados foi sobrescrito mostrando polimorfismo 
#mesma ideiad do professor 


#INTERFACE 

#a tela herda de tk.frame 
#o canvas é usado para desenhar o fundo da sala e posicionar os elementos

#label: textos 
#button: botao
#treeview: tela de professores cadastradas 
#entry: campos de texto


#LOGICA DE CADASTRO 

#o metodo le os valores digitados pelo uuario
#usa strip() para remover espaços eextras
#valida se todos os campos foraam preenchidos 
#armazena o registro na lista dados_professores 

#IMAGENS
#sao carregadas com pillow e exdibida no canvas 

#O CODIGO POSSUI UMA CLASSE ABSTRATA PESSOA (porque tanto Aluno quanto Professor possuem características em comum, como o nome e o método para exibir dados. Em vez de repetir código, coloquei essas características na classe Pessoa), DA QUAL HERDAM ALUNO E PROFESSOR. APLICANDO HERANÇA DE POLIMORFISMO . O SISTEMA É MODULAR 

