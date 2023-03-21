# -*- coding: utf-8 -*-

class Trie:
    
    def __init__(self):
        self.nodes = { 0:{} } # dictionary
        self.num = 0
    
    def print_trie(self):
        for k in self.nodes.keys():
            print (k, "->" , self.nodes[k]) 
    
    def add_node(self, origin, symbol):
        self.num += 1
        self.nodes[origin][symbol] = self.num
        self.nodes[self.num] = {}
    
    def add_pattern(self, p): #p=padrão
        """ Função que permite adicionar um padrão à trie.

        Argumento:
            p (string):padrão
        """
        node=0
        for position in range (len(p)):
            if p[position] not in self[node].keys():
                self.add_node(node, p[position])
                node=self.nodes[node][p[position]]


    def trie_from_patterns(self, pats): #pats: lista padrões
        """Função que permite adicionar cunjunto de padrões à trie

        Argumento:
            pats (list): lista de padrões
        """
        for p in pats:
             self.add_pattern(p)
       
    def prefix_trie_match(self, text): #text é a string que derá match contra a arvore
        pos = 0 # posição inicial
        match = "" #lista vazia 
        node = 0 #node 0, inicial
        while pos < len(text): #vai correr o text atél encontrarem os matches
            if text[pos] in self.nodes[node].keys(): #vai ver se é valido
                node= self.nodes[node][text[pos]]
                match += text[pos]
                if self.nodes[node] == {}:
                     return match
                else:
                     pos += 1
            else : return None
    
        
    def trie_matches(self, text):
        res = []
        for i in range(len(text)):
            m=self.prefix_trie_match(text[i:])
            if m!=None:res.append((i,m))
            return res
        return res
        
          
def test():
    patterns = ["GAT", "CCT", "GAG"]
    t = Trie()
    t.trie_from_patterns(patterns)
    t.print_trie()

   
def test2():
    patterns = ["AGAGAT", "AGC", "AGTCC", "CAGAT", "CCTA", "GAGAT", "GAT", "TC"]
    t = Trie()
    t.trie_from_patterns(patterns)
    print (t.prefix_trie_match("GAGATCCTA"))
    print (t.trie_matches("GAGATCCTA"))
    
test()
print()
test2()

import unittest


class TestStringMethods(unittest.TestCase):
        def test_trie(self):
            t = Trie()
            t.trie_from_patterns(['AA', 'CG'])
            text = 'CAATCAAGAATT'
            matches = t.trie_matches(text)
            expected_matches = [(1, 'AA'), (5, 'AA'), (8, 'AA')]
            self.assertEqual(matches, expected_matches)
        
if __name__ == '__main__':
    unittest.main()