import binascii as crc
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
        self.preambulo='10101010'
        self.macDestino=None
        self.macOrigem=None
        self.tamQuadro=0
        self.dados=None
        self.FCS=None
        self.pad=0
        self.tamMin=64
        self.tamMax=1500


    def obterTamQuadro(self):
        #gera tamanhos para o cabeçalho do quadro
        pream=7
        tOri=random.randint(2,6)
        tDes=random.randint(2,6)
        SD=1
        length=2
        tDados=len(self.dados)
        crc=4
        self.tamQuadro=pream + tOri + tDes + SD + length + tDados + crc
        #algoritmo padding
        if(self.tamQuadro<self.tamMin):
            self.padding()

        
    def crc32(self):
        return crc.crc32(self.dados)
        
    
    def padding(self):
        self.pad=self.tamMin-self.tamQuadro

            
    def exibir(self):
        print 'Quadro Ethernet: \n',' preambulo---> ',self.preambulo,'\n mac destino--->',self.macDestino,'\n mac origem--->',self.macOrigem,'\n dados---> ',self.dados




class Meio(object):
    '''classe responsavel por compartilhar um quadro entre cliente origem e destino'''
    def __init__(self):
        self.quadro=None

        
    def ocupado(self):
        return self.quadro!=None

    
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


    def transmitirQuadro(self):
        chance=random.randint(0, 1)
        if chance==1:
            print 'houve ruido durante a transmissão do quadro'
            self.__geraRuido()


    def __geraRuido(self):
        temp=self.quadro.dados
        pos=random.randint(0,(len(temp)-1))
        ruido=temp.replace(temp[pos],'?')
        self.quadro.dados=ruido
        #print ruido
        
        
            

class ClienteDestino(object):

    def __init__(self,mac):
        self.mac=mac
    
def aplicacao():
    print '-----------SIMULADOR QUADRO ETHERNET-----------------'
    
    #instancia quadro e canal 
    q=QuadroEthernet()
    canal=Meio()
    origem='00:1D:7D:B2:34:F9'
    destino='00:1D:7D:W4:86:G5'
    #recupera dados do usuario
    q.macOrigem=origem
    q.macDestino=destino
    q.dados=raw_input('informe a mensagem que deseja transmitir:')
    q.exibir()
    

aplicacao()
    
        
