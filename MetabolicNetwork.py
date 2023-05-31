# -*- coding: utf-8 -*-

from MyGraph import MyGraph


class MetabolicNetwork (MyGraph):
    '''
    Classe que representa as redes metabólicas
    Args:
         network_type: Tipo de rede metabólica
         split_rev: Se a reação for reversível retorna true
    '''
    
    def __init__(self, network_type:str = "metabolite-reaction", split_rev:bool = False):
        '''
        Função que armazena as variáveis globais da classe
        '''
        MyGraph.__init__(self, {})
        self.net_type = network_type
        self.node_types = {}
        if network_type == "metabolite-reaction":
            self.node_types["metabolite"] = []
            self.node_types["reaction"] = []
        self.split_rev =  split_rev
    
    def add_vertex_type(self, v:str, nodetype:str)->None:
        '''
        Função que adiciona nós à rede metabolica
        Args:
            v: Nó que é adionado à rede metabólica
            nodetype: O tipo de nó que é adicionado (reaction ou metabolite)
        '''
        self.add_vertex(v)
        self.node_types[nodetype].append(v)
    
    def get_nodes_type(self, node_type:str)->list:
        '''
        Função que identifica os tipos de nós
        Args:
            :node_type: Tipo de nó
        Returns: Devolve os nós do tipo que escolhemos
        '''
        if node_type in self.node_types:
            return self.node_types[node_type]
        else: return None
    
        
    def convert_metabolite_net(self, gmr:'MetabolicNetwork', metabolite:str):
        '''
        Função que converte a rede metabólica (metabolite-reaction) para (metabolite-metabolite) ou (reaction-reaction)
        Args:
            gmr: Rede Metabólica
            metabolite: O tipo de nó é reaction ou metabolite
        '''
        for type_of_node in gmr.node_types[metabolite]:  # Obtém todos os metabolitos ou reações
            self.add_vertex(type_of_node)  # Adiciona o metabolito ou reação á rede
            successors = gmr.get_successors(type_of_node)  # Se o tipo de nó for (metabolite) obtém as reações de cada metabolito, Exemplo: M1 -> R1
            for s in successors:
                succesors_type_of_node = gmr.get_successors(s)  # Obtém os metabolitos de cada reação, Exemplo: R2 -> M3
                for s2 in succesors_type_of_node:  # Obtém o metabolito resultante da reação
                    if type_of_node != s2:  # Se o metabolito for diferente do metabolito da reação:
                        self.add_edge(type_of_node, s2)  # Adiciona a ligação

        
    def convert_reaction_graph(self, gmr: 'MetabolicNetwork')-> dict[str, list[str]]:
        '''
    Função que converte o grafo de reações em outro formato
    Args:
        gmr (MetabolicNetwork): Grafo de reações
    Returns:
            Dict[str, List[str]]: Grafo convertido.
        '''
        converted_graph = {}  # Initialize the converted graph
    
        for r in gmr.node_types["reaction"]:
            neighbors = []  # Initialize the list of neighbors for each reaction
        
        for metabolite in gmr.adjacency_list[r]:
            for neighbor in gmr.adjacency_list[r][metabolite]:
                if neighbor != r and neighbor not in neighbors:
                    neighbors.append(neighbor)
        
        converted_graph[r] = neighbors  # Add the reaction and its neighbors to the converted graph
    
        return converted_graph


from unittest import TestCase
from MetabolicNetwork import MetabolicNetwork

class TestMetabolicNetwork(TestCase):
    def test_type(self):
        m = MetabolicNetwork("metabolite-reaction")
        m.add_vertex_type("R1", "reaction")
        m.add_edge("M1", "R1")
        self.assertRaises(TypeError, m.check_type_error_vertex, 123, "reacao")
        self.assertRaises(TypeError, m.check_type_error_network_type, "reacao__reacao")
        self.assertRaises(TypeError, m.check_TypeError_node, ["fasf"])


from MyGraph import MyGraph
from MetabolicNetwork import MetabolicNetwork


net = MetabolicNetwork()

net.add_vertex_type("R1", "reaction")
net.add_vertex_type("M1", "metabolite")
net.add_edge("M1", "R1")

reaction_nodes = net.get_nodes_type("reaction")
metabolite_nodes = net.get_nodes_type("metabolite")


print("Reaction Nodes:", reaction_nodes)
print("Metabolite Nodes:", metabolite_nodes)