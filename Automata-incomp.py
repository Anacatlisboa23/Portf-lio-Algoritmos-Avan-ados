# -*- coding: utf-8 -*-


class Automata:
    
    def __init__(self, alphabet, pattern):
        self.numstates = len(pattern) + 1
        self.alphabet = alphabet
        self.transitionTable = {}
        self.buildTransitionTable(pattern)        
    
    def buildTransitionTable(self, pattern):
        for q in range(self.numstates):
            for a in self.alphabet:
                prefix = pattern[:q] + a
                self.transition_table[(q,a)] = overlap(prefix, pattern)
       
    def printAutomata(self):
        print ("States: " , self.numstates)
        print ("Alphabet: " , self.alphabet)
        print ("Transition table:")
        for k in self.transitionTable.keys():
            print (k[0], ",", k[1], " -> ", self.transitionTable[k])
         
    def nextState(self, current, symbol):
       """ Função que calcula o próximo estado do autômato em função do estado atual e o símbolo de entrada.
            Args:
            current(int): nº inteiro que representa o estado atual do autômato.
            symbol:  caractere que representa o símbolo a ser processado.
            """
        
       for x in range(self.numstates):
            for j in self.alphabet:

            # Se simbolo é o próximo no padrão
                if(symbol == self.pattern[self.current]): 
                    self.current += 1 
                    # Avançar para o próximo estado
                    if(self.current == self.numstates):
                        self.detected = True
                        self.current = self.patternSubSequence(symbol)
                    else:
                        self.detected = False
                else:
            # Verificar se existe uma subsequência no (padrão detectato até agora+simbolo) que faça parte do padrão
                    self.current = self.patternSubSequence(symbol)
                    self.detected = False

        #ou

        return self.transitionTable.get(current,symbol)
        
    def applySeq(self, seq:str)->list[]:
        """Função que aplica uma sequência de entrada ao autômato. Retorna a sequência de estados percorridos.
            Args
            seq: uma string que representa a sequência de entrada.

            Returns: 
             list: lista de inteiros que representa a sequência de estados percorridos pelo autômato ao aplicar a sequência de entrad
            """

        q = 0
        res = [q]
        for c in seq:
            q = self.next_state(q, c)
            res.append(q)
        return res
        
    def occurencesPattern(self, text:str)->list[]:
        """Função que utiliza o autômato para buscar todas as ocorrências do padrão no texto de entrada.
        Args:
            text: uma string que representa o texto de entrada.
        Returns:
        list: lista de º inteiros que representa os índices das ocorrências do padrão no texto de entrada.
        """
        
        q = 0 
        res = []
        states = self.applySeq(text)
        c = 0                                                                  
        for i in states:
            if i == (self.numstates-1):                                        
                c += 1
                res.append(c)                                                  
            elif i != (self.numstates-1) and (c!=0):
                c+=1
        return res

def overlap(s1, s2):
    """" Função auxiliar que calcula a maior superposição entre duas cadeias.
    Args:
    s1(str): uma string que representa a primeira cadeia.
    s2(str): uma string que representa a segunda cadeia.

Returns: 
    num(int): um nº inteiro que representa a maior superposição entre as duas cadeias.
    """
    maxov = min(len(s1), len(s2))
    for i in range(maxov,0,-1):
        if s1[-i:] == s2[:i]: return i
    return 0
               
def test():
    auto = Automata("AC", "ACA")
    auto.printAutomata()
    print (auto.applySeq("CACAACAA"))
    print (auto.occurencesPattern("CACAACAA"))

test()

import unittest

class TestAutomata(unittest.TestCase):
    def test_applySeq(self):
        auto = Automata("AC", "ACA")
        self.assertEqual(auto.applySeq("CACAACAA"), [0, 1, 0, 1, 2, 0, 1, 3, 1])

    def test_occurencesPattern(self):
        auto = Automata("AC", "ACA")
        self.assertEqual(auto.occurencesPattern("CACAACAA"), [1, 4])

if __name__ == '_main_':
    unittest.main()

#States:  4
#Alphabet:  AC
#Transition table:
#0 , A  ->  1
#0 , C  ->  0
#1 , A  ->  1
#1 , C  ->  2
#2 , A  ->  3
#2 , C  ->  0
#3 , A  ->  1
#3 , C  ->  2
#[0, 0, 1, 2, 3, 1, 2, 3, 1]
#[1, 4]



