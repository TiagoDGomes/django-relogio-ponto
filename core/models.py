# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from pyRelogioPonto.relogioponto.base import get_rep_suportados
from collections import OrderedDict
from core.util import somente_numeros


class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    pis = models.CharField(max_length=25, unique=True, verbose_name='PIS')
    verificar_digital = models.NullBooleanField()
    
    class Meta:
        verbose_name_plural = 'colaboradores'
        ordering = ('nome',)
           
    def __str__(self):
        return "{0} ({1})".format(self.nome, self.pis)
    
    
    
class Matricula(models.Model):
    colaborador = models.ForeignKey(Colaborador, related_name='matriculas')
    numero = models.IntegerField(verbose_name='número',)   
               
    def __str__(self):
        return "Matricula %s de %s" % (str(self.numero) , self.colaborador)
    

    
    
class RelogioPonto(models.Model):      
    
    CHOICES_TIPOS_RELOGIOS = [(id, nome) for id, nome, tipo, parametros in get_rep_suportados()]  
    nome = models.CharField(max_length=30)
    tipo = models.IntegerField(choices=CHOICES_TIPOS_RELOGIOS)
    

    
    class Meta:
        verbose_name = 'relógio de ponto'
        verbose_name_plural = 'relógios de ponto'
    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        nao_salvo = False
        if not self.id:
            nao_salvo = True
        
        s = super(RelogioPonto, self).save(*args, **kwargs)
        if nao_salvo:
            for id, nome, tipo, parametros in get_rep_suportados():
                if self.tipo == id:
                    for propriedade, tipo_valor in parametros:
                        parametro = Parametro()
                        parametro.propriedade =  propriedade
                        parametro.tipo = tipo_valor
                        parametro.relogio = self
                        parametro.save()  
        return s
    
      


class Parametro(models.Model):
    propriedade = models.CharField(max_length=25, editable=False)
    valor = models.CharField(max_length=100)
    tipo = models.CharField(max_length=25, default='str', editable=False)
    relogio = models.ForeignKey(RelogioPonto,verbose_name='relógio', related_name='parametros')
    
    def __str__(self):
        return self.propriedade

    class Meta:
        verbose_name = 'parâmetro'  
        
         

class RegistroPonto(models.Model):
    relogio = models.ForeignKey(RelogioPonto)
    colaborador = models.ForeignKey(Colaborador)
    data_hora = models.DateTimeField()
    
    def __str__(self):
        return "{nome} ({pis}): {batida}".format(
                                                  batida=self.data_hora.strftime('%d/%m/%Y %H:%M'), 
                                                  nome=self.colaborador.nome, 
                                                  pis=self.colaborador.pis
                                                  )
    
        
    
    def converter_em_texto(self, formato):        
        result = ''
        contem_matricula = False
        for f in formato:
            if f[0] == 'matricula':
                contem_matricula = True
                break                
        
        if contem_matricula:
            for matricula in self.colaborador.matriculas.all():
                formato.append(('obj_matricula', matricula))
                result += self._converter_em_texto(formato)
                  
        else:
            result = self._converter_em_texto(formato)        
        
                
        return result 
    
    def _converter_em_texto(self, params):        
        result = ''
        for p in params:
            kw = p[0] 
            try:      
                param = p[1]
            except:
                param = None 
                  
            value = ''                 
            if kw == 'matricula':
                matricula = params[-1][1]               
                value = str(matricula.numero).zfill(param)                    
            elif kw == 'pis':
                pis = somente_numeros(self.colaborador.pis)
                value = str(pis).zfill(param)                    
            elif kw == 'datahora':
                value = self.data_hora.strftime(param)
            elif kw == 'personalizado':
                value = param
                
            result += value
            
        if result != '':
            result += '\n'   
        return result 
    
          
     
    
    
class PadraoExportacao(models.Model):
    parametro = models.CharField(max_length=15)
    formato = models.CharField(max_length=100, null=True, blank=True)
    tamanho = models.IntegerField(null=True, blank=True)
    
    @classmethod
    def gerar_com(cls, recurso):
        if type(recurso) == str:
            return cls.gerar_com_texto(recurso) 
        
    @classmethod        
    def gerar_com_texto(cls, texto):
        pass
    
