import numpy as np
import functools 
import statistics 
from time import time, sleep
import random
from collections import deque
import gc

# Ativação do garbage collector.
gc.enable()

# A leitura do arquivo texto ocorre fora das classes definidas.
with open("grafo_6.txt") as f:
    mylist = f.read().splitlines() 
links = []
for i in range(1, len(mylist)):
    a,b = mylist[i].split(" ")
    links.append([int(a),int(b)])
number_vertices = int(mylist[0])
# Definimos o número de vértices e o número de arestas.

class Grafo:
    def __init__(self, n, links):
        # Definimos n como o número de vértices e links como as arestas.
        self.n = n
        self.links = links

class Matriz_Grafo(Grafo):
    def __init__(self, n, links):
        super().__init__(n, links)
        # Utilizamos herança para a classe Matriz ter as mesmas características da classe Grafo.
        self.matriz = np.zeros((self.n, self.n), dtype = int) 
        for a, b in links:
            a -= 1
            b -= 1
            self.matriz[a][b] = self.matriz[b][a] = 1
            
    def __repr__(self):
        return str(self.matriz)
    
    def BFS(self, raiz):
        nivel = [0] * self.n
        pai = [0] * self.n
        self.verticesBFS = [0] * self.n
        fila = deque([raiz-1])
        self.verticesBFS[raiz-1] = 1
        while fila:
            v = fila.popleft()
            for i in range(self.n):
                if self.matriz[v][i] == 1 and self.verticesBFS[i] == 0:
                    pai[i] = v + 1
                    nivel[i] = nivel[v] + 1
                    self.verticesBFS[i] = 1
                    fila.append(i)
        return pai, nivel
    
    def DFS(self, raiz):
        nivel = [0] * self.n
        pai = [0] * self.n
        vertices = [0] * self.n
        pilha = deque()
        pilha.append(raiz-1)
        while len(pilha) !=0:
            u = pilha.pop()
            if vertices[u] == 0:
                vertices[u] = 1
                for i in range(self.n):
                    if self.matriz[u][i] == 1:
                        pilha.append(i)
                        if vertices[i] == 0:
                            pai[i] = u + 1
                            nivel[i] = nivel[u] + 1
        return pai, nivel

    def distancia(self, u, v):
        return self.BFS(u)[1][v-1]
    
    def diametro(self):
        distancias = np.array([])
        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                if i!=j:
                    distancias = np.concatenate((distancias, np.array([self.distancia(i,j)])))
        return int(distancias.max())
    
    def componentes_conexos(self):
        tamanho = np.array([], dtype = int)
        Ver_BFS = [0 for i in range(self.n)]
        lista_vert = np.array([], dtype = int)
        self.BFS(1)
        tamanho = np.concatenate((tamanho, np.array([np.count_nonzero(self.verticesBFS == 1)])))
        for i in range(self.n):
            if self.verticesBFS[i] == 1:
                lista_vert = np.concatenate((lista_vert,np.array([i+1])))
                Ver_BFS[i] = 1
        while len(lista_vert) != self.n:
            if Ver_BFS.index(0)+1 not in lista_vert:
                self.BFS(Ver_BFS.index(0)+1)
                tamanho = np.concatenate((tamanho, np.array([np.count_nonzero(self.verticesBFS == 1)])))
                for i in range(self.n):
                    if self.verticesBFS[i] == 1:
                        lista_vert = np.concatenate((lista_vert, np.array([i+1])))
                        Ver_BFS[i] = 1
        lista_vert = list(lista_vert)
        for i in range(len(tamanho)):
            if i != len(tamanho) - 1:
                lista_vert[i:tamanho[i]] = [lista_vert[i:tamanho[i]]]
            else:
                lista_vert[i:] = [lista_vert[i:]]
        return tamanho, lista_vert, len(tamanho)
    
