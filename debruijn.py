# -*- coding: utf-8 -*-


from MyGraph import MyGraph

class DeBruijnGraph (MyGraph):
    '''
    Esta classe representa os fragmentos (k-mers) como arcos, sendo os nós sequências 
    de tamanho k-1 correspondendo a prefixos/ sufixos destes fragmentos.
    '''
    
    def __init__(self, frags):
        MyGraph.__init__(self, {})
        self.create_deBruijn_graph(frags)

    def add_edge(self, o, d):
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        self.graph[o].append(d)

    def in_degree(self, v):
        res = 0
        for k in self.graph.keys(): 
            if v in self.graph[k]: 
                res += self.graph[k].count(v)
        return res

    def create_deBruijn_graph(self, frags):
        for seq in frags:
            suf = suffix(seq)
            self.add_vertex(suf)
            pref = prefix(seq)
            self.add_vertex(pref)
            self.add_edge(pref, suf)
        pass

    def seq_from_path(self, path):
        seq = path[0]
        for i in range(1,len(path)):
            nxt = path[i]
            seq += nxt[-1]
        return seq 
    
def suffix (seq:str)->str: 
    '''
    Função que dá o sufixo da sequência
    Args:
        seq: Sequência
    Returns:
        return: sufixo da sequência
    '''
    return seq[1:]
    
def prefix(seq:str)->str:
     '''
    Função que dá o prefixo da sequência
    Inputs:
        seq: Sequência
    Returns:
        return: prefixo da sequência
    '''
     return seq[:-1]

def composition(k:int, seq:str)->list[str]:
    res = []
    for i in range(len(seq)-k+1):
        res.append(seq[i:i+k])
    res.sort()
    return res

from unittest import TestCase
import debruijn as db

class TestDeBruijnGraph(TestCase):

    def test_seq_from_path(self):
        orig_sequence = "ATGCAATTTGTCTG"
        frags = db.composition(3, orig_sequence)
        dbgr = db.DeBruijnGraph(frags)
        self.assertIn(frags[0], orig_sequence, "O fraguemento não pertence à sequencia original")
        p = dbgr.eulerian_path()
        self.assertEqual(dbgr.seq_from_path(p), "ATGCAATGGTCTG")
        frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC",
                 "TTT"]
        dbgr = db.DeBruijnGraph(frags)
        p = dbgr.eulerian_path()
        self.assertEqual(dbgr.seq_from_path(p), "ACCATTTCATGGCATAA")

    def test_types(self):
        frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC",
                 "TTT"]
        dbgr = db.DeBruijnGraph(frags)
        self.assertRaises(TypeError, dbgr.check_frags, ["phge"])
        self.assertRaises(TypeError, dbgr.check_frags, True)
        self.assertRaises(TypeError, dbgr.check_frags, 1654)



#test2()
#print()
#test3()
    
