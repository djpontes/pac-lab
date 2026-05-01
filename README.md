PAC-LAB — Projeto de Inteligência Artificial em Jogos
======================================================

Desenvolvido por: Eduarda Pontes e Júlia Lima

------------------------------------------------------
1. DESCRIÇÃO DO PROJETO
------------------------------------------------------

O PAC-LAB é um simulador visual de algoritmos de busca desenvolvido em Python
utilizando a biblioteca Pygame. O objetivo do projeto é demonstrar, de forma
interativa, o funcionamento de diferentes algoritmos de Inteligência Artificial
aplicados à busca de caminhos em um grid.

O usuário pode selecionar um algoritmo e visualizar o caminho encontrado entre
um ponto inicial (Pac-Man) e um ponto final (Fantasma).

Algoritmos implementados:
- Busca em Amplitude (BFS)
- Busca em Profundidade (DFS)
- Custo Uniforme
- Busca Gulosa (Greedy)
- A*
- AIA*
- Profundidade Limitada
- Aprofundamento Iterativo
- Busca Bidirecional

------------------------------------------------------
2. REQUISITOS
------------------------------------------------------

✔ Python 3.10 ou superior

✔ Ambiente virtual (venv)

✔ Bibliotecas utilizadas:
- pygame
- numpy

✔ Bibliotecas nativas (não precisam instalação):
- math
- sys

------------------------------------------------------
3. AMBIENTE VIRTUAL (VENV)
------------------------------------------------------

O projeto foi desenvolvido utilizando um ambiente virtual (venv) para isolar
as dependências do Python.

Para criar o ambiente virtual (caso necessário):

    python -m venv venv

Para ativar o ambiente:

    Windows:
    venv\Scripts\activate

    Linux / Mac:
    source venv/bin/activate

------------------------------------------------------
4. INSTALAÇÃO DAS DEPENDÊNCIAS
------------------------------------------------------

As dependências do projeto estão listadas no arquivo:

    requirements.txt

Para instalar todas as bibliotecas necessárias, execute:

    pip install -r requirements.txt

OBS: Se caso a instalação pelo requirements.txt de errado, execute:

    pip install pygame numpy


------------------------------------------------------
5. COMO EXECUTAR O PROGRAMA
------------------------------------------------------

Após ativar o ambiente virtual e instalar as dependências:

    python main.py

------------------------------------------------------
6. FUNCIONAMENTO DA INTERFACE GRÁFICA
------------------------------------------------------

O sistema possui duas telas principais:

✔ MENU INICIAL

    - O usuário escolhe um dos algoritmos de busca:
        Amplitude
        Profundidade
        Custo Uniforme
        Greedy
        A*
        AIA*
        Profundidade Limitada
        Aprofundamento Iterativo
        Bidirecional


✔ TELA DO JOGO (EXECUÇÃO)

    - O mapa é exibido em formato de grade (grid).
        Durante a execução do algoritmo, o usuário interage com o mapa clicando nas células do grid.

        Regras de seleção:

        - Só pode clicar em células válidas do caminho.
        - Células válidas são representadas por "moedinhas".
        - Qualquer clique em parede é ignorado pelo sistema.

    - Clique no mapa:
        1º clique → define o ponto de origem (Pac-Man)
        2º clique → define o ponto de destino (Fantasma)
    - Clique em “Iniciar” para executar a busca

    Botões disponíveis:
    - Iniciar → executa o algoritmo selecionado
    - Limpar → limpa o início, fim, caminho e custo
    - Menu → retorna à tela inicial (menu)

------------------------------------------------------
7. ESTRUTURA DO PROJETO
------------------------------------------------------

main.py → código principal da aplicação
node.py → estrutura de nó para buscas não informadas
nodeP.py → estrutura de nó para buscas informadas (heurísticas)
buscaNP.py → algoritmos de busca não informada
buscaP.py → algoritmos de busca informada
mapa.txt → representação do labirinto
requirements.txt → dependências do projeto
assets/ → fontes e sons

------------------------------------------------------
8. OBSERVAÇÕES
------------------------------------------------------

- O mapa pode ser alterado diretamente no arquivo mapa.txt.
