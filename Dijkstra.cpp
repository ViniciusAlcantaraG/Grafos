#include <iostream>
#include <vector>
#include <queue>
#include <limits>
#include <fstream>
#include <sstream>
#include <string>
#include <time.h>
using namespace std;

struct Edge {
    float v1;
    float v2;
    float peso;

    Edge(float vertex1, float vertex2, float weight) : v1(vertex1), v2(vertex2), peso(weight) {}
};



class Grafos{
    public: 
        int number_vertices;
        vector<Edge> links;
        Grafos(int n, vector<Edge> conexoes){
            number_vertices = n;
            links = conexoes;
        }
    
};

class Grafo_vetor: public Grafos {
    public:
        vector<vector<pair<int, float>>> vetor; 
        Grafo_vetor(int n, vector<Edge> conexoes) : Grafos(n, conexoes){
            vetor.resize(n);
            for (const Edge& edge : links) {
                vetor[edge.v1 - 1].push_back({edge.v2 - 1, edge.peso});
                vetor[edge.v2 - 1].push_back({edge.v1 - 1, edge.peso});
            }
        }
    
    pair<vector<float>, vector<int>> Dijkstra(int raiz){
        vector<float> dist(number_vertices, numeric_limits<float>::infinity());
        vector<int> pai(number_vertices, -1);
        vector<int> visitado(number_vertices, 0);
        priority_queue<pair<float,int>, vector<pair<float,int>>, greater<pair<float,int>>> S;
        dist[raiz-1] = 0;
        S.push({0, raiz-1});
        while(!S.empty()){
            int u = S.top().second;
            float dist_atual = S.top().first;
            visitado[u] = 1;
            S.pop();
            if (dist_atual > dist[u]) continue;

            for (pair<int, float>& edge : vetor[u]){
                int neighbor = edge.first;
                float weight = edge.second;
                if (visitado[neighbor] == 0){
                    if (dist[neighbor] > dist_atual + weight){
                        dist[neighbor] = dist_atual + weight; 
                        S.push({dist[neighbor], neighbor});
                        pai[neighbor] = u+1;
                    }
                }
                //cout << "Estou aqui" << endl;
            }
        }
        return make_pair(dist, pai);
    }

    pair<vector<float>, vector<int>> Dijkstra_2(float raiz){
        vector<float> dist(number_vertices, numeric_limits<float>::infinity());
        vector<int> pai(number_vertices, -1);
        vector<vector<float>> S;
        vector<int> visitado(number_vertices, 0);
        dist[raiz-1] = 0;
        S.push_back({0, raiz-1});
        while(!S.empty()){
            int u = 0;
            float dist_atual = numeric_limits<float>::infinity();
            int k = 0;
            visitado[u] = 1;
            for (int i = 0; i < S.size(); i++){
                if (S[i][0] < dist_atual){
                    dist_atual = S[i][0];
                    u = S[i][1];
                    k = i;
                }
            }
            S.erase(S.begin() + k);
            for (pair<int, float>& edge : vetor[u]){
                int neighbor = edge.first;
                float weight = edge.second;
                if (visitado[neighbor] == 0){
                    if (dist[neighbor] > dist_atual + weight){
                        dist[neighbor] = dist_atual + weight; 
                        S.push_back({dist[neighbor], (float)neighbor});
                        pai[neighbor] = u+1;
                    }
                }
                //cout << "Estou aqui" << endl;
            }
        }
        pai[raiz-1] = raiz;
        return make_pair(dist, pai);
    }
};

int main(){
    ifstream archive;
    string myText;
    int numeroDeVertices;
    ifstream arquivo("grafo_W_4.txt");
    // Variável para armazenar cada linha do arquivo
    string linha;
    vector<Edge> grafo;    
    // Lê o numero de vertices na primeira linha do arquivo
    getline(arquivo, linha);
    numeroDeVertices = stoi(linha);
    while (getline(arquivo, linha)){
        istringstream iss(linha);
        float v1, v2, peso;
        if (iss >> v1 >> v2 >> peso){
            if (peso < 0){
                cout << "Peso Negativo";
                return 0;
            }
            grafo.push_back({v1,v2,peso});
        }
    }
    arquivo.close();
    cout << "Avarakecobra" << endl;
    Grafo_vetor cachorrinho(numeroDeVertices, grafo);

    clock_t t0 = clock();
    cout << "Lamentável" << endl;
    pair<vector<float>, vector<int>> temporary = cachorrinho.Dijkstra_2(10);
    clock_t tf = clock();
    double time_spent = (double)(tf - t0) / CLOCKS_PER_SEC;
    cout << "tempo " << time_spent << endl;
    vector<int> pais;
    vector<float> blac;
    pais = temporary.second;
    blac = temporary.first;
    vector<float> distancias;
    
    distancias.push_back(blac[19]);
    distancias.push_back(blac[29]);
    distancias.push_back(blac[39]);
    distancias.push_back(blac[49]);
    distancias.push_back(blac[59]);
    for (float i: distancias){
        cout << i << endl;
    }


    Grafo_vetor cachorro(5, {{1,2,0.1},{2,5,0.2},{5,3,5},{3,4,0},{4,5,2.3},{1,5,1}});
    vector<int> bla = cachorro.Dijkstra(1).second;
    vector<vector<int>> caminho;
    for (const int& i : {19,29,39,49,59}){
        //cout << "oi" << endl;
        int k = pais[i];
        //cout << k << endl;
        vector<int> atual = {};
        atual.push_back(k);
        while(k!=10){
            //cout << "entrou";
            k = pais[k-1];
            atual.push_back(k);
            //cout << "entrou " << k << endl;
        }
        caminho.push_back(atual);
    }
    for (const vector<int>& i : caminho){
        for (int j: i){
            cout << j << " ";
        }
        cout << endl;
    }

    
    return 0;
}
