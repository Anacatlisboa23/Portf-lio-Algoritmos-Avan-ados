# -*- coding: utf-8 -*-

class BWT:

    """Classe que implementa o algoritmo Burrows-Wheeler Transform (BWT)
     que é responsável por produzir uma nova sequência a partir de uma sequência original de caracteres.
    """
    def __init__(self, seq = "", buildsufarray = False):
        """
        Inicializa a classe com uma determinada entrada de texto.

        Args:
            texto (str): O texto que será transformado.

        Atributos:
            text (str): O texto a ser transformado.
            bwt (str): A transformação Burrows-Wheeler do texto de entrada.
            c (dict): O dicionário de contagem para cada carácter no texto de entrada.
            first_col (str): A primeira coluna da Transformada Burrows-Wheeler.
            last_to_first (list): Do último ao primeiro mapeamento para cada caracterer presente na primeira coluna.

        """
        self.bwt = self.build_bwt(seq, buildsufarray) 
        
    def set_bwt(self, bw):
        self.bwt = bw

    def build_bwt(self, text:str, buildsufarray = False)->str:
        """
        Constroi Burrows-Wheeler Transform apartir de um determinado texto.

        Args:
            text (str): O texto que será transformado.

        Returns:
            str: Burrows-Wheeler Transform do texto.
        """

        ls = []
        if buildsufarray:
            sa = []
            # implementar algoritmo para construir sufix array
        else:
            sa = sorted(range(len(text)), key=lambda x: text[x:])
        for i in sa:
            if i == 0:
                ls.append('$')
            else:
                ls.append(text[i-1])
        return ''.join(ls)
    
    def inverse_bwt(self)->str:
        """
        Descodifica Burrows-Wheeler  Transform para gerar o texto original.

        Args:
            bwt (str): A Transformada Burrows-Wheeler a ser descodificada.

        Returns:
            str: O texto original.
        """
        firstcol = self.get_first_col()
        res = ""
        c = "$" 
        occ = 1
        for i in range(len(self.bwt)):
            c_count = self.bwt[0:i+1].count(c)
            j = self.c[ord(c)]
            i = j + c_count - occ
            res += firstcol[i]
            c = self.bwt[i]
            occ = self.bwt[0:i+1].count(c)
        return res
                 
 
    def get_first_col (self):
        """
        Retorna a 1º coluna do Burrows-Wheeler Transform.

        Returns:
            str: a 1º coluna do Burrows-Wheeler Transform.
        """

        firstcol = []
        for c in self.bwt:
             firstcol.append(c)
        firstcol.sort()
        return firstcol
        

    def last_to_first(self) -> list[]:
        """
        Retorna uma lista com os índices mostrando qual a posição que o último caractere de cada sufixo 
        ordenado de uma Burrows-Wheeler Transform ocupa na primeira coluna.

        Returns:
            list: Do último ao primeiro mapeamento para cada caracter na primeira coluna.
        """
        res = []
        for i in range(len(self.bwt)):
            c = self.bwt[i]
            occ = self.bwt[0:i+1].count(c)
            res.append(self.c[ord(c)] + occ - 1)
            return res



    def bw_matching(self, patt:list[])->list[]:
       
        lf = self.last_to_first()
        res = []
        top = 0
        bottom = len(self.bwt)-1
        flag = True
        while flag and top <= bottom:
            if patt != "":
                symbol = patt[-1]
                patt = patt[:-1]
                lmat = self.bwt[top:(bottom+1)] #considerar tudo nos 2 marcadores, o +1 é pq o python não conta com a ultima letra
                if symbol in lmat:
                    topIndex = lmat.index(symbol) + top
                    bottomIndex = bottom - lmat[::-1].index(symbol)
                    top = lf[topIndex]
                    bottom = lf[bottomIndex]
                else: flag = False
            else: 
                for i in range(top, bottom+1): res.append(i)
                flag = False            
        return res        
 
    def bw_matching_pos(self, patt:list[])->list[]: 
        """
        Retorna a posição inicial de cada ocorrência de um dado padrão no Burrows-Wheeler Transform.

        Arg:
            padrão (str): O padrão a ser pesquisado.

        Returns:
            list: A lista das posições de partida do padrão.
        """
        res = []
        matches = self.bw_matching(patt)
        for m in matches:
            res.append(self.sa[m])
        res.sort()
        return res
# auxiliary
 
        def find_ith_occ(l,elem,index): #qual a posição de index ...
            j,k = 0,0
            while k < index and j < len(l):
                if l[j] == elem:
                    k = k +1
                    if k == index: return j
                    j += 1
                return -1

import unittest


class TestBWT(unittest.TestCase):
    def test_bwt(self):
        seq = "TAGACAGAGA$"
        bw = BWT(seq)
        self.assertEqual(bw.bwt, "AGGGTT$AAAAC")


    def test_inverse_bwt(self):
        bw = BWT("")
        bw.set_bwt("ACG$GTAAAAC")
        self.assertEqual(bw.inverse_bwt(), "ACTAGCAAAA$G")

    def test_sa(self):
        seq = "TAGACAGAGA$"
        bw = BWT(seq, True)
        self.assertEqual(bw.sa, [10, 8, 5, 2, 0, 7, 6, 4, 1, 9, 3])

    def test_bw_matching_pos(self):
        seq = "TAGACAGAGA$"
        bw = BWT(seq, True)
        self.assertEqual(bw.bw_matching_pos("AGA"), [2, 6])        

if  __name__ == '__main__':
        unittest.main()


def test():
    seq = "TAGACAGAGA$"
    bw = BWT(seq)
    print (bw.bwt)
#    print (bw.last_to_first())
#    print (bw.bw_matching("AGA"))


def test2():
    bw = BWT("")
    bw.set_bwt("ACG$GTAAAAC")
    print (bw.inverse_bwt())

def test3():
    seq = "TAGACAGAGA$"
    bw = BWT(seq, True)
    print("Suffix array:", bw.sa)
#    print(bw.bw_matching_pos("AGA"))

test()
#test2()
#test3()

