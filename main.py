import pygame
import sys
import math
from buscaNP import buscaNP
from buscaP import buscaP

class Fantasma:
    def __init__(self, x, y, cor, escala=1):
        self.x = x
        self.y_base = y   # posição original
        self.y = y
        self.cor = cor
        self.escala = escala

        self.tempo = 0    # controla animação

    def update(self):
        self.tempo += 0.01
        self.y = self.y_base + math.sin(self.tempo) * 1  # movimento vertical suave

    def draw(self, tela):
        s = self.escala

        # corpo
        pygame.draw.rect(tela, self.cor, (self.x - 12*s, self.y, 24*s, 14*s))
        pygame.draw.circle(tela, self.cor, (self.x, self.y), 12*s)

        # ondinhas
        pygame.draw.circle(tela, self.cor, (self.x - 8*s, self.y + 14*s), 6*s)
        pygame.draw.circle(tela, self.cor, (self.x + 8*s, self.y + 14*s), 6*s)

        # olhos
        pygame.draw.circle(tela, (255, 255, 255), (self.x - 5*s, self.y), 4*s)
        pygame.draw.circle(tela, (255, 255, 255), (self.x + 5*s, self.y), 4*s)

        # pupilas
        pygame.draw.circle(tela, (0, 0, 0), (self.x - 5*s, self.y), 2*s)
        pygame.draw.circle(tela, (0, 0, 0), (self.x + 5*s, self.y), 2*s)

class PacmanMenu:
    def __init__(self):
        self.x = 80
        self.y = 180
        self.target_x = 80
        self.target_y = 180
        self.boca = 0

    def move_to(self, x, y):
        self.target_x = x
        self.target_y = y

    def update(self):
        # movimento suave em X
        if self.x < self.target_x:
            self.x += 4
        elif self.x > self.target_x:
            self.x -= 4

        # movimento suave em Y
        if self.y < self.target_y:
            self.y += 3
        elif self.y > self.target_y:
            self.y -= 3

        self.boca += 0.50  # animação da boca

    def draw(self, tela):
        # corpo
        pygame.draw.circle(tela, (255, 255, 0), (self.x, self.y), 12)

        # boca (triângulo preto animado)
        abertura = abs(pygame.math.Vector2(1, 0).rotate(self.boca * 1).x)

        pygame.draw.polygon(tela, (0, 0, 0), [
            (self.x, self.y),
            (self.x + 12, self.y - int(10 * abertura)),
            (self.x + 12, self.y + int(10 * abertura))
        ])

        # olho
        pygame.draw.circle(tela, (0, 0, 0), (self.x + 4, self.y - 5), 2)

pygame.init()

