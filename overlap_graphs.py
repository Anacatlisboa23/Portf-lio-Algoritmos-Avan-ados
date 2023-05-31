# -*- coding: utf-8 -*-

from MyGraph import MyGraph

class OverlapGraph(MyGraph):
    
    def __init__(self, frags:list[str]):
        MyGraph.__init__(self, {})
        self.create_overlap_graph(frags)

#    def __init__(self, frags, reps = False):
#        if reps: self.create_overlap_graph_with_reps(frags)
#        else: self.create_overlap_graph(frags)
#        self.reps = reps
        
    
    ## create overlap graph from list of sequences (fragments)
    def create_overlap_graph(self, frags:list[str])->None:
         for seq in frags:
            self.add_vertex(seq)
        for g in frags:
            for f in frags:
                if suffix(g) == prefix(f): self.add_edge(g, f)
        
    def create_overlap_graph_with_reps(self, frags:list[str])->None: 
        """
        Creates an overlap graph from a list of DNA sequence fragments allowing duplicates.

        Args:
            frags: A list of DNA sequence fragments.
        """ 
        idnum = 1
        for seq in frags:
            self.add_vertex(seq + "-" + str(idnum))
        idnum = idnum + 1
        idnum = 1
        for seq in frags:
            suf = suffix(seq)
            for seq2 in frags:
                if prefix(seq2) == suf:
                    for x in self.get_instances(seq2):
                        self.add_edge(seq + "-" + str(idnum), x)
        idnum = idnum + 1
    
    def get_instances(self, seq:str)->list[str]:
        """
        Get all instances of a DNA sequence in the graph.

        Args:
            seq: A DNA sequence.

        Returns:
            A list of instances of the DNA sequence.
        """
        res = []
        for k in self.graph.keys():
            if seq in k: res.append(k)
        return res
    
    def get_seq(self, node:str)->None:
        """
        Get the DNA sequence from a node in the graph.

        Args:
            node: A node in the graph.

        Returns:
            The DNA sequence of the node if found, otherwise None.
        """
        if node not in self.graph.keys(): return None
        if self.reps: return node.split("-")[0]
        else: return node
    
    def seq_from_path(self, path):
         if len(path) == 0:

    sequence = self.get_seq(path[0])
    for i in range(1, len(path)):
        node = path[i]
        seq = self.get_seq(node)
        if seq is not None:
            suffix = seq[-1]
            sequence += suffix

    return sequence
        return seq    
   
                    
# auxiliary
def composition(k, seq):
    res = []
    for i in range(len(seq)-k+1):
        res.append(seq[i:i+k])
    res.sort()
    return res
    
def suffix (seq): 
    return seq[1:]
    
def prefix(seq):
    return seq[:-1]

  
# testing / mains
def test1():
    seq = "CAATCATGATG"
    k = 3
    print (composition(k, seq))
   
def test2():
    frags = ["ACC", "ATA", "CAT", "CCA", "TAA"]
    ovgr = OverlapGraph(frags, False)
    ovgr.print_graph()

def test3():
     frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
     ovgr = OverlapGraph(frags, True)
     ovgr.print_graph()

def test4():
    frags = ["ATA",  "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA" , "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags, True)
    path = [’ACC−2’, ’CCA−8’, ’CAT−5’, ’ATG−3’]
    print (ovgr.check_if_valid_path(path))
    print (ovgr.check_if_hamiltonian_path(path))
    path2 = [’ACC−2’, ’CCA−8’, ’CAT−5’, ’ATG−3’, ’TGG−13’, ’GGC−10’, ’GCA−9’, ’CAT−6’, ’ATT−4’, ’TTT−15’, ’TTC−14’, ’TCA−12’, ’CAT−7’, ’ATA−1’, ’TAA−11’]
    print (ovgr.check_if_valid_path(path2))
    print (ovgr.check_if_hamiltonian_path(path2))
    #print (ovgr.seq_from_path(path2))

def test5():
    frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags, True)

    path = ovgr.search_hamiltonian_path()
    print(path)
    print (ovgr.check_if_hamiltonian_path(path))
    print (ovgr.seq_from_path(path))

def test6():
    orig_sequence = "CAATCATGATGATGATC"
    frags = composition(3, orig_sequence)
    print (frags)
    ovgr = OverlapGraph(frags, True)
    ovgr.print_graph()
    path = ovgr.search_hamiltonian_path()
    print (path)
    print (ovgr.seq_from_path(path))

    import unittest

class OverlapGraphTests(unittest.TestCase):

    def test_create_overlap_graph(self):
        frags = ["ACC", "ATA", "CAT", "CCA", "TAA"]
        ovgr = OverlapGraph(frags)
        # Assert the expected vertices and edges in the graph
        self.assertEqual(len(ovgr.graph), 5)
        self.assertEqual(len(ovgr.edges), 4)
        self.assertIn("ACC", ovgr.graph)
        self.assertIn("ATA", ovgr.graph)
       
    def test_get_instances(self):
        frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
        ovgr = OverlapGraph(frags)
        instances = ovgr.get_instances("CAT")
        self.assertEqual(len(instances), 3)
        self.assertIn("CAT", instances)
        self.assertIn("CAT-6", instances)
     
if __name__ == '__main__':
    unittest.main()

   
test1()
print()
test2()
print()
#test3()
#print()
#test4()
#print()
#test5()
#print()
#test6()
