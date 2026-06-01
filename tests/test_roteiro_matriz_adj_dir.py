import unittest
from bibgrafo.aresta import Aresta
from bibgrafo.vertice import Vertice
from bibgrafo.grafo_errors import VerticeInvalidoError, ArestaInvalidaError
from bibgrafo.grafo_builder import GrafoBuilder
from src.meu_grafo_matriz_adj_dir import *

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

        self.grafo_nulo = MeuGrafoMatrizAdjacenciaDirecionado()

        self.grafo_um_vertice = GrafoBuilder().tipo(MeuGrafoMatrizAdjacenciaDirecionado()) \
            .vertices(1).build()
        self.um_vertice_alcancabilidade = [[0]]

        self.grafo_vazio = GrafoBuilder().tipo(MeuGrafoMatrizAdjacenciaDirecionado()) \
            .vertices(5).build()
        self.vazio_alcancabilidade = [[0]*5]*5

        self.grafo_completo = GrafoBuilder().tipo(MeuGrafoMatrizAdjacenciaDirecionado()) \
            .vertices(5).arestas([
                ArestaDirecionada('a1', a, b, 5),
                ArestaDirecionada('a2', a, c, 2),
                ArestaDirecionada('a3', a, d, 3),
                ArestaDirecionada('a4', a, e, 14),

                ArestaDirecionada('b1', b, a, 5),
                ArestaDirecionada('b2', b, c, 6),
                ArestaDirecionada('b3', b, d, 2),
                ArestaDirecionada('b4', b, e, 8),

                ArestaDirecionada('c1', c, a, 9),
                ArestaDirecionada('c2', c, b, 10),
                ArestaDirecionada('c3', c, d, 11),
                ArestaDirecionada('c4', c, e, 5),

                ArestaDirecionada('d1', d, a, 7),
                ArestaDirecionada('d2', d, b, 14),
                ArestaDirecionada('d3', d, c, 1),
                ArestaDirecionada('d4', d, e, 12),

                ArestaDirecionada('e1', e, a, 3),
                ArestaDirecionada('e2', e, b, 11),
                ArestaDirecionada('e3', e, c, 1),
                ArestaDirecionada('e4', e, d, 6),
            ]).build()

        self.completo_alcancabilidade = [[1]*5]*5

        vertices = ['J', 'C', 'E', 'P', 'M', 'T', 'Z']
        vertices_pb = {v: Vertice(v) for v in vertices}

        self.grafo_pb = GrafoBuilder().tipo(MeuGrafoMatrizAdjacenciaDirecionado()) \
            .vertices(vertices).arestas([
                ArestaDirecionada('a1', vertices_pb['J'], vertices_pb['C'], 4),

                ArestaDirecionada('a2', vertices_pb['C'], vertices_pb['E'], 5),
                ArestaDirecionada('a3', vertices_pb['C'], vertices_pb['E'], 3),

                ArestaDirecionada('a4', vertices_pb['P'], vertices_pb['C'], 8),
                ArestaDirecionada('a5', vertices_pb['P'], vertices_pb['C'], 12),

                ArestaDirecionada('a6', vertices_pb['T'], vertices_pb['C'], 10),
                ArestaDirecionada('a7', vertices_pb['M'], vertices_pb['C'], 7),
                ArestaDirecionada('a8', vertices_pb['M'], vertices_pb['T'], 9),
                ArestaDirecionada('a9', vertices_pb['T'], vertices_pb['Z'], 6)
            ]).build()
        
        self.grafo_pb_alcancabilidade = [
            [0, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 1, 1],
            [0, 1, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0]
        ]


    def test_alcancabilidade(self):
        self.assertEqual(self.grafo_nulo.alcancabilidade(), [])

        self.assertEqual(self.grafo_um_vertice.alcancabilidade(), self.um_vertice_alcancabilidade)
        self.assertEqual(self.grafo_vazio.alcancabilidade(), self.vazio_alcancabilidade)

        self.assertEqual(self.grafo_completo.alcancabilidade(), self.completo_alcancabilidade)
        self.assertEqual(self.grafo_pb.alcancabilidade(), self.grafo_pb_alcancabilidade)

    def test_menor_caminho(self):
        self.assertEqual(self.grafo_vazio.menor_caminho('A', 'B'), [float("inf"), []])

        self.assertEqual(self.grafo_completo.menor_caminho('A', 'E'), [7, ['A', 'a2', 'C', 'c4', 'E']])

        self.assertEqual(self.grafo_pb.menor_caminho('J', 'C'), [4, ['J', 'a1', 'C']])
        self.assertEqual(self.grafo_pb.menor_caminho('M', 'Z'), [15, ['M', 'a8', 'T', 'a9', 'Z']])
