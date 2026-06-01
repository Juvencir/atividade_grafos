import unittest
from bibgrafo.aresta import Aresta
from bibgrafo.vertice import Vertice
from bibgrafo.grafo_errors import VerticeInvalidoError, ArestaInvalidaError
from bibgrafo.grafo_builder import GrafoBuilder
from src.meu_grafo_lista_adj_nao_dir import *

class TestGrafo(unittest.TestCase):
    def setUp(self):
        a = Vertice('A')
        b = Vertice('B')
        c = Vertice('C')
        d = Vertice('D')
        e = Vertice('E')
        f = Vertice('F')
        g = Vertice('G')
        h = Vertice('H')
        i = Vertice('I')

        self.grafo_nulo = MeuGrafoListaAdjacenciaNaoDirecionado()

        self.grafo_um_vertice = GrafoBuilder().tipo(MeuGrafoListaAdjacenciaNaoDirecionado()) \
            .vertices(1).build()
        
        self.grafo_vazio = GrafoBuilder().tipo(MeuGrafoListaAdjacenciaNaoDirecionado()) \
            .vertices(5).build()

        self.grafo_completo = GrafoBuilder().tipo(MeuGrafoListaAdjacenciaNaoDirecionado()) \
            .vertices(5).arestas(True).build()


        self.grafo_arvore = GrafoBuilder().tipo(MeuGrafoListaAdjacenciaNaoDirecionado()) \
            .vertices(9).arestas([
                Aresta('a1', a, b),
                Aresta('a2', a, c),

                Aresta('b1', b, d),
                Aresta('b2', b, e),
                Aresta('b3', c, f),

                Aresta('c1', f, g),
                Aresta('c2', f, h),
                Aresta('c3', f, i),
            ]).build()
        
        self.folhas_grafo_arvore = {'D', 'E', 'H', 'I', 'G'}
        
        self.grafo_arvore_ciclo = GrafoBuilder().tipo(MeuGrafoListaAdjacenciaNaoDirecionado()) \
            .vertices(9).arestas([
                Aresta('a1', a, b),
                Aresta('a2', a, c),

                Aresta('b1', b, d),
                Aresta('b2', b, e),
                Aresta('b3', c, f),

                Aresta('c1', f, g),
                Aresta('c2', f, h),
                Aresta('c3', f, i),

                Aresta('ciclo', c, e)
            ]).build()
        
        self.grafo_arvore_paralela = GrafoBuilder().tipo(MeuGrafoListaAdjacenciaNaoDirecionado()) \
            .vertices(9).arestas([
                Aresta('a1', a, b),
                Aresta('a2', a, c),

                Aresta('b1', b, d),
                Aresta('b2', b, e),
                Aresta('b3', c, f),

                Aresta('c1', f, g),
                Aresta('c2', f, h),
                Aresta('c3', f, i),

                Aresta('paralela', a, b)
            ]).build()

        self.grafo_arvore_desconexa = GrafoBuilder().tipo(MeuGrafoListaAdjacenciaNaoDirecionado()) \
            .vertices(9).arestas([
                Aresta('a1', a, b),
                #Aresta('a2', a, c), 

                Aresta('b1', b, d),
                Aresta('b2', b, e),
                Aresta('b3', c, f),

                Aresta('c1', f, g),
                Aresta('c2', f, h),
                Aresta('c3', f, i)
            ]).build()
        
        vertices = ['J', 'C', 'E', 'P', 'M', 'T', 'Z']
        vertices_pb = {v: Vertice(v) for v in vertices}

        self.grafo_pb = GrafoBuilder().tipo(MeuGrafoListaAdjacenciaNaoDirecionado()) \
            .vertices(vertices).arestas([
                Aresta('a1', vertices_pb['J'], vertices_pb['C']),
                Aresta('a2', vertices_pb['C'], vertices_pb['E']),
                Aresta('a3', vertices_pb['C'], vertices_pb['E']),
                Aresta('a4', vertices_pb['P'], vertices_pb['C']),
                Aresta('a5', vertices_pb['P'], vertices_pb['C']),
                Aresta('a6', vertices_pb['T'], vertices_pb['C']),
                Aresta('a7', vertices_pb['M'], vertices_pb['C']),
                Aresta('a8', vertices_pb['M'], vertices_pb['T']),
                Aresta('a9', vertices_pb['T'], vertices_pb['Z'])
            ]).build()

        self.grafo_bipartido = GrafoBuilder().tipo(MeuGrafoListaAdjacenciaNaoDirecionado()) \
            .vertices(7).arestas([
                Aresta('a1', a, e),
                Aresta('a2', b, e),
                Aresta('a3', b, f),
                Aresta('a4', c, g),
            ]).build()
        
        self.grafo_bipartido_completo = GrafoBuilder().tipo(MeuGrafoListaAdjacenciaNaoDirecionado()) \
            .vertices(7).arestas([
                Aresta('a1', a, e),
                Aresta('a2', a, f),
                Aresta('a3', a, g),

                Aresta('a4', b, e),
                Aresta('a5', b, f),
                Aresta('a6', b, g),

                Aresta('a7', c, e),
                Aresta('a8', c, f),
                Aresta('a9', c, g),

                Aresta('a10', d, e),
                Aresta('a11', d, f),
                Aresta('a12', d, g),
            ]).build()

        self.grafo_nao_bipartido = GrafoBuilder().tipo(MeuGrafoListaAdjacenciaNaoDirecionado()) \
            .vertices(7).arestas([
                Aresta('a1', a, e),
                Aresta('a2', a, f),
                Aresta('a3', b, e),
                Aresta('a4', b, f),
                Aresta('a5', c, g),

                Aresta('a6', a, b)
            ]).build()

    def test_ha_ciclo(self):
        self.assertFalse(self.grafo_nulo.ha_ciclo())
        self.assertFalse(self.grafo_vazio.ha_ciclo())
        self.assertFalse(self.grafo_um_vertice.ha_ciclo())
        self.assertTrue(self.grafo_completo.ha_ciclo())

        self.assertFalse(self.grafo_arvore.ha_ciclo())
        self.assertTrue(self.grafo_arvore_ciclo.ha_ciclo())
        self.assertTrue(self.grafo_arvore_paralela.ha_ciclo())
        self.assertFalse(self.grafo_arvore_desconexa.ha_ciclo())

        self.assertTrue(self.grafo_pb.ha_ciclo())

        self.assertFalse(self.grafo_bipartido.ha_ciclo())
        self.assertTrue(self.grafo_bipartido_completo.ha_ciclo())
        self.assertTrue(self.grafo_nao_bipartido.ha_ciclo())

    def test_eh_arvore(self):
        self.assertFalse(self.grafo_nulo.eh_arvore())
        self.assertFalse(self.grafo_vazio.eh_arvore())
        self.assertSetEqual(self.grafo_um_vertice.eh_arvore(), {self.grafo_um_vertice.vertices[0].rotulo})
        self.assertFalse(self.grafo_completo.eh_arvore())

        self.assertSetEqual(self.grafo_arvore.eh_arvore(), self.folhas_grafo_arvore)
        self.assertFalse(self.grafo_arvore_ciclo.eh_arvore())
        self.assertFalse(self.grafo_arvore_paralela.eh_arvore())
        self.assertFalse(self.grafo_arvore_desconexa.eh_arvore())

        self.assertFalse(self.grafo_pb.eh_arvore())

        self.assertFalse(self.grafo_bipartido.eh_arvore())
        self.assertFalse(self.grafo_bipartido_completo.eh_arvore())
        self.assertFalse(self.grafo_nao_bipartido.eh_arvore())

    def test_eh_bipartido(self):
        self.assertTrue(self.grafo_nulo.eh_bipartido())
        self.assertTrue(self.grafo_vazio.eh_bipartido())
        self.assertTrue(self.grafo_um_vertice.eh_bipartido())
        self.assertFalse(self.grafo_completo.eh_bipartido())

        self.assertTrue(self.grafo_arvore.eh_bipartido())
        self.assertTrue(self.grafo_arvore_ciclo.eh_bipartido())
        self.assertTrue(self.grafo_arvore_paralela.eh_bipartido())
        self.assertTrue(self.grafo_arvore_desconexa.eh_bipartido())

        self.assertFalse(self.grafo_pb.eh_bipartido())

        self.assertTrue(self.grafo_bipartido.eh_bipartido())
        self.assertTrue(self.grafo_bipartido_completo.eh_bipartido())
        self.assertFalse(self.grafo_nao_bipartido.eh_bipartido())