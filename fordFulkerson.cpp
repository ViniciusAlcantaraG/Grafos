#include <iostream>
#include <vector>
#include <queue>
#include <limits>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <string>
#include <time.h>
using namespace std;

// Definindo a estrutura Edge
struct Edge {
    int v1;
    int v2;
    float peso;

    Edge(int vertex1, int vertex2, float weight) : v1(vertex1), v2(vertex2), peso(weight) {}
};

// Definindo a classe Grafos
class Grafos {
public:
    int number_vertices;
    vector<vector<pair<int, float>>> links;
    bool isDirecionado;

    Grafos(int n, const vector<Edge>& conexoes, bool direcionado) : number_vertices(n), links(n), isDirecionado(direcionado) {
        links.resize(n);
        for (const Edge& edge : conexoes) {
            links[edge.v1 - 1].push_back({edge.v2 - 1, edge.peso});

            if (!isDirecionado) {
                // Adicione a aresta reversa se o grafo não for direcionado
                links[edge.v2 - 1].push_back({edge.v1 - 1, edge.peso});
            }
        }
    }
};

// Função para copiar o grafo original
vector<vector<pair<int, float>>> copiarGrafoOriginal(const vector<vector<pair<int, float>>>& grafo) {
    // Crie uma cópia do grafo original
    vector<vector<pair<int, float>>> copia(grafo.size());

    for (int i = 0; i < grafo.size(); ++i) {
        for (const auto& edge : grafo[i]) {
            copia[i].push_back({edge.first, edge.second});
        }
    }

    return copia;
}

// Função para encontrar um caminho aumentante usando BFS
vector<int> encontrarCaminhoAumentante(const vector<vector<pair<int, float>>>& grafoResidual, int origem, int destino) {
    queue<int> fila;
    vector<int> parent(grafoResidual.size(), -1);

    fila.push(origem);
    parent[origem] = origem;

    while (!fila.empty()) {
        int atual = fila.front();
        fila.pop();

        for (const auto& vizinho : grafoResidual[atual]) {
            int proximo = vizinho.first;

            if (parent[proximo] == -1 && vizinho.second > 0) {
                parent[proximo] = atual;
                fila.push(proximo);

                if (proximo == destino) {
                    // Caminho aumentante encontrado
                    vector<int> caminho;
                    int v = destino;
                    while (v != origem) {
                        caminho.push_back(v);
                        v = parent[v];
                    }
                    caminho.push_back(origem);
                    reverse(caminho.begin(), caminho.end());
                    return caminho;
                }
            }
        }
    }

    // Não há mais caminhos aumentantes
    return vector<int>();
}

// Função para encontrar a capacidade residual mínima ao longo do caminho aumentante
float encontrarCapacidadeResidualMinima(const vector<vector<pair<int, float>>>& grafoResidual, const vector<int>& caminho) {
    float capacidadeMinima = numeric_limits<float>::infinity();

    for (int i = 0; i < caminho.size() - 1; ++i) {
        int atual = caminho[i];
        int proximo = caminho[i + 1];

        for (const auto& vizinho : grafoResidual[atual]) {
            if (vizinho.first == proximo) {
                capacidadeMinima = min(capacidadeMinima, vizinho.second);
                break;
            }
        }
    }

    return capacidadeMinima;
}

// Função para atualizar o grafo residual subtraindo a capacidade residual mínima do fluxo nas arestas
void atualizarGrafoResidual(vector<vector<pair<int, float>>>& grafoResidual, const vector<int>& caminho, float capacidadeResidualMinima) {
    for (int i = 0; i < caminho.size() - 1; ++i) {
        int atual = caminho[i];
        int proximo = caminho[i + 1];

        for (auto& vizinho : grafoResidual[atual]) {
            if (vizinho.first == proximo) {
                vizinho.second -= capacidadeResidualMinima;
                break;
            }
        }

        // Adicionar a capacidade residual mínima ao fluxo reverso
        for (auto& vizinho : grafoResidual[proximo]) {
            if (vizinho.first == atual) {
                vizinho.second += capacidadeResidualMinima;
                break;
            }
        }
    }
}

