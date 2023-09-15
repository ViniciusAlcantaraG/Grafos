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
        self.matriz = [[0 for j in range(self.n)] for i in range(self.n)]
        for i in range(len(links)):
            a = links[i][0] - 1
            b = links[i][1] - 1
            self.matriz[a][b] = self.matriz[b][a] = 1
            
    def __repr__(self):
        return str(self.matriz)
    
    def BFS(self, raiz):
        nivel = [0 for i in range(self.n)]
        pai = [0 for i in range(self.n)]
        self.verticesBFS = [0 for i in range(self.n)]
        fila = []
        self.verticesBFS[raiz - 1] = 1
        fila.append(raiz-1)
        while fila != []:
            v = fila[0]
            fila.pop(0)
            for i in range(len(self.matriz[v])):
                if self.matriz[v][i] == 1:
                    if self.verticesBFS[i] == 0:
                        pai[i] = v + 1
                        nivel[i] = nivel[v] + 1
                        self.verticesBFS[i] = 1
                        fila.append(i)
        return pai, nivel
    
    def DFS(self, raiz):
        nivel = [0 for i in range(self.n)]
        pai = [0 for i in range(self.n)]
        vertices = [0 for i in range(self.n)]
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
        distancias = []
        for i in range(self.n):
            for j in range(self.n):
                if i!=j:
                    distancias.append(self.distancia(i,j))
        return max(distancias)
    
    def componentes_conexos(self):
        tamanho = []
        Ver_BFS = [0 for i in range(self.n)]
        lista_vert = []
        self.BFS(1)
        tamanho.append(self.verticesBFS.count(1))
        for i in range(self.n):
            if self.verticesBFS[i] == 1:
                lista_vert.append(i+1)
                Ver_BFS[i] = 1
        while len(lista_vert) != self.n:
            if Ver_BFS.index(0)+1 not in lista_vert:
                self.BFS(Ver_BFS.index(0)+1)
                tamanho.append(self.verticesBFS.count(1))
                for i in range(self.n):
                    if self.verticesBFS[i] == 1:
                        lista_vert.append(i+1)
                        Ver_BFS[i] = 1
        x = 0
        lista2 = []
        for i in range(len(tamanho)):
            lista2.append(lista_vert[x:tamanho[i]+x])
            x = tamanho[i]
        return tamanho, lista2, len(tamanho)
    
class Lista_Grafo(Grafo):
    def __init__(self, n, links):
        super().__init__(n, links)



cachorro = Matriz_Grafo(5, [[1,2],[2,3],[1,3],[4,5]])
print(cachorro.componentes_conexos())
