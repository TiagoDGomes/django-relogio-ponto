# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
import string
from datetime import datetime


def somente_numeros(texto):
    all = string.maketrans('','')
    nodigs = all.translate(all, string.digits)
    return texto.encode('utf-8').translate(all, nodigs)

def update_afd(*args, **kwargs):
    from core import models
    registros_all = []
    for relogio_reg in models.RelogioPonto.objects.all():
        registros_all.append(relogio_reg.atualizar_registros())        
    return registros_all



def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    if isinstance(obj, str):
        return obj
    return str(obj)
    #raise TypeError ("Type not serializable: %s" % type(obj))
            
        