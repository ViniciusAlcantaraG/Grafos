#include <iostream>
#include <vector>
#include <queue>
#include <limits>
#include <fstream>
#include <sstream>
#include <string>
using namespace std;


class Grafos{
    public: 
        int number_vertices;
        vector<vector<float>> links;
        Grafos(int n, vector<vector<float>> conexoes){
            number_vertices = n;
            links = conexoes;
        }
    
};

class Grafo_vetor: public Grafos {
    public:
        vector<vector<vector<float>>> vetor;
        Grafo_vetor(int n, vector<vector<float>> conexoes) : Grafos(n, conexoes){
            for (int i = 0; i < number_vertices; i++) {
                vetor.push_back({});  // Create an empty vector for each vertex
            }
            for (vector<float> i : links) {
                vetor[i[0]-1].push_back({i[1]-1, i[2]});
                vetor[i[1]-1].push_back({i[0]-1, i[2]});
            }
        }
    
    vector<vector<float>> Dijkstra(int raiz){
        vector<float> dist;
        vector<float> pai;
        priority_queue<pair<float,int>, vector<pair<float,int>>, greater<pair<float,int>>> S;
        for (int i = 0; i < number_vertices; i++){
            dist.push_back(numeric_limits<float>::infinity());
            pai.push_back(0);
        }
        dist[raiz-1] = 0;
        S.push({0, raiz-1});
        while(!S.empty()){
            int u = S.top().second;
            float dist_atual = S.top().first;
            S.pop();
            for (vector<float> i : vetor[u]){
                if (dist[i[0]] > dist_atual + i[1]){
                    dist[i[0]] = dist_atual + i[1]; 
                    S.push({dist[i[0]], i[0]});
                    pai[i[0]] = u+1;
                }
            }
        }
        pai[raiz-1] = raiz;
        vector<vector<float>> retornar;
        retornar.push_back(dist);
        retornar.push_back(pai);
        return retornar;
    }

    vector<float> Dijkstra_2(float raiz){
        vector<float> dist;
        vector<vector<float>> S;
        for (int i = 0; i < number_vertices; i++){
            dist.push_back(numeric_limits<float>::infinity());
        }
        dist[raiz-1] = 0;
        S.push_back({0, raiz-1});
        while(!S.empty()){
            int u = 0;
            float dist_atual = numeric_limits<float>::infinity();
            int k = 0;
            for (int i = 0; i < S.size(); i++){
                if (S[i][0] < dist_atual){
                    dist_atual = S[i][0];
                    u = S[i][1];
                    k = i;
                }
            }
            S.erase(S.begin() + k);
            for (vector<float> i : vetor[u]){
                if (dist[i[0]] > dist_atual + i[1]){
                    dist[i[0]] = dist_atual + i[1]; 
                    S.push_back({dist[i[0]], i[0]});
                }
            }
        }
        return dist;
    }
};

int main(){
    ifstream archive;
    string myText;
    int numeroDeVertices;
    ifstream arquivo("grafo_W_1.txt");
    // Variável para armazenar cada linha do arquivo
    string linha;
    vector<vector<float>> grafo;    
    // Lê o numero de vertices na primeira linha do arquivo
    getline(arquivo, linha);
    numeroDeVertices = stoi(linha);
    while (getline(arquivo, linha)){
        istringstream iss(linha);
        float v1, v2, peso;
        if (iss >> v1 >> v2 >> peso){
            grafo.push_back({v1,v2,peso});
        }
    }
    
    Grafo_vetor cachorrinho(numeroDeVertices, grafo);
    vector<float> pais = cachorrinho.Dijkstra(10)[1];
    vector<float> blac = cachorrinho.Dijkstra(10)[0];
    vector<float> distancias;
    distancias.push_back(blac[19]);
    distancias.push_back(blac[29]);
    distancias.push_back(blac[39]);
    distancias.push_back(blac[49]);
    distancias.push_back(blac[59]);
    for (float i: distancias){
        cout << i << endl;
    }
    //for (int i = 0; i<5; i++){
    //    cout << printar[i] << "\n";
    //}
    Grafo_vetor cachorro(5, {{1,2,0.1},{2,5,0.2},{5,3,5},{3,4,0},{4,5,2.3},{1,5,1}});
    vector<float> bla = cachorro.Dijkstra(1)[1];
    vector<vector<int>> caminho;
    for (int i = 0; i < numeroDeVertices; i++){
        cout << "oi" << endl;
        int k = pais[i];
        cout << k << endl;
        vector<int> atual = {};
        atual.push_back(k);
        while(k!=10){
            k = bla[k-1];
            atual.push_back(k);
            //cout << "entrou " << k << endl;
        }
        caminho.push_back(atual);
    }
    for (vector<int> i : caminho){
        for (int j: i){
            cout << j << " ";
        }
        cout << endl;
    }
    for (int j: {19,29,39,49,59}){
        for (int i:caminho[j]){
            cout << i << " ";
        }
        cout << endl;
    }
    
    return 0;
}
