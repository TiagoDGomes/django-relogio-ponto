# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from pprint import pprint
from core.util import somente_numeros
import after_response
from django.core.exceptions import ObjectDoesNotExist


@after_response.enable
def update_afd(*args, **kwargs):
    from core import models

    while True:   
        for relogio_reg in models.RelogioPonto.objects.all():
            pprint(relogio_reg)
            relogio_rep = relogio_reg.get_rep()
            pprint(relogio_rep)
            for registro in relogio_rep.get_registros():
                if registro['tipo'] == 3:
                    print registro
                    pis = str(int(somente_numeros(registro['colaborador'].pis)))
                    pprint(pis)
                    data_hora = registro['data_marcacao']
                    try:                        
                        colaborador = models.Colaborador.objects.get(pis=pis)
                        novo_registro = models.RegistroPonto.objects.get_or_create(relogio=relogio_reg,
                                                                            colaborador=colaborador,
                                                                            data_hora=data_hora,
                                                                            )[0]
                        novo_registro.save()
                        pprint(registro)
                    except ObjectDoesNotExist:
                        pass
                    except Exception as e:
                        print e
        time.sleep(600)