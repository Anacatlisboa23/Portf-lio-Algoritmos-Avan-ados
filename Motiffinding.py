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
    
    #test consensus (heuristic)
    def test_heuristic_consensus(self):
        motf = MotifFinding()
        motf.readFile("exemploMotifs.txt","dna")
        self.assertEqual(motf.heuristicConsensus(), [0, 6, 9, 27, 3])
        motf = MotifFinding()
        motf.readFile("exemploMotifs2.txt","dna")
        self.assertEqual(motf.heuristicConsensus(), [26, 4, 45, 63, 51])

    # Consensus (heuristic)
    def heuristicConsensus(self)-> list:
        '''
            Este algoritmo apresenta um elevado nº de soluções parciais em cada iteração.Selecionando o melhor resultado no final
           
       '''
        for y in range(len(self.seqs)):              # Considera apenas as 2 primeiras sequências 
            seque=(self.seqSize(y), self.seqs[0:2])  
            restante = self.seqs[2:] 
            ExhS= seque.exhaustiveSearch()           #Maximiza a função de avaliação(score)
        for i in range(len(restante)):               #Procura posições de motifs para as restantes posições
            aux = ExhS
            melhorScore = -1
            for h in range(len(restante[i])-self.motifsize):   #Para cada uma das restantes sequências,de maneira iterativa, escolher a melhor posição inicial na sequência, de modo a maximizar o score, considerando as posições anteriores fixas
                aux.append(h)
                score = self.score(aux)         
                if (score > bestScore):
                    bestScore = score
                    best_i = h
                aux.pop()
            ExhS.append(best_i)
        return ExhS
    
#test heuristic stochastic
    def test_heuristic_stochastic(self):
        moti= MotifFinding()
        moti.readFile("exemploMotifs.txt","dna")
        self.assertEqual(type(moti.heuristicStochastic()), list)
    
    # Consensus (heuristic)

    def heuristicStochastic(self)-> list:
        from random import randint
        from random import random
        '''
            Este algoritmo depende bastante das posições iniciais. Os resultados 
            podem ser melhorados se considerarmos várias ordens de apresentação das 
            sequências distintas.
            '''
        best_Score_list = []
        for x in range(1000): #Inicia com valores aleatórios todas as posições
            startpos = [random.randint(0, self.seqSize(x)-self.motifSize) for x in range(len(self.seqs))]
            motif = self.createMotifFromIndexes(startpos) #Perfil construido com todas as posições iniciais
            motif.createPWM()
            score = self.scoreMult(startpos)
            novo_score = score + 0.000001
            while score < novo_score:
                for i in range(len(startpos)): #Avalia a melhor posição inicial para cada sequência baseando-se no perfil
                    startpos[i] = motif.mostProbableSeq(self.seqs[i])
                score = novo_score #Aqui vamos verificar se houve alguma melhoria
                novo_score = self.scoreMult(startpos)
                motif = self.createMotifFromIndexes(startpos)
                motif.createPWM()
            best_Score_list.append(novo_score)

        return best_Score_list #Lista com os scores melhores encontrados
    
    # Gibbs sampling
    #test:
    from unittest import TestCase
    from MySeq import MySeq

    def test_gibbs(self):
        motif = MotifFinding()
        motif.readFile("exemploMotifs.txt","dna")
        self.assertEqual(type(motif.gibbs()), list)

        # Gibbs sampling 
        '''
            O algoritmo anteriormente demostrado pode ser melhorado introduzindo o método de Gibbs Sampling,
            sendo este mais lento, escolhendo novos segmentos de forma aleatória, aumentando assim as possibilidades
            de convergir para uma solução correta.
            '''
        

    def gibbs (self, iteration=100): 
        from random import randint
        from random import random
        startpos = [random.randint(0, self.seqSize(x)-self.motifSize) for x in range(len(self.seqs))] #Escolhe posições iniciais de forma aleatória
        bestMotifs = startpos[:]
        bestMotifsScore=self.scoreMult(startpos)
        time_last_improvement=0  # Até enquanto der para encontrar scores melhores
        while time_last_improvement< iteration:
             time_last_improvement += 1
             for x in range(iteration): #Escolhe aleatoriamente uma sequência 
                i = random.randite(0,len(self.seqs)-1) #Posição
                startpos.pop(i)
                outraseq=self.seqs.pop(i) #Indica qual a posição da sequência que foi retirada
                perfil=self.createMotifFromIndexes(startpos) 
                perfil.create_PWM() #Perfil P das sequências s
                self.seqs.insert(i,outraseq) #Adiciona a sequência que foi removida anteriormente
                probabilidades=perfil.probAllPositions(self.seqs[outraseq]) # Seleciona a posição baseada na roullette
                roul=self.roulette(probabilidades) #Cria a roleta de probabilidades
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

#test4()