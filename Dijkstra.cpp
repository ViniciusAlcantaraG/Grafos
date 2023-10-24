#include <iostream>
#include <vector>
#include <queue>
#include <limits>
#include <fstream>
#include <sstream>
#include <string>
#include <time.h>
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
            for (vector<float> i : vetor[u]){
                if (visitado[i[0]] == 0){
                    if (dist[i[0]] > dist_atual + i[1]){
                        dist[i[0]] = dist_atual + i[1]; 
                        S.push({dist[i[0]], i[0]});
                        pai[i[0]] = u+1;
                    }
                }
            }
        }
        return make_pair(dist, pai);
    }

    vector<vector<float>> Dijkstra_2(float raiz){
        vector<float> dist;
        vector<float> pai;
        vector<vector<float>> S;
        for (int i = 0; i < number_vertices; i++){
            dist.push_back(numeric_limits<float>::infinity());
            pai.push_back(0);
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
};

int main(){
    ifstream archive;
    string myText;
    int numeroDeVertices;
    ifstream arquivo("grafo_W_4.txt");
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
            if (peso < 0){
                cout << "Peso Negativo";
                return 0;
            }
            grafo.push_back({v1,v2,peso});
        }
    }
    
    Grafo_vetor cachorrinho(numeroDeVertices, grafo);
    //float soma=0;
    //for (int i = 0; i<10;i++){
        //clock_t t0 = clock();
        //cachorrinho.Dijkstra(100);
        //clock_t tf = clock();
        //double time_spent = (double)(tf - t0) / CLOCKS_PER_SEC;
        //printf("t=%f ", time_spent);
        //soma+=time_spent;
    //}
    //cout << soma/10 << endl; 
    clock_t t0 = clock();
    pair<vector<float>, vector<int>> temporary = cachorrinho.Dijkstra(10);
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
    //for (int i = 0; i<5; i++){
    //    cout << printar[i] << "\n";
    //}
    Grafo_vetor cachorro(5, {{1,2,0.1},{2,5,0.2},{5,3,5},{3,4,0},{4,5,2.3},{1,5,1}});
    vector<int> bla = cachorro.Dijkstra(1).second;
    vector<vector<int>> caminho;
    for (int i:{19,29,39,49,59}){
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
    for (vector<int> i : caminho){
        for (int j: i){
            cout << j << " ";
        }
        cout << endl;
    }
    //for (int j: {19,29,39,49,59}){
        //for (int i:caminho[j]){
            //cout << i << " ";
        //}
        //cout << endl;
    //}
    
    return 0;
}
