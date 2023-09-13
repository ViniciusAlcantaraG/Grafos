class Grafo:
    def __init__(self, n, links):
        self.n = n
        self.links = links


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
        vertices = [0 for i in range(self.n)]
        fila = []
        vertices[raiz - 1] = 1
        fila.append(raiz-1)
        while fila != []:
            v = fila[0]
            fila.pop(0)
            for i in range(len(self.matriz[v])):
                if self.matriz[v][i] == 1:
                    if vertices[i] == 0:
                        vertices[i] = 1
                        fila.append(i)

                
            



        


    
class Lista_Grafo(Grafo):
    def __init__(self, n, links):
        super().__init__(n, links)



cachorro = Matriz_Grafo(5, [[1,2],[2,5],[5,3],[4,5],[1,5]])
print(cachorro)
cachorro.BFS(1)
