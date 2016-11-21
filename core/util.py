# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

import string

def somente_numeros(texto):
    all = string.maketrans('','')
    nodigs = all.translate(all, string.digits)
    return texto.encode('utf-8').translate(all, nodigs)
    