class Lista_Grafo(Grafo):
    def __init__(self, n, links):
        super().__init__(n, links)
        self.lista=[[] for i in range(self.n)]
        for i in range(len(self.links)):
            [a,b] = self.links[i]
            self.lista[a-1].append(b)
            self.lista[b-1].append(a)
        for i in range(len(self.lista)):
            self.lista[i].sort()
    def __repr__(self):
        return str(self.lista)
    
    def BFS(self, raiz):
        nivel = [0] * self.n
        pai = [0] * self.n
        self.vertices_BFS = [0] * self.n
        fila = deque([raiz - 1])
        self.vertices_BFS[raiz - 1] = 1

        while fila:
            v = fila.popleft()
            for i in self.lista[v]:
                if self.vertices_BFS[i-1] == 0:
                    pai[i - 1] = v + 1
                    nivel[i - 1] = nivel[v] + 1
                    self.vertices_BFS[i - 1] = 1
                    fila.append(i - 1)

        return pai, nivel
    def DFS(self, raiz):
        nivel = [0] * self.n
        pai = [0] * self.n
        vertices = [0] * self.n
        pilha = deque()
        pilha.append(raiz-1)
        while len(pilha) != 0:
            u = pilha.pop()
            if vertices[u] == 0:
                vertices[u] = 1
                for i in self.lista[u]:
                    pilha.append(i-1)
                    if vertices[i-1] == 0:
                        pai[i-1] = u + 1
                        nivel[i-1] = nivel[u] + 1
        return pai, nivel
    
    def distancia(self, u ,v):
        return self.BFS(u)[1][v-1]
    
    def diametro(self):
        diam = 0
        for i in range(1, self.n + 1):
            níveis = self.BFS(i)[1]
            nível_max = max(níveis)
            diam = max(diam, nível_max)
        return diam
    def diametro_aprox(self):
        # Nossa aproximação exige a definição de um número de amostras. Quanto maior o número,
        # será a aproximação.
        distancias_max = []
        num_amostras = 1000
        diam = 0
        for j in range(num_amostras):
            vertices = random.randint(1, self.n)
            níveis = self.BFS(vertices)[1]
            nível_max = max(níveis)
            diam = max(diam, nível_max)
        return diam
    
    def componentes_conexos(self):
        # Realizamos uma BFS com raiz em 1. Caso algum vértice não tenha sido descoberto,
        # executamos uma nova BFS com esse vértice como raiz. Assim, o número de BFS's
        # será igual ao número de componentes conexas.
        tamanho = np.array([], dtype = int)
        Ver_BFS = [0 for i in range(self.n)]
        lista_vert = np.array([], dtype = int)
        self.BFS(1)
        tamanho = np.concatenate((tamanho, np.array([len(self.vertices_BFS)])))
        for i in self.vertices_BFS:
            lista_vert = np.concatenate((lista_vert,np.array([i+1])))
            Ver_BFS[i] = 1
        while len(lista_vert) != self.n:
            if Ver_BFS.index(0)+1 not in lista_vert:
                self.BFS(Ver_BFS.index(0)+1)
                tamanho = np.concatenate((tamanho, np.array([len(self.vertices_BFS)])))
                for i in self.vertices_BFS:
                    lista_vert = np.concatenate((lista_vert, np.array([i+1])))
                    Ver_BFS[i] = 1
        lista_vert = list(lista_vert)
        for i in range(len(tamanho)):
            if i != len(tamanho) - 1:
                lista_vert[i:tamanho[i]] = [lista_vert[i:tamanho[i]]]
            else:
                lista_vert[i:] = [lista_vert[i:]]
        return tamanho, lista_vert, len(tamanho)


arquivo = Lista_Grafo(number_vertices, links)

b = np.array(cachorro.lista)
b = np.array(list(map(len,b)))

# Definição de alguns valores que estarão presentes no arquivo de saída.
media = functools.reduce(lambda a, c: a+c, b)//number_vertices
media = statistics.mean(b)
mediana = statistics.median(np.sort(b))
tamanho = arquivo.componentes_conexos()[2]
tamanho_de_cada_componente = arquivo.componentes_conexos()[0]
vertices_conexos = arquivo.componentes_conexos()[1]

# Arquivo de sáida
g = open("saida.txt", "w")
g.write("Número de vértices: " + str(number_vertices) + "\n" + 
        "Número de arestas: " + str(len(links)) + "\n" +
        "Grau mínimo: " + str(b.min()) + "\n" + 
        "Grau máximo: " + str(b.max()) + "\n" + 
        "Grau médio: " + str(media) + "\n" +
        "Mediana de grau: " + str(int(mediana)) + "\n" +
        "Número de componentes conexas: " + str(tamanho) + "\n" +
        "Tamanho de cada componente: " + str(tamanho_de_cada_componente) + "\n" + 
        "Lista de vértices pertencentes à componente: " + str(vertices_conexos))

# Trecho do código responsável pela execução das 100 DFS's e BFS's
tempos = []
for i in range(100):
    start_time = time()
    arquivo.DFS(random.randint(1, number_vertices))
    time_elapsed = time() - start_time
    tempos.append(time_elapsed)
print(tempos)
print(sum(tempos)/100)


gc.disable()
