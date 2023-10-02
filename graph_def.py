import numpy as np
import functools 
import statistics 
from time import time
import random
from collections import deque
import gc

with open("grafo_3.txt") as f:
    mylist = f.read().splitlines() 
links = []
for i in range(1, len(mylist)):
    a,b = mylist[i].split(" ")
    links.append([int(a),int(b)])
number_vertices = int(mylist[0])
print(number_vertices, len(links))



class Grafo:
    def __init__(self, n, links):
        self.n = n
        self.links = links

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
 
 
class Stack:
 
    # Initializing a stack.
    # Use a dummy node, which is
    # easier for handling edge cases.
    def __init__(self):
        self.head = Node("head")
        self.size = 0
 
    # String representation of the stack
    def __str__(self):
        cur = self.head.next
        out = ""
        while cur:
            out += str(cur.value) + "->"
            cur = cur.next
        return out[:-2]
 
    # Get the current size of the stack
    def getSize(self):
        return self.size
 
    # Check if the stack is empty
    def isEmpty(self):
        return self.size == 0
 
    # Get the top item of the stack
    def peek(self):
 
        # Sanitary check to see if we
        # are peeking an empty stack.
        if self.isEmpty():
            raise Exception("Peeking from an empty stack")
        return self.head.next.value
 
    # Push a value into the stack.
    def push(self, value):
        node = Node(value)
        node.next = self.head.next
        self.head.next = node
        self.size += 1
 
    # Remove a value from the stack and return.
    def pop(self):
        if self.isEmpty():
            raise Exception("Popping from an empty stack")
        remove = self.head.next
        self.head.next = self.head.next.next
        self.size -= 1
        return remove.value

class Matriz_Grafo(Grafo):
    def __init__(self, n, links):
        super().__init__(n, links)
        self.matriz = np.zeros((self.n, self.n), dtype = int) 
        for a, b in links:
            a -= 1
            b -= 1
            self.matriz[a][b] = 1
        self.matriz = np.triu(self.matriz)
    def __repr__(self):
        return str(self.matriz)
    
    def BFS(self, raiz):
        nivel = [0] * self.n
        pai = [0] * self.n
        self.verticesBFS = set()
        fila = deque([raiz-1])
        self.verticesBFS.add(raiz-1)
        while fila:
            v = fila.popleft()
            for i in range(self.n):
                if self.matriz[v][i] == 1 and i not in self.verticesBFS:
                    pai[i] = v + 1
                    nivel[i] = nivel[v] + 1
                    self.verticesBFS.add(i)
                    fila.append(i)
        return pai, nivel
    
    def DFS(self, raiz):
        nivel = [0] * self.n
        pai = [0] * self.n
        vertices = [0] * self.n
        pilha = Stack()
        pilha.push(raiz-1)
        while not pilha.isEmpty:
            u = pilha.pop()
            if vertices[u] == 0:
                vertices[u] = 1
                for i in range(self.n):
                    if self.matriz[u][i] == 1:
                        pilha.push(i)
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
        self.vertices_BFS = set()
        fila = deque([raiz - 1])
        self.vertices_BFS.add(raiz - 1)

        while fila:
            v = fila.popleft()
            for i in self.lista[v]:
                if i - 1 not in self.vertices_BFS:
                    pai[i - 1] = v + 1
                    nivel[i - 1] = nivel[v] + 1
                    self.vertices_BFS.add(i - 1)
                    fila.append(i - 1)

        return pai, nivel
    def DFS(self, raiz):
        nivel = np.zeros(self.n, dtype = int)
        pai = np.zeros(self.n, dtype = int)
        vertices = np.zeros(self.n, dtype = int)
        pilha = Stack()
        pilha.push(raiz-1)
        while pilha.isEmpty() == False:
            u = pilha.pop()
            if vertices[u] == 0:
                vertices[u] = 1
                for i in self.lista[u]:
                    pilha.push(i-1)
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


cachorrinho = Lista_Grafo(5, [[1,2], [2,5], [5,3], [4,5], [1,5]])
#print(cachorrinho.componentes_conexos())
cachorro = Lista_Grafo(number_vertices, links)
#print(cachorro.BFS(1))

#a=[[1,2,3],[2],[1,2]]
#b = np.array(cachorro.lista)
#b = np.array(list(map(len, b)))
media = functools.reduce(lambda a, c: a+c, b)//10000
media = statistics.mean(b)
mediana = statistics.median(np.sort(b))
tamanho = cachorro.componentes_conexos()[2]
tamanho_de_cada_componente = cachorro.componentes_conexos()[0]
vertices_conexos = cachorro.componentes_conexos()[1]

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
tempos = []
"""for i in range(100):
    start_time = time()
    cachorro.DFS(random.randint(1, number_vertices))
    time_elapsed = time() - start_time
    tempos.append(time_elapsed)
print(tempos)
print(sum(tempos)/100)"""

a = cachorro.diametro_aprox()
#print(cachorro.componentes_conexos()[2])
print(a)
