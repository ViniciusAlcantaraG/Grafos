#include <iostream>
#include <vector>
#include <queue>
#include <limits>
#include <fstream>
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
    
    vector<float> Dijkstra(int raiz){
        vector<float> dist;
        for (int i = 0; i < vetor.size(); i++){
            cout << i << ": ";
                for (int j = 0; j < vetor[i].size(); j++){
                    for (int k = 0; k < vetor[i][j].size(); k++){
                        //cout << i << j << k << endl;
                        cout << vetor[i][j][k] << " ";
                    }
                    cout << ", ";
                }
                cout << endl;
            }
        priority_queue<pair<float,int>, vector<pair<float,int>>, greater<pair<float,int>>> S;
        for (int i = 0; i < number_vertices; i++){
            dist.push_back(numeric_limits<float>::infinity());
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
    //ifstream arquivo("grafo_1.txt");
    // Variável para armazenar cada linha do arquivo
    string linha;
    // Lê o numero de vertices na primeira linha do arquivo
    //getline(arquivo, linha);
    //numeroDeVertices = stoi(linha);
    //cout << numeroDeVertices << "\n";

    
    
    //for (int i = 0; i<5; i++){
    //    cout << printar[i] << "\n";
    //}
    Grafo_vetor cachorro(5, {{1,2,0.1},{2,5,0.2},{5,3,5},{3,4,0},{4,5,2.3},{1,5,1}});
    vector<float> bla = cachorro.Dijkstra(1);
    return 0;
}
