# -*- coding: utf-8 -*-

class SuffixTree:
    
    def __init__(self):
        self.nodes = { 0:(-1,{}) } # root node
        self.num = 0
    
    def print_tree(self):
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0:
                print (k, "->", self.nodes[k][1]) 
            else:
                print (k, ":", self.nodes[k][0])
                
    def add_node(self, origin, symbol, leafnum = -1):
        self.num += 1
        self.nodes[origin][1][symbol] = self.num
        self.nodes[self.num] = (leafnum,{})
        
    def add_suffix(self, p:str, sufnum:int):
        """ Fução que permite adicionar sufixos á árvore de sufixos

        Args:
            p (string): padrão
            sufnum (int): posição da folha correspondente ao sufixo da sequencia original

        Returns:
            None
        """
        node = 0
        for i in range(len(p)):
            caracter = p[i]
        if caracter not in self.nodes[node][1]:
            self.add_node(node, caracter)
        node = self.nodes[node][1][caracter]
        self.add_leaf(node, sufnum)
        return None
    
    def suffix_tree_from_seq(self, text:str):
        """ Função usada para criar a árvore de sufixos apartir da string text.

        Args:
            text (string): String pela qual se construirá a árvore de sufixos
        """
        t = text+"$"
        for i in range(len(t)): #Divide o texto
            self.add_suffix(t[i:], i) # nº de seq. que são adicionadas à àrvore
            
    def find_pattern(self, pattern:str)->list[]:
        '''
        Procura padrões na trie. 
        Se o padrão for encontrado, as leaves embaixo do node são devolvidas pelo self.get_leafes_below().
        Caso contrario, a procura falha, retorna None. 
     
        Ars:
        pattern (str) 
        
        Returns:
        Lista (list) de posições dos padrões ocorridos ou None se não houver matches.
        '''
        pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():
                node = self.nodes[node][1][pattern[pos]]
            else: return None
        return self.get_leafes_below(node)
        

    def get_leafes_below(self, node:int)->list[]:
        '''
        Coleciona as leaves à baixo de node expecifico.
        
        Args:
        node (int)
        
        Returns:
        Lista (list) das leaves a baixo do node.
        
        '''
        res = []
        if self.nodes[node][0] >=0: 
            res.append(self.nodes[node][0])            
        else:
            for k in self.nodes[node][1].keys():
                newnode = self.nodes[node][1][k]
                leafes = self.get_leafes_below(newnode)
                res.extend(leafes)
        return res

def test():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    print (st.find_pattern("TA"))
    print (st.find_pattern("ACG"))

def test2():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    print (st.find_pattern("TA"))
    print(st.repeats(2,2))

test()
print()
test2()

import unittest

class TestStringMethods(unittest.TestCase):
    def test_trie(self):
        seq="ACGTAAG"
        st= SuffixTree()
        st.suffix_tree_from_seq(seq)
        self.assertEqual(st.find_pattern("AC"),[0])
        self.assertEqual(st.find_pattern("TAA"),[3])
        self.assertIsNone(st.find_pattern("CC"))
        self.assertIsNone(st.find_pattern("CGA"))
    if __name__ == '_main_':
            unittest.main()
            
    
    