// Função para o algoritmo Ford-Fulkerson
float fordFulkerson(const Grafos& grafo, int origem, int destino) {
    float fluxoMaximo = 0;

    // Criar uma cópia do grafo original para armazenar o grafo residual
    vector<vector<pair<int, float>>> grafoResidual = copiarGrafoOriginal(grafo.links);

    // Enquanto existir um caminho aumentante de origem até destino no grafoResidual
    while (true) {
        // Encontrar um caminho aumentante usando BFS
        vector<int> caminhoAumentante = encontrarCaminhoAumentante(grafoResidual, origem, destino);

        // Se não houver caminho aumentante, terminar o loop
        if (caminhoAumentante.empty()) {
            break;
        }

        // Encontrar a capacidade residual mínima ao longo do caminho aumentante
        float capacidadeResidualMinima = encontrarCapacidadeResidualMinima(grafoResidual, caminhoAumentante);

        // Atualizar o grafo residual subtraindo a capacidade residual mínima do fluxo nas arestas
        atualizarGrafoResidual(grafoResidual, caminhoAumentante, capacidadeResidualMinima);

        // Adicionar a capacidade residual mínima ao fluxo máximo
        fluxoMaximo += capacidadeResidualMinima;
    }

    //essa parte é descartável da função
    vector<vector<pair<int, float>>> grafoOriginal = copiarGrafoOriginal(grafo.links);
    // Depois de executar o algoritmo de Ford-Fulkerson, calcule o fluxo para cada aresta
    for (int v1 = 0; v1 < grafo.number_vertices; ++v1) {
        for (const auto& edge : grafoOriginal[v1]) {
            int v2 = edge.first;
            float pesoOriginal = edge.second;
            float pesoResidual = 0;

            // Encontre a aresta correspondente no grafo residual
            for (const auto& edgeResidual : grafoResidual[v1]) {
                if (edgeResidual.first == v2) {
                    pesoResidual = edgeResidual.second;
                    break;
              }
          }

          // O fluxo é o peso original menos o peso residual
          float fluxo = pesoOriginal - pesoResidual;
          //cout << "O fluxo da aresta " << v1 << " para " << v2 << " é " << fluxo << endl;
        }
    }


    // Retornar o fluxo máximo encontrado
    return fluxoMaximo;
}

int main() {
    ifstream archive;
    string myText;
    int numeroDeVertices;
    ifstream arquivo("grafo_rf_6.txt");
    // Variável para armazenar cada linha do arquivo
    string linha;
    vector<Edge> conexoes;
    getline(arquivo, linha);
    numeroDeVertices = stoi(linha);
    while (getline(arquivo, linha)){
        istringstream iss(linha);
        int v1, v2;
        float peso;
        if (iss >> v1 >> v2 >> peso){
            if (peso < 0){
                cout << "Peso Negativo";
                return 0;
            }
            conexoes.push_back({v1,v2,peso});
        }
    }
    arquivo.close();
    bool direcionado = false;
    Grafos grafo(numeroDeVertices, conexoes, direcionado);
    // Exemplo de uso
    //int num_vertices = 7;
    //vector<Edge> conexoes = {Edge(0, 1, 9.0), Edge(0, 2, 5.0), Edge(0, 3, 12.0),
                             //Edge(1, 3, 3.0), Edge(1, 2, 10.0), Edge(1, 4, 5.0),
                             //Edge(2, 4, 3.0), Edge(2, 5, 6.0), Edge(2, 6, 5.0),
                            // Edge(3, 4, 5.0), Edge(3, 5, 3.0), Edge(3, 6, 4.0),
                             //Edge(4, 5, 8.0),
                            // Edge(5, 6, 12.0)};
    
    //Grafos grafo(num_vertices, conexoes, true);

    int origem = 0;
    int destino = 1;
    double total = 0;
    float maxFlow;
    for (int i = 0; i < 5; i++){
        clock_t t0 = clock();
        //cout << "Lamentável" << endl;
        maxFlow = fordFulkerson(grafo, origem, destino);
        clock_t tf = clock();
        double time_spent = (double)(tf - t0) / CLOCKS_PER_SEC;
        total+=time_spent;
        
        
    }
    cout << "Fluxo Máximo: " << maxFlow << endl;
    cout << "tempo " << total/5 << endl;
    //float maxFlow = fordFulkerson(grafo, origem, destino);

    

    return 0;
}
