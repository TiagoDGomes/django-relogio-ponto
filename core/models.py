# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from pyRelogioPonto.relogioponto.base import get_rep_suportados, \
                                Colaborador as ColaboradorREP
from core.util import somente_numeros
from django.core.exceptions import ObjectDoesNotExist
from pprint import pprint


class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    pis = models.CharField(max_length=25, unique=True, verbose_name='PIS')
    verificar_digital = models.BooleanField(default=True, null=False, blank=False)
    
    class Meta:
        verbose_name_plural = 'colaboradores'
        ordering = ('nome',)
           
    def __str__(self):
        return "{0} ({1})".format(self.nome, self.pis)
    
    def salvar_em_relogios(self, relogios=[]):
        if not relogios:
            relogios = RelogioPonto.objects.all()

        
        for relogio in relogios:
            rep =  relogio.get_rep() 
            try:               
                colREP = rep.colaboradores.filter(pis=self.pis)[0]
                if not colREP:
                    colREP = ColaboradorREP(rep)
            except:
                colREP = ColaboradorREP(rep)
            colREP.nome = self.nome
            colREP.pis = self.pis
            colREP.verificar_digital = self.verificar_digital
            colREP.matriculas = [] 
            for m in self.matriculas.all():
                colREP.matriculas.append(int(m.numero))
            print colREP.matriculas
            colREP.save()
    
    
    
class Matricula(models.Model):
    colaborador = models.ForeignKey(Colaborador, related_name='matriculas')
    numero = models.IntegerField(verbose_name='número',)   
               
    def __str__(self):
        return "Matricula %s de %s" % (str(self.numero) , self.colaborador)
    

    
    
class RelogioPonto(models.Model):      
    
    CHOICES_TIPOS_RELOGIOS = [(id, nome) for id, nome, tipo, parametros in get_rep_suportados()]  
    nome = models.CharField(max_length=30)
    tipo = models.IntegerField(choices=CHOICES_TIPOS_RELOGIOS)
    ativo = models.BooleanField(default=True)
    _rep = None

    
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
            for id_, _, __, parametros in get_rep_suportados():
                if self.tipo == id_:
                    for propriedade, tipo_valor in parametros:
                        parametro = Parametro()
                        parametro.propriedade =  propriedade
                        parametro.tipo = tipo_valor
                        parametro.relogio = self
                        parametro.save()
            parametro = Parametro()
            parametro.propriedade =  'ultimo_nsr'
            parametro.tipo = int
            parametro.relogio = self
            parametro.valor = 0
            parametro.save()
        return s
    
    def get_rep(self):
        if not self._rep: # se não foi definido            
            for id_, _, RelogioPontoDevice, parametros in get_rep_suportados():
                if self.tipo == id_: # se mesmo modelo
                    plist = []                     
                    for propriedade, tipo_valor in parametros:
                        for parametro_local in self.parametros.all():
                            if parametro_local.propriedade == propriedade: 
                                if tipo_valor == int :
                                    plist.append(propriedade + '=' + parametro_local.valor)
                                else:    
                                    plist.append(propriedade + '="' + parametro_local.valor + '"')
                    cmd = 'self._rep = RelogioPontoDevice(%s)' % ",".join(plist)                    
                    exec cmd
        return self._rep
    
    def atualizar_registros(self, force=False):
        ultimo_nsr = self.parametros.get_or_create(propriedade='ultimo_nsr')[0] 
        relogio_rep = self.get_rep()
        if not force:
            registros = relogio_rep.get_registros(nsr=int('0'+ultimo_nsr.valor)+1)
        elif self.ativo:
            registros = relogio_rep.get_registros()

        for registro in registros:            
            if registro['tipo'] == 3:                
                pis = str(int(somente_numeros(registro['colaborador'].pis)))
                data_hora = registro['data_marcacao']
                try:                        
                    colaborador = Colaborador.objects.get(pis=pis)
                    novo_registro = RegistroPonto.objects.get_or_create(relogio=self,
                                                                        colaborador=colaborador,
                                                                        data_hora=data_hora,
                                                                        )[0]
                    novo_registro.save()
                except ObjectDoesNotExist:
                    pass
                
        
        ultimo_nsr.valor = relogio_rep.quantidade_eventos_registrados
        ultimo_nsr.save() 
        return registros           
     


class Parametro(models.Model):
    propriedade = models.CharField(max_length=25, editable=False)
    valor = models.CharField(max_length=100)
    tipo = models.CharField(max_length=25, default='str', editable=False)
    relogio = models.ForeignKey(RelogioPonto,verbose_name='relógio', related_name='parametros')
    
    def __str__(self):
        return self.propriedade

    class Meta:
        verbose_name = 'parâmetro'  
        unique_together = (('relogio','propriedade'),)
        
         

class RegistroPonto(models.Model):
    relogio = models.ForeignKey(RelogioPonto,verbose_name='relógio')
    colaborador = models.ForeignKey(Colaborador, related_name='registros')
    data_hora = models.DateTimeField(verbose_name='data do registro')
    exportado = models.BooleanField(default=False, verbose_name='registro exportado')
    
    class Meta:
        verbose_name = 'registro de ponto'
        verbose_name_plural = 'registros de ponto'
    
    
    def __str__(self):
        return "{nome} ({pis}): {batida}".format(
                                                  batida=self.data_hora.strftime('%d/%m/%Y %H:%M'), 
                                                  nome=self.colaborador.nome, 
                                                  pis=self.colaborador.pis
                                                  )
    
        
    
    def converter_em_texto(self, formato):        
        result = []
        contem_matricula = False
        for f in formato:
            if f[0] == 'matricula':
                contem_matricula = True
                break                
        
        if contem_matricula: # Se contiver matrícula, é preciso gerar registro por cada matrícula
            for matricula in self.colaborador.matriculas.all(): # 
                linha = self._converter_registro_em_texto(formato, 
                                                 matricula=matricula.numero,
                                                 pis=self.colaborador.pis,
                                                 datahora=self.data_hora,       
                                                ) 
                result.append(linha)
                            
            return "\n".join(result) 
                     
        else:
            return self._converter_registro_em_texto(formato,
                                                 pis=self.colaborador.pis,
                                                 datahora=self.data_hora,   
                                                 )  
        
              
         
    
    def _converter_registro_em_texto(self, params=[], matricula=None, pis=None, datahora=None):        
        res = []
        for p in params:
            param_nome = p[0] 
            try:      
                param_valor = p[1]
            except:
                param_valor = None 
                  
            valor = ''                 
            if param_nome == 'matricula':         
                valor = str(matricula).zfill(param_valor)                    
            elif param_nome == 'pis':
                pis = somente_numeros(pis)
                valor = str(pis).zfill(param_valor)                    
            elif param_nome == 'datahora':
                valor = datahora.strftime(param_valor)
            elif param_nome == 'personalizado':
                valor = param_valor
                
            res.append(valor)            

        return "".join(res) 
    

class FormatoExportacao(models.Model):
    nome = models.CharField(max_length=25)
    formato = models.CharField(max_length=100)
    
    ''' 
    
    Formatação: 
    Exemplo de formato:
       [matricula|:|15][datahora|:|%d%m%y%H%M][personalizado|:|00100100]
       
       ira gerar:
       
        [('matricula',15), 
         ('datahora', "%d%m%y%H%M"),
         ('personalizado','00100100'),
        ]       
        
    '''
    def to_python(self):
        f = self.formato.split("][")
        return f   
    
    
    
                
