from EvolAlgorithm import EvolAlgorithm
from Popul import PopulInt, PopulReal
from MotifFinding import MotifFinding
from MyMotifs import MyMotifs


def createMatZeros(nl, nc):
    res = []
    for _ in range(0, nl):
        res.append([0]*nc)
    return res


def printMat(mat):
    for i in range(0, len(mat)):
        for j in range(len(mat[i])):
            print(f"{mat[i][j]:.3f}", end=' ')
        print()


class EAMotifsInt (EvolAlgorithm):
    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = len(self.motifs)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulInt(self.popsize, indsize,
                              maxvalue, [])

    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            fit = self.motifs.score(sol)
            ind.setFitness(fit)




class EAMotifsReal (EvolAlgorithm): 
    """ O EAMotifsReal receber o tamanho da população, o nº de iterações,
      o nº de descedentes e o tamanho do individuo

      Argumentos: 
        popsize:tamanho da população
        numits: nº de iterações
        noffspring: nº de filhos gerados em cada geração
        filename: contém o arquivo com as sequencias de DNA

      Devolve: Lista com Motifs  
"""
    def __init__(self, popsize, numits, noffspring, filename)->list:
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = self.motifs.motifSize * len(self.motifs.alphabet)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulReal(self.popsize, indsize,maxvalue, [])
    
    def criar_PWM (self,vetor):
        pwm=createMatZero(len(self.motifs.alphabet),self.motifs.motifSize)
        for x in range (0,len(vetor),self.motifs.alphabet):
            idxcol= x/ len(self.motifs.alphabet)
            col=vetor [x:x + len(self.motifs.alphabet)]
            soma=sum(col)
            for c in range (len(self.motifs.alphabet)):
                self.pwm[c][idxcol]=col[c]/soma
                
    def evaluate(self, indivs):
        for ind in indivs:
            sol = ind.getGenes()
            self.motifs.pwm = self.criar_PWM(sol)
            s = [self.motifs.mostProbableSeq(seq) for seq in self.motifs.seqs]
            fit = self.motifs.score(sol)
            ind.setFitness(fit)

import unittest
class TestStringMethods(unittest.TestCase):
    def test1():
        t=EAMotifsReal (50,10,100, "exemploMotifs.txt")
        t.run
        t.printBestSolution()
    

def test1():
    t=EAMotifsReal (50,10,100, "exemploMotifs.txt")
    t.run
    t.printBestSolution()



def test1():
    ea = EAMotifsInt(100, 1000, 50, "exemploMotifs.txt")
    ea.run()
    ea.printBestSolution()


def test2():
    ea = EAMotifsReal(100, 2000, 50, "exemploMotifs.txt", 2)
    ea.run()
    ea.printBestSolution()

if _name_ == '_main_':
    unittest.main()