from collections import deque
from nodeP import NodeP
from math import sqrt, fabs

class buscaP(object):
#--------------------------------------------------------------------------
# SUCESSORES PARA GRID
#--------------------------------------------------------------------------
    def sucessores_grid(self,st,nx,ny,mapa):
        f = []
        x, y = st[0], st[1]
        # DIREITA
        if y+1<ny:
            if mapa[x][y+1]!=1:
                suc = []
                suc.append(x)
                suc.append(y+1)
                custo = 5
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        # ESQUERDA
        if y-1>=0:
            if mapa[x][y-1]==0:
                suc = []
                suc.append(x)
                suc.append(y-1)
                custo = 7
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        # ABAIXO
        if x+1<nx:
            if mapa[x+1][y]==0:
                suc = []
                suc.append(x+1)
                suc.append(y)
                custo = 2
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        # ACIMA
        if x-1>=0:
            if mapa[x-1][y]==0:
                suc = []
                suc.append(x-1)
                suc.append(y)
                custo = 3
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)        
        return f
#--------------------------------------------------------------------------    
# INSERE NA LISTA MANTENDO-A ORDENADA
#--------------------------------------------------------------------------    
    def inserir_ordenado(self,lista, no):
        for i, n in enumerate(lista):
            if no.v1 < n.v1:
                lista.insert(i, no)
                break
        else:
            lista.append(no)
#--------------------------------------------------------------------------    
# EXIBE O CAMINHO ENCONTRADO NA ÁRVORE DE BUSCA
#--------------------------------------------------------------------------    
    def exibirCaminho(self,node):
        caminho = []
        while node is not None:
            caminho.append(node.estado)
            node = node.pai
        caminho.reverse()
        return caminho

#--------------------------------------------------------------------------    
# GERA H - GRID
#--------------------------------------------------------------------------    
    def heuristica_grid(self,p1,p2):
        if (p2[0]-p1[0])<0:
            c1 = 3
        else:
            c1 = 2
        if (p2[1]-p1[1])<0:
            c2 = 7
        else:
            c2 = 5
        h = sqrt(c1*(p1[0]-p2[0])*(p1[0]-p2[0]) + c2*(p1[1]-p2[1])*(p1[1]-p2[1]))
        #h = c1*fabs(p1[0]-p2[0]) + c2*fabs(p1[1]-p2[1])
        return h
# -----------------------------------------------------------------------------
# CUSTO UNIFORME - GRID
# -----------------------------------------------------------------------------
    def custo_uniforme_grid(self,inicio,fim,mapa,nx,ny): # grid
        # Origem igual a destino
        if inicio == fim:
            return [inicio], 0
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        t_inicio = tuple(inicio)
        raiz = NodeP(None, t_inicio,0, None, None, 0)
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {tuple(inicio): raiz}
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Chegou ao objetivo
            if atual.estado == fim:
                return self.exibirCaminho(atual), atual.v2
    
            # Gera sucessores - grid
            filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
    
            for novo in filhos:
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = v2
    
                # Não visitado ou custo melhor
                t_novo = tuple(novo[0])
                if (t_novo not in visitado) or (v2<visitado[t_novo].v2):
                    filho = NodeP(atual,t_novo, v1, None, None, v2)
                    visitado[t_novo] = filho
                    self.inserir_ordenado(lista, filho)
        return None

# -----------------------------------------------------------------------------
# GREEDY - GRID
# -----------------------------------------------------------------------------
    def greedy_grid(self,inicio,fim,mapa,nx,ny): # grid
        # Origem igual a destino
        if inicio == fim:
            return [inicio], 0
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        t_inicio = tuple(inicio)
        raiz = NodeP(None, t_inicio,0, None, None, 0)
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {tuple(inicio): raiz}
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Chegou ao objetivo
            if atual.estado == fim:
                return self.exibirCaminho(atual), atual.v2
            
            # Gera sucessores
            filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
    
            for novo in filhos:
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = self.heuristica_grid(novo[0],fim)  
    
                # Não visitado ou custo melhor
                t_novo = tuple(novo[0])
                if (t_novo not in visitado) or (v2<visitado[t_novo].v2):
                    filho = NodeP(atual,t_novo, v1, None, None, v2)
                    visitado[t_novo] = filho
                    self.inserir_ordenado(lista, filho)
        return None

# -----------------------------------------------------------------------------
# A ESTRELA- GRID
# -----------------------------------------------------------------------------
    def a_estrela_grid(self,inicio,fim,mapa,nx,ny):
        # Origem igual a destino
        if inicio == fim:
            return [inicio], 0
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        t_inicio = tuple(inicio)
        raiz = NodeP(None, t_inicio,0, None, None, 0)
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {tuple(inicio): raiz}
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Chegou ao objetivo
            if atual.estado == fim:
                return self.exibirCaminho(atual), atual.v2
            
            # Gera sucessores
            filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
    
            for novo in filhos:
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = v2 + self.heuristica_grid(novo[0],fim)  
    
                # Não visitado ou custo melhor
                t_novo = tuple(novo[0])
                if (t_novo not in visitado) or (v2<visitado[t_novo].v2):
                    filho = NodeP(atual,t_novo, v1, None, None, v2)
                    visitado[t_novo] = filho
                    self.inserir_ordenado(lista, filho)
        return None

# -----------------------------------------------------------------------------
# AIA ESTRELA- GRID
# -----------------------------------------------------------------------------
    def aia_estrela_grid(self,inicio,fim,mapa,nx,ny):
        # Origem igual a destino
        if inicio == fim:
            return [inicio], 0
        lim = self.heuristica_grid(inicio,fim)
        
        while True:        
            # Fila de prioridade baseada em deque + inserção ordenada
            lista = deque()
            t_inicio = tuple(inicio)
            raiz = NodeP(None, t_inicio,0, None, None, 0)
            lista.append(raiz)
        
            # Controle de nós visitados
            visitado = {tuple(inicio): raiz}
            
            # loop de busca
            novo_lim = []
            while lista:
                # remove o primeiro nó
                atual = lista.popleft()
                valor_atual = atual.v2
        
                # Chegou ao objetivo
                if atual.estado == fim:
                    return self.exibirCaminho(atual), atual.v2
                
                # Gera sucessores
                filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
        
                for novo in filhos:
                    # custo acumulado até o sucessor
                    v2 = valor_atual + novo[1]
                    v1 = v2 + self.heuristica_grid(novo[0],fim)
                    
                    if v1<=lim:        
                        # Não visitado ou custo melhor
                        t_novo = tuple(novo[0])
                        if (t_novo not in visitado) or (v2<visitado[t_novo].v2):
                            filho = NodeP(atual,t_novo, v1, None, None, v2)
                            visitado[t_novo] = filho
                            self.inserir_ordenado(lista, filho)
                    else:
                        novo_lim.append(v1)
            lim = (int)(sum(novo_lim)/(len(novo_lim)))
            lista.clear()
            visitado.clear()
            novo_lim.clear()
        return None
