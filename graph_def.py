import numpy as np
import functools 
import statistics 
from time import time
import random

with open("grafo_1.txt") as f:
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
        for i in range(len(links)):
            a = links[i][0] - 1
            b = links[i][1] - 1
            self.matriz[a][b] = self.matriz[b][a] = 1
            
    def __repr__(self):
        return str(self.matriz)
    
    def BFS(self, raiz):
        nivel = np.zeros(self.n, dtype = int)
        pai = np.zeros(self.n, dtype = int)
        self.verticesBFS = np.zeros(self.n, dtype = int)
        fila = np.array([raiz-1])
        self.verticesBFS[raiz - 1] = 1
        while len(fila) != 0:
            v = fila[0]
            fila = fila[1:]
            for i in range(len(self.matriz[v])):
                if self.matriz[v][i] == 1:
                    if self.verticesBFS[i] == 0:
                        pai[i] = v + 1
                        nivel[i] = nivel[v] + 1
                        self.verticesBFS[i] = 1
                        fila = np.concatenate((fila, np.array([i])))
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
                for i in range(len(self.matriz[u])):
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
        nivel = np.zeros(self.n, dtype = int)
        pai = np.zeros(self.n, dtype = int)
        self.vertices_BFS = np.zeros(self.n, dtype = int)
        fila = np.array([raiz-1])
        self.vertices_BFS[raiz-1] = 1
        while len(fila) != 0:
            v = fila[0]
            fila = fila[1:]
            for i in self.lista[v]:
                if self.vertices_BFS[i-1] == 0:
                    pai[i-1] = v + 1
                    nivel[i-1] = nivel[v] + 1
                    self.vertices_BFS[i-1] = 1
                    fila = np.concatenate((fila, np.array([i-1])))
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
        distancias = np.array([])
        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                if j <=i:
                    pass
                else:
                    distancias = np.concatenate((distancias, np.array([self.distancia(i,j)])))
        return int(distancias.max())
    
    def componentes_conexos(self):
        tamanho = np.array([], dtype = int)
        Ver_BFS = [0 for i in range(self.n)]
        lista_vert = np.array([], dtype = int)
        self.BFS(1)
        tamanho = np.concatenate((tamanho, np.array([np.count_nonzero(self.vertices_BFS == 1)])))
        for i in range(self.n):
            if self.vertices_BFS[i] == 1:
                lista_vert = np.concatenate((lista_vert,np.array([i+1])))
                Ver_BFS[i] = 1
        while len(lista_vert) != self.n:
            if Ver_BFS.index(0)+1 not in lista_vert:
                self.BFS(Ver_BFS.index(0)+1)
                tamanho = np.concatenate((tamanho, np.array([np.count_nonzero(self.vertices_BFS == 1)])))
                for i in range(self.n):
                    if self.vertices_BFS[i] == 1:
                        lista_vert = np.concatenate((lista_vert, np.array([i+1])))
                        Ver_BFS[i] = 1
        lista_vert = list(lista_vert)
        for i in range(len(tamanho)):
            if i != len(tamanho) - 1:
                lista_vert[i:tamanho[i]] = [lista_vert[i:tamanho[i]]]
            else:
                lista_vert[i:] = [lista_vert[i:]]
        return tamanho, lista_vert, len(tamanho)


cachorrinho = Lista_Grafo(5, [[1,2], [2,3], [1,3], [4,5]])
print(cachorrinho.componentes_conexos())
cachorro = Lista_Grafo(number_vertices, links)
a=[[1,2,3],[2],[1,2]]
b = np.array(cachorro.lista)
b = np.array(list(map(len, b)))
#media = functools.reduce(lambda a, c: a+c, b)//10000
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
