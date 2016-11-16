import binascii as bin
import threading
import time
import random


class QuadroEthernet(object):
    '''
    Descrição: \n
        Representação em alto nivel de um quadro ethernet \n
    \n
    Atributos: \n
        preambulo: \n
        macDestino: endereço do mac destino \n
        macOrigem: endereço do mac origem \n
        tipo: \ntes
    
    
    '''
    def __init__(self):
        self.preambulo=None
        self.macDestino=None
        self.macOrigem=None
        self.tipo=None
        self.dados=None
        self.FCS=None
    





class Meio(object):
    '''classe responsavel por compartilhar um quadro entre cliente origem e destino'''
    def __main__():
        self.quadro=None
        
        
    
    def addQuadro(self,q):
        '''
        Descrição:
        função para adicionar quadro no meio compartilhado

        Utilização:
        addQuadro(q)
         
        Params:
        q: objeto QuadroEthernet a ser colocado no meio compartilhado

        Retorno:
        boolean informando se conseguiu adicionar quadro ao meio
        '''
        if self.quadro==None:
            self.quadro=q
            return True
        else:
            print 'meio esta ocupado com um quadro:'
            print self.quadro
            return False
            
            
    
    def retiraQuadro(self):
        '''
        Descrição:
        função para retirar quadro ethernet do meio compartilhado, retorna o objeto QuadroEthernet
        retirado

        Utilização:
        retiraQuadro()
         
        Retorno:
        um objeto QuadroEthernet  
        '''
        if self.quadro==None:
            print 'nao ha quadro a ser retirado'
            return None
        else:
            quadro=self.quadro
            self.quadro=None
            return quadro

class ClienteDestino(object):

    def __init__(self,mac):
        self.mac=mac
    
        
        
