from bibgrafo.grafo_matriz_adj_dir import *
from bibgrafo.grafo_errors import *

class MeuGrafoMatrizAdjacenciaDirecionado(GrafoMatrizAdjacenciaDirecionado):

    def vertices_nao_adjacentes(self):
        '''
        Provê uma lista de vértices não adjacentes no grafo. A lista terá o seguinte formato: [X-Z, X-W, ...]
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Uma lista com os pares de vértices não adjacentes
        '''
        pass

    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''
        pass


    def grau_entrada(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        pass

    def grau_saida(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        pass

    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        pass

    def arestas_sobre_vertice(self, V):
        '''
        Provê uma lista que contém os rótulos das arestas que incidem sobre o vértice passado como parâmetro
        :param V: O vértice a ser analisado
        :return: Uma lista os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        pass

    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''
        pass

    def alcancabilidade(self):
        '''
        Provê a matriz de alcançabilidade de Warshall do grafo
        :return: Uma lista de listas preenchidas com 0s e 1s que representa a matriz de alcançabilidade de Warshall associada ao grafo
        '''

        E = list()
        n = len(self.vertices)
        
        for k in range(n):
            E.append(list())
            for m in range(n):
                if self.matriz[k][m]:
                    E[k].append(1)
                else:
                    E[k].append(0)

        for i in range(n):
            for j in range(n):
                if E[j][i] == 1:
                    for k in range(n):
                        E[j][k] = max(E[j][k], E[i][k])
        
        return E
    
    class PesoNegativoError(Exception):
        """Lançada quando o algoritmo de menor caminho encontra arestas de peso negativo"""
        pass

    def menor_caminho(self, vi, vf):
        """
        Executa o algoritmo de Dijkstra para encontrar o caminho mais curto entre dois vértices.
        :param vi: Um string com o rótulo do vértice de origem
        :param vf: Um string com o rótulo do vértice de destino
        :return: Uma lista com o custo e os vértices e arestas que formam o caminho mínimo (ex: [3.5, ['A', 'a1', 'B']])
        :raises: VerticeInvalidoError se o vértice de origem ou destino não existe no grafo
        :raises: PesoNegativoError se o grafo contém arestas de peso negativo
        """
        import heapq

        if not self.existe_rotulo_vertice(vi) or \
        not self.existe_rotulo_vertice(vf):
            raise self.VerticeInvalidoError()
            
        for _, linha in enumerate(self.matriz):
            for _, dict_arestas in enumerate(linha):
                if dict_arestas:
                    for _, aresta in dict_arestas.items():
                        if aresta.peso < 0:
                            raise self.PesoNegativoError()
        
        mapa_indices = {v.rotulo: i for i, v in enumerate(self.vertices)}
        
        distancias = {v.rotulo: float("inf") for v in self.vertices}
        distancias[vi] = 0
        queue = [(0, vi)]
        predecessores = {}
        
        while queue:
            distancia_atual, u_rotulo = heapq.heappop(queue)
            
            if distancia_atual > distancias[u_rotulo]:
                continue

            if u_rotulo == vf:
                break

            u_idx = mapa_indices[u_rotulo]
            
            for v_idx, v in enumerate(self.vertices):
                dic_arestas = self.matriz[u_idx][v_idx]
                
                if dic_arestas:
                    peso_minimo = float('inf')
                    aresta_minima = None
                    
                    for r, aresta in dic_arestas.items():
                        if aresta.peso < peso_minimo:
                            peso_minimo = aresta.peso
                            aresta_minima = r
                            
                    nova_distancia = distancia_atual + peso_minimo                    
                    if nova_distancia < distancias[v.rotulo]:
                        distancias[v.rotulo] = nova_distancia
                        predecessores[v.rotulo] = (u_rotulo, aresta_minima)
                        heapq.heappush(queue, (nova_distancia, v.rotulo))

        if distancias[vf] == float("inf"):
            return [float("inf"), []]

        menor_caminho = []
        atual = vf
        while atual != vi:
            antecessor, aresta_usada = predecessores[atual]
            menor_caminho.insert(0, atual)
            menor_caminho.insert(0, aresta_usada)
            atual = antecessor
            
        menor_caminho.insert(0, vi)
        
        return [distancias[vf], menor_caminho]