pygame.mixer.init()
click_sound = pygame.mixer.Sound("click_arcade.wav")
pygame.mixer.music.load("paclab.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # tocar em loop

# ---------------- MAPA ----------------
def carregar_mapa(arquivo):
    mapa = []
    with open(arquivo) as file:
        for linha in file:
            mapa.append(list(map(int, linha.strip().split(","))))
    return mapa

mapa = carregar_mapa("mapa.txt")

LINHAS = len(mapa)
COLUNAS = len(mapa[0])

nx, ny = LINHAS, COLUNAS

# ---------------- CONFIG ----------------
TAM = 20
OFFSET_X = 500
LARGURA = COLUNAS * TAM + OFFSET_X + 20
ALTURA = LINHAS * TAM + 120

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pac-Lab")

fonte = pygame.font.Font("PressStart2P.ttf", 12)
fonte_titulo_menu = pygame.font.Font("PressStart2P.ttf", 30)
fonte_titulo = pygame.font.Font("PressStart2P.ttf", 20)
fonte_subtitulo = pygame.font.Font("PressStart2P.ttf", 16)

# ---------------- CORES ----------------
BRANCO = (255,255,255)
PRETO = (0,0,0)
VERDE = (0,200,0)
VERMELHO = (200,0,0)
AZUL = (0,0,255)
CINZA = (220,220,220)
CINZA_ESCURO = (180,180,180)
AMARELO = (255, 255, 0)

# ---------------- VARIÁVEIS ----------------
inicio = None
fim = None
caminho = []
custo = 0
scroll_caminho = 0
frame = 0

estado = "menu"
algoritmo = None

clicou = False
pacman = PacmanMenu()

fantasmas = [
    Fantasma(480, 500, (255, 0, 0), 1.2),
    Fantasma(530, 500, (0, 255, 255), 1.2),
    Fantasma(580, 500, (255, 105, 180), 1.2),
    Fantasma(630, 500, (255, 165, 0), 1.2),
]

busca_np = buscaNP()
busca_p = buscaP()


# ---------------- BOTÃO ----------------
def botao(texto, x, y, w, h):
    global clicou

    mouse = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, w, h)

    hover = rect.collidepoint(mouse)

    # fundo preto sempre
    pygame.draw.rect(tela, (0, 0, 0), rect, border_radius=10)

    # borda azul sempre
    pygame.draw.rect(tela, (0, 120, 255), rect, 2, border_radius=10)

    # movimento do pacman
    if hover:
        pacman.move_to(x - 25, y + h // 2)

    # texto muda só no hover
    if hover:
        cor_texto = (255, 255, 0)  # amarelo
    else:
        cor_texto = (255, 255, 255)  # branco

    txt = fonte.render(texto, True, cor_texto)
    txt_rect = txt.get_rect(center=(x + w // 2, y + h // 2 - 1))
    
    tela.blit(txt, txt_rect)

    # clique
    if hover and clicou:
        clicou = False
        return True

    return False

# ---------------- MENU ----------------
def desenhar_menu():
    tela.fill((0, 0, 0))


    titulo = fonte_titulo_menu.render("Escolha o Algoritmo", True, VERMELHO)
    tela.blit(titulo, (260, 80))

    y = 170

    if botao("1. Amplitude", 130, y, 350, 35): return "amplitude"
    if botao("2. Profundidade", 130, y+60, 350, 35): return "profundidade"
    if botao("3. Custo Uniforme", 130, y+120, 350, 35): return "custo_uniforme"
    if botao("4. Greedy", 130, y+180, 350, 35): return "gulosa"
    if botao("5. A*", 130, y+240, 350, 35): return "a_estrela"
    if botao("6. AIA*", 630, y, 350, 35): return "aia_estrela"
    if botao("7. Profundidade Limitada", 630, y+60, 350, 35): return "prof_limitada"
    if botao("8. Aprofundamento Iterativo", 630, y+120, 350, 35): return "aprofundamento"
    if botao("9. Bidirecional", 630, y+180, 350, 35): return "bidirecional"

    pacman.update()
    pacman.draw(tela)

    by = fonte.render("Por: Eduarda Pontes e Júlia Lima", True, BRANCO)
    tela.blit(by, (370, 590))

    for f in fantasmas:
        f.update()
        f.draw(tela) 

    return None

def nome_bonito_algoritmo(alg):
    nomes = {
        "amplitude": "Amplitude",
        "profundidade": "Profundidade",
        "custo_uniforme": "Custo Uniforme",
        "gulosa": "Gulosa",
        "a_estrela": "A*",
        "aia_estrela": "AIA*",
        "prof_limitada": "Profundidade Limitada",
        "aprofundamento": "Aprofundamento Iterativo",
        "bidirecional": "Bidirecional"
    }
    return nomes.get(alg, alg)

def quebrar_linha(texto, fonte, max_largura):
    palavras = texto.split(" ")
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        teste = linha_atual + palavra + " "
        largura, _ = fonte.size(teste)

        if largura <= max_largura:
            linha_atual = teste
        else:
            linhas.append(linha_atual)
            linha_atual = palavra + " "

    linhas.append(linha_atual)
    return linhas

def resetar_pacman_menu():
    pacman.x = 80
    pacman.y = 180
    pacman.target_x = 80
    pacman.target_y = 180

def desenhar_parede(tela, i, j):
    x = j*TAM + OFFSET_X
    y = i*TAM + 60

    # fundo da parede
    pygame.draw.rect(tela, PRETO, (x, y, TAM, TAM))

    esp = 4  # espessura da borda

    # verificar vizinhos
    cima = i > 0 and mapa[i-1][j] == 1
    baixo = i < LINHAS-1 and mapa[i+1][j] == 1
    esquerda = j > 0 and mapa[i][j-1] == 1
    direita = j < COLUNAS-1 and mapa[i][j+1] == 1

    # desenhar bordas só onde NÃO tem vizinho
    if not cima:
        pygame.draw.line(tela, AZUL, (x, y), (x+TAM, y), esp)

    if not baixo:
        pygame.draw.line(tela, AZUL, (x, y+TAM), (x+TAM, y+TAM), esp)

    if not esquerda:
        pygame.draw.line(tela, AZUL, (x, y), (x, y+TAM), esp)

    if not direita:
        pygame.draw.line(tela, AZUL, (x+TAM, y), (x+TAM, y+TAM), esp)


def desenhar_pontinho(tela, x, y):
    pygame.draw.circle(tela, AMARELO, (x + TAM//2, y + TAM//2), 2)


def desenhar_power(tela, x, y, frame):
    tamanho = 4 + int(abs(math.sin(frame * 0.1)) * 2)
    pygame.draw.circle(tela, BRANCO, (x + TAM//2, y + TAM//2), tamanho)

def desenhar_pacman_grid(tela, x, y, frame):
    centro = (x + TAM//2, y + TAM//2)
    raio = TAM//2 - 2

    angulo = abs(math.sin(frame * 0.2)) * 40

    pygame.draw.circle(tela, (255, 255, 0), centro, raio)

    p1 = (centro[0] + raio * math.cos(math.radians(angulo)),
          centro[1] - raio * math.sin(math.radians(angulo)))

    p2 = (centro[0] + raio * math.cos(math.radians(-angulo)),
          centro[1] - raio * math.sin(math.radians(-angulo)))

    pygame.draw.polygon(tela, (0, 0, 0), [centro, p1, p2])

def desenhar_fantasma_grid(tela, x, y):
    # cabeça
    pygame.draw.circle(tela, (255, 60, 60), (x + TAM//2, y + TAM//2 - 2), TAM//2 - 4)

    # corpo
    pygame.draw.rect(tela, (255, 60, 60), (x + 2, y + TAM//2 - 2, TAM - 4, TAM//2))

    # ondinhas
    for i in range(3):
        pygame.draw.circle(tela, (255, 60, 60), (x + 4 + i*6, y + TAM - 4), 3)

    # olhos
    pygame.draw.circle(tela, (255, 255, 255), (x + 6, y + TAM//2 - 2), 3)
    pygame.draw.circle(tela, (255, 255, 255), (x + TAM - 6, y + TAM//2 - 2), 3)

    pygame.draw.circle(tela, (0, 0, 255), (x + 7, y + TAM//2), 1)
    pygame.draw.circle(tela, (0, 0, 255), (x + TAM - 5, y + TAM//2), 1)

# ---------------- GRID ----------------
def desenhar_grid():
    global scroll_caminho
    tela.fill(PRETO)

    area_x = 30
    area_y = 180
    area_w = OFFSET_X - 60
    area_h = 300


    pygame.draw.rect(tela, (20, 20, 20), (area_x, area_y, area_w, area_h))
    pygame.draw.rect(tela, AZUL, (area_x, area_y, area_w, area_h), 2)

    # título
    if algoritmo:
        # texto fixo (preto)
        txt1 = fonte_titulo.render("Algoritmo: ", True, BRANCO)
        tela.blit(txt1, (30, 80))

        # nome do algoritmo (azul)
        nome = nome_bonito_algoritmo(algoritmo)

        # largura máxima antes de bater no grid
        max_largura = OFFSET_X - (10 + txt1.get_width()) - 20

        linhas_nome = quebrar_linha(nome, fonte_subtitulo, max_largura)

        y_nome = 80

        for linha in linhas_nome:
            txt2 = fonte_subtitulo.render(linha, True, AZUL)
            tela.blit(txt2, (10 + txt1.get_width(), y_nome))
            y_nome += 20

    # custo
    txt_custo = fonte.render(f"Custo: {custo}", True, BRANCO)
    tela.blit(txt_custo, (30, 130))

    # caminho
    if caminho:
        titulo_caminho = fonte.render("Caminho:", True, BRANCO)
        tela.blit(titulo_caminho, (area_x, area_y - 25))  # <- sobe o texto

        texto = " -> ".join([str(p) for p in caminho])

        linhas = quebrar_linha(texto, fonte, area_w - 10)

        linha_altura = 20
        max_linhas_visiveis = area_h // linha_altura

        scroll_caminho = min(scroll_caminho, max(0, len(linhas) - max_linhas_visiveis))

        linhas_visiveis = linhas[scroll_caminho:scroll_caminho + max_linhas_visiveis]

        y_texto = area_y + 5

        for linha in linhas_visiveis:
            txt = fonte.render(linha, True, BRANCO)
            tela.blit(txt, (area_x + 5, y_texto))
            y_texto += linha_altura

    # grid
    for i in range(LINHAS):
        for j in range(COLUNAS):

            x = j*TAM + OFFSET_X
            y = i*TAM + 60

            if mapa[i][j] == 1:
                desenhar_parede(tela, i, j)
            else:
                # fundo
                pygame.draw.rect(tela, PRETO, (x, y, TAM, TAM))

                # pontinho
                desenhar_pontinho(tela, x, y)


   # início = PACMAN
    if inicio:
        x = inicio[1]*TAM + OFFSET_X
        y = inicio[0]*TAM + 60
        desenhar_pacman_grid(tela, x, y, frame)

# fim = FANTASMA
    if fim:
        x = fim[1]*TAM + OFFSET_X
        y = fim[0]*TAM + 60
        desenhar_fantasma_grid(tela, x, y)

    # caminho
    for p in caminho:
        pygame.draw.rect(tela, PRETO, (p[1]*TAM + OFFSET_X, p[0]*TAM + 60, TAM, TAM))
    
    if caminho:
        ultimo = caminho[-1]

        x = ultimo[1]*TAM + OFFSET_X
        y = ultimo[0]*TAM + 60

        desenhar_pacman_grid(tela, x, y, frame)

    # botões
    if botao("Iniciar", 50, 520, 100, 35):
        executar_busca()

    if botao("Limpar", 180, 520, 100, 35):
        limpar()

    if botao("Menu", 310, 520, 100, 35):    
        resetar_pacman_menu()
        voltar_menu()

    pacman.update()
    pacman.draw(tela)  

    

# ---------------- FUNÇÕES ----------------
def executar_busca():
    global caminho, custo

    if inicio and fim:

        if algoritmo == "amplitude":
            caminho = busca_np.amplitude_grid(inicio, fim, nx, ny, mapa)
            custo = len(caminho)-1 if caminho else 0

        elif algoritmo == "profundidade":
            caminho = busca_np.profundidade_grid(inicio, fim, nx, ny, mapa)
            custo = len(caminho)-1 if caminho else 0

        elif algoritmo == "prof_limitada":
            caminho = busca_np.prof_limitada_grid(inicio, fim, nx, ny, mapa, 100)
            custo = len(caminho)-1 if caminho else 0

        elif algoritmo == "aprofundamento":
            caminho = busca_np.aprof_iterativo_grid(inicio, fim, nx, ny, mapa, 100)
            custo = len(caminho)-1 if caminho else 0

        elif algoritmo == "bidirecional":
            caminho = busca_np.bidirecional_grid(inicio, fim, nx, ny, mapa)
            custo = len(caminho)-1 if caminho else 0

        elif algoritmo == "custo_uniforme":
            resultado = busca_p.custo_uniforme_grid(inicio, fim, mapa, nx, ny)
            if resultado:
                caminho, custo = resultado

        elif algoritmo == "gulosa":
            resultado = busca_p.greedy_grid(inicio, fim, mapa, nx, ny)
            if resultado:
                caminho, custo = resultado

        elif algoritmo == "a_estrela":
            resultado = busca_p.a_estrela_grid(inicio, fim, mapa, nx, ny)
            if resultado:
                caminho, custo = resultado

        elif algoritmo == "aia_estrela":
            resultado = busca_p.aia_estrela_grid(inicio, fim, mapa, nx, ny)
            if resultado:
                caminho, custo = resultado

def limpar():
    global inicio, fim, caminho, custo
    inicio = None
    fim = None
    caminho = []
    custo = 0

def voltar_menu():
    global estado
    estado = "menu"
    limpar()

def resetar_pacman_jogo():
    pacman.x = 25
    pacman.y = 540
    pacman.target_x = 25
    pacman.target_y = 540



# ---------------- LOOP ----------------
power_pellets = [(1,1), (1, COLUNAS-2), (LINHAS-2,1), (LINHAS-2, COLUNAS-2)]
rodando = True
while rodando:

    clicou = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:  # clique normal
                clicou = True
                click_sound.play()

            elif event.button == 4:  # scroll pra cima
                scroll_caminho = max(0, scroll_caminho - 1)

            elif event.button == 5:  # scroll pra baixo
                scroll_caminho += 1

        if estado == "jogo":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if 60 < y < 60 + LINHAS*TAM:
                    linha = (y - 60) // TAM
                    coluna = (x - OFFSET_X) // TAM
                    

                    if mapa[linha][coluna] == 0:
                        if not inicio:
                            inicio = (linha, coluna)
                        elif not fim:
                            fim = (linha, coluna)
    for p in power_pellets:
        x = p[1]*TAM + OFFSET_X
        y = p[0]*TAM + 60
        desenhar_power(tela, x, y, frame)

    if estado == "menu":
        escolha = desenhar_menu()
        if escolha:
            algoritmo = escolha
            estado = "jogo"
            resetar_pacman_jogo()
    else:
        desenhar_grid() 

    

    frame += 1
    pygame.display.update()


pygame.quit()
sys.exit()