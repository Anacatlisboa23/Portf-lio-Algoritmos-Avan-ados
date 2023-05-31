# -*- coding: utf-8 -*-


class MyGraph:
    
    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g    

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v])

    ## get basic info

    def get_nodes(self)->list[int]:
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())
        
    def get_edges(self)->list[tuple[int,int]]: 
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v,d))
        return edges
      
    def size(self)-> tuple[int, int]:
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())
      
    ## add nodes and edges    
    
    def add_vertex(self, v:int)->None:
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''

    # Check if the vertex already exists in the graph
        if v in self.graph:
            print("Vertex", v, "already exists.")
        else:
        # Add the new vertex to the graph dictionary with an empty set as its value
            self.graph[v] = set()

    def add_edge(self, o:int, d:int):
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph ''' 
        if o not in self.graph:
            self.add_vertex(o)
        if d not in self.graph:
            self.add_certex(d)

        self.graph[o].add(d)
        self.graph[d].add(o)

    ## successors, predecessors, adjacent nodes
        
    def get_successors(self, v:int)->list[int]:
        """
    Retorna uma lista de sucessores do nó `v` no grafo.

    Arguments:
        v (int): O nó para o qual os sucessores devem ser encontrados.

    Returns:
        list: Uma lista de sucessores do nó `v`.
    """
        return list(self.graph[v])     
             
    def get_predecessors(self, v:int)->list[int]:
        """
    Retorna uma lista de predecessores do nó `v` no grafo.

    Arguments:
        v (int): O nó para o qual os predecessores devem ser encontrados.

    Returns:
        list: Uma lista de predecessores do nó `v`.
    """
        predecessors = []
        for u in self.graph:
            if v in self.graph[u]:
                predecessors.append(u)
        return predecessors
    
    def get_adjacents(self, v:int)->list[int]:
        """
    Retorna uma lista de nós adjacentes (sucessores e predecessores) do nó `v` no grafo.

    Arguments:
        v (int): O nó para o qual os nós adjacentes devem ser encontrados.

    Returns:
        list: Uma lista de nós adjacentes (sucessores e predecessores) do nó `v`.
    """
        self.get_successors(v)
        for u in self.graph:
            if v in self.graph[u]:
                self.get_successors.append(u)
        return self.get_successors
        
    ## degrees    
    
    def out_degree(self, v:int)->int:
        """
    Retorna o grau de saída do nó `v` no grafo.

    Arguments:
        v (int): O nó para o qual o grau de saída deve ser encontrado.

    Retorns:
        int: O grau de saída do nó `v`.
    """
        return len (self.graph[v])
    
    def in_degree(self, v:int)->int:
        """
    Retorna o grau de entrada do nó `v` no grafo.

    Arguments:
        v (int): O nó para o qual o grau de entrada deve ser encontrado.

    Returns:
        int: O grau de entrada do nó `v`.
    """
        in_degree = 0
        for u in self.graph:
            if v in self.graph[u]:
                in_degree += 1
        return in_degree
        
    def degree(self, v:int)->int:
        """
    Retorna o grau do nó `v` no grafo.

    Arguments:
        v (int): O nó para o qual o grau deve ser encontrado.

    Returns:
        int: O grau do nó `v`.
    """
        return self.in_degree(v) + self.out_degree(v)
        
        
    
    ## BFS and DFS searches    
    
    def reachable_bfs(self, v:int)->list[int]:
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            for elem in self.graph[node]:
                if elem not in res and elem not in l and elem != node:
                    l.append(elem)
        return res
        
    def reachable_dfs(self, v:int)->list[int]:
        """
    Realiza uma busca em largura a partir do nó `v` no grafo e retorna uma lista de nós alcançáveis.

    Arguments:
        v (int): O nó inicial para a busca em largura.

    Returns:
        list: Uma lista de nós alcançáveis a partir do nó `v`.
    """
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            s = 0
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)
                    s += 1
        return res    
    
    def distance(self, s:int, d:int)->int:
        """
    Retorna a menor distância entre os nós `s` e `d` no grafo.

    Arguments:
        s (int): O nó de origem.
        d (int): O nó de destino.

    Returns:
        int: A menor distância entre os nós `s` e `d` no grafo. Retorna None se não houver um caminho entre os nós.
    """
        if s == d:
             return 0
        visited = set()
        queue = [(s, 0)]
        while queue:
            (node, dist) = queue.pop(0)
            if node not in visited:
                visited.add(node)
                if node == d:
                    return dist
                for neighbour in self.graph[node]:
                     queue.append((neighbour, dist+1))
            return None
    
    def shortest_path(self, s:int, d:int)->list[int]:
        """
    Retorna o menor caminho entre os nós `s` e `d` no grafo.

    Arguments:
        s (int): O nó de origem.
        d (int): O nó de destino.

    Returns:
        list: Uma lista contendo o menor caminho entre os nós `s` e `d` no grafo, incluindo ambos os nós. Retorna None se não houver um caminho entre os nós.
    """
        if s == d:
            return [s]
        visited = {s}
        queue = [(s, [])]
        while queue:
            (node, path) = queue.pop(0)
            for neighbour in self.graph[node] - visited:
                if neighbour == d:
                    return path + [node, neighbour]
                else:
                    visited.add(neighbour)
                    queue.append((neighbour, path + [node]))
        return None
        
        
        
    def reachable_with_dist(self, s:int)->list[tuple[int,int]]:
        res = []
        l = [(s,0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: res.append((node,dist))
            for elem in self.graph[node]:
                if not is_in_tuple_list(l,elem) and not is_in_tuple_list(res,elem): 
                    l.append((elem,dist+1))
        return res

## cycles
    def node_has_cycle (self, v:int)->bool:
        """
        Verifica se o nó `v` possui um ciclo no grafo.

        Arguments:
            v (int): O nó a ser verificado.

        Returns:
            bool: True se o nó `v` possui um ciclo no grafo, False caso contrário.
        """
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v: return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return res

    def has_cycle(self):
        """
        Verifica se o grafo possui ciclos.

        Returns:
            bool: True se o grafo possui ciclos, False caso contrário.
        """
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): return True
        return res


def is_in_tuple_list (tl:list[tuple[int,int]], val:int)->bool:
    """
        Verifica se um valor está presente em uma lista de tuplas.

        Arguments:
            tl (list): A lista de tuplas.
            val (int): O valor a ser verificado.

        Returns:
            bool: True se o valor está presente na lista de tuplas, False caso contrário.
        """
    res = False
    for (x,y) in tl:
        if val == x: return True
    return res


import unittest

class MyGraphTests(unittest.TestCase):

    def setUp(self):
        self.gr = MyGraph({1:[2], 2:[3], 3:[2,4], 4:[2]})
        self.gr2 = MyGraph()

    def test_print_graph(self):
        self.assertEqual(self.gr.print_graph(), None)

    def test_get_nodes(self):
        self.assertEqual(self.gr.get_nodes(), [1, 2, 3, 4])

    def test_get_edges(self):
        self.assertEqual(self.gr.get_edges(), [(1, 2), (2, 3), (3, 2), (3, 4), (4, 2)])

    def test_add_vertex(self):
        self.gr2.add_vertex(1)
        self.assertIn(1, self.gr2.get_nodes())

    def test_add_edge(self):
        self.gr2.add_vertex(1)
        self.gr2.add_vertex(2)
        self.gr2.add_edge(1, 2)
        self.assertIn(2, self.gr2.get_successors(1))


if __name__ == "__main__":
    unittest.main()
