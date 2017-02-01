# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

import string
from django.core.exceptions import ObjectDoesNotExist

def somente_numeros(texto):
    all = string.maketrans('','')
    nodigs = all.translate(all, string.digits)
    return texto.encode('utf-8').translate(all, nodigs)

def update_afd(*args, **kwargs):
    from core import models
    for relogio_reg in models.RelogioPonto.objects.all():
        relogio_rep = relogio_reg.get_rep()
        for registro in relogio_rep.get_registros():
            if registro['tipo'] == 3:
                print registro
                pis = str(int(somente_numeros(registro['colaborador'].pis)))
                data_hora = registro['data_marcacao']
                try:                        
                    colaborador = models.Colaborador.objects.get(pis=pis)
                    novo_registro = models.RegistroPonto.objects.get_or_create(relogio=relogio_reg,
                                                                        colaborador=colaborador,
                                                                        data_hora=data_hora,
                                                                        )[0]
                    novo_registro.save()
                except ObjectDoesNotExist:
                    pass
                except Exception as e:
                    print e