# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from pyRelogioPonto.relogioponto.base import get_rep_suportados


class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    pis = models.CharField(max_length=25, unique=True, verbose_name='PIS')
    verificar_digital = models.NullBooleanField()
    
    class Meta:
        verbose_name_plural = 'colaboradores'
           

class Matricula(models.Model):
    colaborador = models.ForeignKey(Colaborador)
    numero = models.IntegerField(verbose_name='número')   
    
    
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
                print(nome, tipo)
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
    relogio = models.ForeignKey(RelogioPonto,verbose_name='relógio')
    
    def __str__(self):
        return self.propriedade

    class Meta:
        verbose_name = 'parâmetro'   
    
