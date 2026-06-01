from bibgrafo.grafo_lista_adj_nao_dir import GrafoListaAdjacenciaNaoDirecionado
from bibgrafo.grafo_errors import *


class MeuGrafoListaAdjacenciaNaoDirecionado(GrafoListaAdjacenciaNaoDirecionado):

    def vertices_nao_adjacentes(self):
        '''
        Provê um conjunto de vértices não adjacentes no grafo.
        O conjunto terá o seguinte formato: {X-Z, X-W, ...}
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Um objeto do tipo set que contém os pares de vértices não adjacentes
        '''
        nadj = set()

        for u in range(len(self.vertices)):
            for v in range(u + 1, len(self.vertices)):
                v1 = self.vertices[u]
                v2 = self.vertices[v]

                adj = False

                for a in self.arestas:
                    aresta = self.arestas[a]
                    if  (v1 == aresta.v1 and v2 == aresta.v2) or \
                        (v1 == aresta.v2 and v2 == aresta.v1):
                        adj = True
                        break
                if not(adj):
                    nadj.add("{}-{}".format(v1.rotulo, v2.rotulo))
        return nadj

    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''
        for a in self.arestas:
            if self.arestas[a].v1 == self.arestas[a].v2:
                return True
        return False

    def grau(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError()
        grau = 0
        for a in self.arestas:
            if self.arestas[a].v1.rotulo == V:
                grau += 1
            if self.arestas[a].v2.rotulo == V:
                grau += 1
        return grau
    
    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        vistas = set()
        for a in self.arestas:
            aresta = tuple(sorted((self.arestas[a].v1.rotulo, self.arestas[a].v2.rotulo)))
            if aresta in vistas:
                return True
            vistas.add(aresta)
        return False

    def arestas_sobre_vertice(self, V):
        '''
        Provê uma lista que contém os rótulos das arestas que incidem sobre o vértice passado como parâmetro
        :param V: Um string com o rótulo do vértice a ser analisado
        :return: Uma lista os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError()
        
        arestas = set()
        for a in self.arestas:
            if(self.arestas[a].v1.rotulo == V or self.arestas[a].v2.rotulo == V):
                arestas.add(self.arestas[a].rotulo)
        return arestas

    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''
        n = len(self.vertices)
        if len(self.arestas) != (n * (n-1)) / 2:
            return False

        if self.ha_paralelas() or self.ha_laco():
            return False
        
        return True
    
    def ha_ciclo(self):
        stack = list()
        vertices = self.vertices.copy()
        arestas = list(self.arestas.values())

        while(vertices):
            stack.append(vertices.pop())

            while(stack):
                v = stack.pop()
                for a in arestas.copy():
                    v2 = False
                    if a.v1 == v:
                        v2 = a.v2
                    if a.v2 == v:
                        v2 = a.v1
                    
                    if v2:
                        if v2 in vertices:
                            stack.append(v2)
                            vertices.remove(v2)
                            arestas.remove(a)
                        else:
                            return True
        return False
    
    def eh_arvore(self):
        """
        Verifica se o grafo é uma árvore.
        :return: False se o grafo não é uma árvore, ou um conjunto com os rótulos dos vértices folhas se o grafo é uma árvore.
        """

        if not self.vertices:
            return False

        stack = list()
        vertices = self.vertices.copy()
        arestas = list(self.arestas.values())
        
        stack.append(vertices.pop())

        while(stack):
            v = stack.pop()
            for a in arestas.copy():
                v2 = False
                if a.v1 == v:
                    v2 = a.v2
                if a.v2 == v:
                    v2 = a.v1
                    
                if v2:
                    if v2 in vertices:
                        stack.append(v2)
                        vertices.remove(v2)
                        arestas.remove(a)
                    else:
                        return False

        if len(vertices):
            return False
        
        if len(self.vertices) == 1:
            return {self.vertices[0].rotulo}
            
        contagem_arestas = {v.rotulo: 0 for v in self.vertices}
        
        for a in self.arestas.values():
            contagem_arestas[a.v1.rotulo] += 1
            contagem_arestas[a.v2.rotulo] += 1
            
        folhas = {rotulo for rotulo, qtd in contagem_arestas.items() if qtd == 1}

        return folhas
    
    def eh_bipartido(self):
        """
        Verifica se o grafo é bipartido.
        :return: Um valor booleano que indica se o grafo é bipartido
        """
        cores = dict()

        for inicial in self.vertices:
            if inicial.rotulo not in cores:
                fila = [inicial]
                cores[inicial.rotulo] = True

                while(fila):
                    v = fila.pop(0)
                
                    for a in self.arestas.values():
                        v2 = False

                        if a.v1 == v:
                            v2 = a.v2
                        if a.v2 == v:
                            v2 = a.v1
                    
                        if v2:
                            if v2.rotulo not in cores:
                                cores[v2.rotulo] = not cores[v.rotulo]
                                fila.append(v2)
                                
                            elif cores[v2.rotulo] == cores[v.rotulo]:
                                return False
        return True