# -*- coding: utf-8 -*-

from MyGraph import MyGraph


class MetabolicNetwork (MyGraph):
    '''
    Classe que representa as redes metabólicas
    Args:
         network_type: Tipo de rede metabólica
         split_rev: Se a reação for reversível retorna true
    '''
    
    def __init__(self, network_type = "metabolite-reaction", split_rev = False):
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
    
    def add_vertex_type(self, v, nodetype):
        '''
        Função que adiciona nós à rede metabolica
        Args:
            v: Nó que é adionado à rede metabólica
            nodetype: O tipo de nó que é adicionado (reaction ou metabolite)
        '''
        self.add_vertex(v)
        self.node_types[nodetype].append(v)
    
    def get_nodes_type(self, node_type):
        '''
        Função que identifica os tipos de nós
        Args:
            :node_type: Tipo de nó
        Returns: Devolve os nós do tipo que escolhemos
        '''
        if node_type in self.node_types:
            return self.node_types[node_type]
        else: return None
    
    def load_from_file(self, filename):
        '''
        Função que cria uma rede metabólica ”metabolite-reaction” (grafo bipartido)
        Args:
            :filename: Nome do Ficheiro
        '''
        rf = open(filename)
        gmr = MetabolicNetwork("metabolite-reaction")
        for line in rf:
            if ":" in line:
                tokens = line.split(":")
                reac_id = tokens[0].strip()
                gmr.add_vertex_type(reac_id, "reaction")
                rline = tokens[1]
            else: raise Exception("Invalid line:")                
            if "<=>" in rline:
                left, right = rline.split("<=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_vertex_type(reac_id+"_b", "reaction")
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id+"_b", met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_edge(met_id, reac_id+"_b")
                        gmr.add_edge(reac_id, met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
            elif "=>" in line:
                left, right = rline.split("=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(met_id, reac_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(reac_id, met_id)
            else: raise Exception("Invalid line:")    

        
        if self.net_type == "metabolite-reaction": 
            self.graph = gmr.graph
            self.node_types = gmr.node_types
        elif self.net_type == "metabolite-metabolite":
            self.convert_metabolite_net(gmr)
        elif self.net_type == "reaction-reaction": 
            self.convert_reaction_graph(gmr)
        else: self.graph = {}
        
        
    def convert_metabolite_net(self, gmr, metabolite):
        '''
        Função que converte a rede metabólica (metabolite-reaction) para (metabolite-metabolite) ou (reaction-reaction)
        Args:
            gmr: Rede Metabólica
            metabolite: O tipo de nó é reaction ou metabolite
        '''
        for tipo_de_no in gmr.node_types[metabolite]:  # Obtém todos os metabolitos ou reações
            self.add_vertex(tipo_de_no)  # Adiciona o metabolito ou reação á rede
            successors = gmr.get_successors(
                tipo_de_no)  # Se o tipo de nó for (metabolite) obtém as reações de cada metabolito, Exemplo: M1 -> R1
            for s in successors:
                succesors_tipo_de_no = gmr.get_successors(s)  # Obtém os metabolitos de cada reação, Exemplo: R2 -> M3
                for s2 in succesors_tipo_de_no:  # Obtém o metabolito resultante da reação
                    if tipo_de_no != s2:  # Se o metabolito for diferente do metabolito da reação:
                        self.add_edge(tipo_de_no, s2)  # Adiciona a ligação

        
    def convert_reaction_graph(self, gmr): 
        '''
    Função que converte o grafo de reações em outro formato
    Args:
        gmr: Grafo de reações
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

import unittest


class TestMetabolicNetwork(unittest.TestCase):
    def test_metabolite_reaction_network(self):
        m = MetabolicNetwork("metabolite-reaction")
        m.add_vertex_type("R1", "reaction")
        m.add_vertex_type("R2", "reaction")
        m.add_vertex_type("R3", "reaction")
        m.add_vertex_type("M1", "metabolite")
        m.add_vertex_type("M2", "metabolite")
        m.add_vertex_type("M3", "metabolite")
        m.add_vertex_type("M4", "metabolite")
        m.add_vertex_type("M5", "metabolite")
        m.add_vertex_type("M6", "metabolite")
        m.add_edge("M1", "R1")
        m.add_edge("M2", "R1")
        m.add_edge("R1", "M3")
        m.add_edge("R1", "M4")
        m.add_edge("M4", "R2")
        m.add_edge("M6", "R2")
        m.add_edge("R2", "M3")
        m.add_edge("M4", "R3")
        m.add_edge("M5", "R3")
        m.add_edge("R3", "M6")
        m.add_edge("R3", "M4")
        m.add_edge("R3", "M5")
        m.add_edge("M6", "R3")

        reactions = m.get_nodes_type("reaction")
        metabolites = m.get_nodes_type("metabolite")

        self.assertCountEqual(reactions, ["R1", "R2", "R3"])
        self.assertCountEqual(metabolites, ["M1", "M2", "M3", "M4", "M5", "M6"])

    def test_convert_networks(self):
        mrn = MetabolicNetwork("metabolite-reaction")
        mrn.load_from_file("example-net.txt")

        mmn = MetabolicNetwork("metabolite-metabolite")
        mmn.load_from_file("example-net.txt")

        rrn = MetabolicNetwork("reaction-reaction")
        rrn.load_from_file("example-net.txt")

        mrsn = MetabolicNetwork("metabolite-reaction", True)
        mrsn.load_from_file("example-net.txt")

        rrsn = MetabolicNetwork("reaction-reaction", True)
        rrsn.load_from_file("example-net.txt")

        # Perform assertions to test the converted networks

        self.assertEqual(len(mrn.get_nodes_type("metabolite")), 4)
        self.assertEqual(len(mrn.get_nodes_type("reaction")), 3)

        self.assertEqual(len(mmn.get_nodes_type("metabolite")), 4)
        self.assertEqual(len(mmn.get_nodes_type("metabolite-metabolite")), 4)

        self.assertEqual(len(rrn.get_nodes_type("reaction")), 3)
        self.assertEqual(len(rrn.get_nodes_type("reaction-reaction")), 3)

        self.assertEqual(len(mrsn.get_nodes_type("metabolite")), 4)
        self.assertEqual(len(mrsn.get_nodes_type("reaction")), 6)

        self.assertEqual(len(rrsn.get_nodes_type("reaction")), 6)
        self.assertEqual(len(rrsn.get_nodes_type("reaction-reaction")), 6)

if __name__ == '__main__':
    unittest.main()





