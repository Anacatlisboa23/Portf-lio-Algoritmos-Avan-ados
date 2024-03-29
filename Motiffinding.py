# -*- coding: utf-8 -*-
"""
Ana Lisboa
Mariana Silva
"""

from MySeq import MySeq
from MyMotifs import MyMotifs

class MotifFinding:
    
    def __init__(self, size = 8, seqs = None):
        self.motifSize = size
        if (seqs != None):
            self.seqs = seqs
            self.alphabet = seqs[0].alfabeto()
        else:
            self.seqs = []
                    
    def __len__ (self):
        return len(self.seqs)
    
    def __getitem__(self, n):
        return self.seqs[n]
    
    def seqSize (self, i):
        return len(self.seqs[i])
    
    def readFile(self, fic, t):
        for s in open(fic, "r"):
            self.seqs.append(MySeq(s.strip().upper(),t))
        self.alphabet = self.seqs[0].alfabeto()
        
        
    def createMotifFromIndexes(self, indexes):
        pseqs = []
        for i,ind in enumerate(indexes):
            pseqs.append( MySeq(self.seqs[i][ind:(ind+self.motifSize)], self.seqs[i].tipo) )
        return MyMotifs(pseqs)
        
        
    # SCORES
        
    def score(self, s):
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts()
        mat = motif.counts
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score += maxcol
        return score
   
    def scoreMult(self, s):
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        motif.createPWM()
        mat = motif.pwm
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score *= maxcol
        return score     
       
    # EXHAUSTIVE SEARCH
       
    def nextSol (self, s):
        nextS = [0]*len(s)
        pos = len(s) - 1     
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if (pos < 0): 
            nextS = None
        else:
            for i in range(pos): 
                nextS[i] = s[i]
            nextS[pos] = s[pos]+1;
            for i in range(pos+1, len(s)):
                nextS[i] = 0
        return nextS
        
    def exhaustiveSearch(self):
        melhorScore = -1
        res = []
        s = [0]* len(self.seqs)
        while (s!= None):
            sc = self.score(s)
            if (sc > melhorScore):
                melhorScore = sc
                res = s
            s = self.nextSol(s)
        return res
     
    # BRANCH AND BOUND     
     
    def nextVertex (self, s):
        res =  []
        if len(s) < len(self.seqs): # internal node -> down one level
            for i in range(len(s)): 
                res.append(s[i])
            res.append(0)
        else: # bypass
            pos = len(s)-1 
            while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
                pos -= 1
            if pos < 0: res = None # last solution
            else:
                for i in range(pos): res.append(s[i])
                res.append(s[pos]+1)
        return res
    
    
    def bypass (self, s):
        res =  []
        pos = len(s) -1
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0: res = None 
        else:
            for i in range(pos): res.append(s[i])
            res.append(s[pos]+1)
        return res
        
    def branchAndBound (self):
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0]*size
        while s != None:
            if len(s) < size:
                optimScore = self.score(s) + (size-len(s)) * self.motifSize
                if optimScore < melhorScore: s = self.bypass(s)
                else: s = self.nextVertex(s)
            else:
                sc = self.score(s)
                if sc > melhorScore:
                    melhorScore = sc
                    melhorMotif  = s
                s = self.nextVertex(s)
        return melhorMotif
    
        

        
        # Gibbs sampling 


    def gibbs (self, iteration : int =100) -> list[int]: 
        """
            Algoritmo que implementa o  Gibbs Sampling, iniciando com subsequências seleccionadas aleatoriamente, 
            sendo posteriormente pontuadas contra o modelo inicial. 
            Em cada iteração, o algoritmo efectua uma pesquisa local, 
            decidindo probabilisticamente se um dos motifs deve ser actualizado.

        Argumento: 
            iteration: nº de iterações
        Devolve:
             lista de Motifs 

        """
        from random import randint
        from random import random

         #Escolher posições iniciais de forma aleatória
        startpos = [random.randint(0, self.seqSize(x)-self.motifSize)
                    for x in range(len(self.seqs))]
        bestMotifs = startpos[:]
        bestMotifsScore=self.scoreMult(startpos)
        time_last_improvement=0 

        while time_last_improvement< iteration:
             time_last_improvement += 1

             #Escolher aleatoriamente uma sequência 
             for x in range(iteration):  
                i = random.randint(0,len(self.seqs)-1)
                startpos.pop(i)
                outraseq=self.seqs.pop(i) 
                perfil=self.createMotifFromIndexes(startpos) 
                perfil.create_PWM() 
                self.seqs.insert(i,outraseq) 

                #vamos ver a probabilidade das subsquencias possiveis na sequencia que foi removida
                probabilidades=perfil.probAllPositions(self.seqs[outraseq]) 
                roul=self.roulette(probabilidades) 
                startpos.insert(i,roul)
                score= self.scoreMult(startpos)
                if score> bestMotifsScore: 
                    bestMotifsScore = score
                    bestMotifs = list(startpos)
                    time_last_improvement=0
        return bestMotifs


    def roulette(self, f):
        from random import random
        tot = 0.0
        for x in f: tot += (0.01+x)
        val = random()* tot
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        return ind-1

# tests
import unittest
from unittest import TestCase
from MySeq import MySeq

class TestStringMethods(unittest.TestCase):
    def test_gibbs(self):
        motif = MotifFinding()
        motif.readFile("exemploMotifs.txt","dna")
        self.assertEqual(type(motif.gibbs()), list)

    def test1():  
        sm = MotifFinding()
        sm.readFile("exemploMotifs.txt","dna")
        sol = [25,20,2,55,59]
        sa = sm.score(sol)
        print(sa)
        scm = sm.scoreMult(sol)
        print(scm)

    def test2():
        print ("Test exhaustive:")
        seq1 = MySeq("ATAGAGCTGA","dna")
        seq2 = MySeq("ACGTAGATGA","dna")
        seq3 = MySeq("AAGATAGGGG","dna")
        mf = MotifFinding(3, [seq1,seq2,seq3])
        sol = mf.exhaustiveSearch()
        print ("Solution", sol)
        print ("Score: ", mf.score(sol))
        print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

        print ("Branch and Bound:")
        sol2 = mf.branchAndBound()
        print ("Solution: " , sol2)
        print ("Score:" , mf.score(sol2))
        print("Consensus:", mf.createMotifFromIndexes(sol2).consensus())
    
        print ("Heuristic consensus: ")
        sol1 = mf.heuristicConsensus()
        print ("Solution: " , sol1)
        print ("Score:" , mf.score(sol1))

    def test3():
        mf = MotifFinding()
        mf.readFile("exemploMotifs.txt","dna")
        print ("Branch and Bound:")
        sol = mf.branchAndBound()
        print ("Solution: " , sol)
        print ("Score:" , mf.score(sol))
        print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

    def test4():
        mf = MotifFinding()
        mf.readFile("exemploMotifs.txt","dna")
        print("Heuristic stochastic")
        sol = mf.heuristicStochastic()
        print ("Solution: " , sol)
        print ("Score:" , mf.score(sol))
        print ("Score mult:" , mf.scoreMult(sol))
        print("Consensus:", mf.createMotifFromIndexes(sol).consensus())
    
        sol2 = mf.gibbs(1000)
        print ("Score:" , mf.score(sol2))
        print ("Score mult:" , mf.scoreMult(sol2))

if _name_ == '_main_':
    unittest.main()
