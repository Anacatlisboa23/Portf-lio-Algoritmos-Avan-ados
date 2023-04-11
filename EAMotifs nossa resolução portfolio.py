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
    """
    Class que implementa o Algoritmo Evolucionário para encontrar motifs.

    Attributes:
        motifs (MotifFinding): Objecto que fornece métodos para a leitura e processamento de sequências de ADN.
        popul (PopulReal): Objecto que representa a população de indivíduos no algoritmo evolutivo.
        popsize (int): Tamanho da população.
        numits (int): Número de iterações a realizar.
        noffspring (int): Número de iterações a realizar: O número de descendência a gerar em cada iteração.
        indsize (int): Tamanho do indivíduo

    """

    def __init__(self, popsize:int, numits:int, noffspring:int, filename:str)->None:
        """
        Inicializa o algoritmo.

        Args:
            popsize (int): Tamanho da população
            numits (int): Número de iterações
            noffspring (int): Número de filhos a serem gerados
            filename (str): Nome do arquivo que contém as sequências de DNA
        """
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = len(self.motifs)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize:int)-> None:
        """
        Função que inicia a população de individuos

        Args:
            indsize (int): Tamanho do indivíduo.
        """
       
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulInt(self.popsize, indsize,
                              maxvalue, [])

    def evaluate(self, indivs:list[])->None:
        """

        Funçaõ que avalia o fitness dos individuos na população.
       
        Args:
            indivs (list): Lista de individuos a avaliar.
        """
       
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            fit = self.motifs.score(sol)
            ind.setFitness(fit)




class EAMotifsReal (EvolAlgorithm): 
    """ O EAMotifsReal receber o tamanho da população, o nº de iterações,
      o nº de descedentes e o tamanho do individuo

      Args: 
        popsize:tamanho da população
        numits: nº de iterações
        noffspring: nº de filhos gerados em cada geração
        filename: contém o arquivo com as sequencias de DNA

      Returns: Lista com Motifs  
"""
    def __init__(self, popsize:int, numits:int, noffspring:int, filename:str)->None:
        """
        Inicializa o objeto EAMotifsReal.

        Args:
            popsize (int): Tamanho da população.
            numits (int): Número de iterações a realizar.
            noffspring (int): Número de iterações a realizar: O número de descendência a gerar em cada iteração.
            filename (str): Nome do ficheiro que contem as sequencias de DNA. 
        """
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = self.motifs.motifSize * len(self.motifs.alphabet)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize:int)->None:
        """
        Função que inicia a população de individuos

        Args:
            indsize (int): Tamanho do indivíduo.
        """
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize #+1
        self.popul = PopulReal(self.popsize, indsize,maxvalue, [])
    
    def criar_PWM (self,vetor:list[float])->list[float]:
        """
        Cria uma matrix position weight (PWM) para o vetor dado.

        Args:
            vetor (list): O vetor para criar  PWM .
        Returns:
            uma matriz 
        """
        pwm=createMatZero(len(self.motifs.alphabet),self.motifs.motifSize)
        for x in range (0,len(vetor), len (self.motifs.alphabet)):
            idxcol= x / len(self.motifs.alphabet)
            col=vetor [x:x + len(self.motifs.alphabet)]
            soma=sum(col)
            for c in range (len(self.motifs.alphabet)):
                self.pwm[c][idxcol]=col[c]/soma
        return pwm
                
    def evaluate(self, indivs:list[])->None:
        """

        Funçaõ que avalia o fitness dos individuos na população.
       
        Args:
            indivs (list): Lista de individuos a avaliar.
        """
        for ind in indivs:
            sol = ind.getGenes()
            self.motifs.pwm = self.criar_PWM(sol)
            s = [self.motifs.mostProbableSeq(seq) for seq in self.motifs.seqs]
            fit = self.motifs.score(sol)
            ind.setFitness(fit)

import unittest
class TestStringMethods(unittest.TestCase):
    def test_run_and_printBestSolution_1(self):
        t = EAMotifsReal(50, 10, 100, "exemploMotifs.txt")
        t.run()
        self.assertIsNotNone(t.bestSolution)
        self.assertIsNotNone(t.bestScore)
        t.printBestSolution()
if __name__ == '_main_':
    unittest.main()


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


test1()
# test2()
