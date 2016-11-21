'''
Created on 21 de nov de 2016

@author: tiago.gomes
'''

import string

def somente_numeros(texto):
    all = string.maketrans('','')
    nodigs = all.translate(all, string.digits)
    return texto.translate(all, nodigs)
    