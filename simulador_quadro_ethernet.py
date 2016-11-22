# -*- coding: utf-8 -*-
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
        tipo:
    
    
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
        self.tamMinDados=46
        self.tamMaxDados=1500


    def obterTamQuadro(self):
        #gera tamanhos para o cabeçalho do quadro
        pream=7
        #alterar para gerar tam 2 ou 6
        tOri=2
        tDes=2
        SD=1
        length=2
        tDados=len(self.dados)
        crc=4
        self.tamQuadro=pream + tOri + tDes + SD + length + crc
        #algoritmo padding
        if(tDados<self.tamMinDados):
            self.padding(tDados)
        #atualiza tamanho do quadro
        self.tamQuadro+=len(self.dados)

        
    def crc32(self):
        return crc.crc32(self.dados)
        


    def padding(self,tDados):
        self.pad=self.tamMinDados-tDados
        print 'padding add:',self.pad
        self.dados=''.join(('',self.dados, '0' * self.pad))
        #atualiza tam do quadro
        #self.tamQuadro+=len(self.dados)

            
    def exibir(self):
        print 'Quadro Ethernet: \n',' preambulo---> ',self.preambulo,'\n mac origem--->',self.macOrigem,'\n mac destino--->',self.macDestino,'\n tam quadro:',self.tamQuadro,'bytes','\n dados---> ',self.dados,'\n CRC 32---> ',bin(self.FCS)




class Meio(object):
    '''classe responsavel por compartilhar um quadro entre cliente origem e destino'''
    def __init__(self):
        self.quadro=None
        self.finish=False
        
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
        print '\n \n ****** Quadro sendo transmitido ******* \n'
        #10% de chance de ocorrer ruido
        chance=random.randint(0, 10)
        if chance==1:
            print 'houve ruido durante a transmissão do quadro'
            self.__geraRuido()
        else:
            print '---->transmissão realizada com sucesso\n'


    def __geraRuido(self):
        temp=self.quadro.dados
        pos=random.randint(0,(len(temp)-1))
        ruido=temp.replace(temp[pos],'?')
        self.quadro.dados=ruido
        #print ruido

        
        
            

class ClienteDestino(threading.Thread):
    

    def __init__(self, threadID, name, counter,canal):
        threading.Thread.__init__(self)
        self.name = name
        self.counter = counter
        self.mac=threadID
        self.canal=canal
        self.quadroRecebido=None

        
    def run(self):
        print "Starting " + self.name
        while(not self.canal.finish):
            #aguarda
            time.sleep(self.counter)
            #acessa canal
            threadLock.acquire()
            if self.canal.quadro != None :
                print '\n\n**************MEIO COMPARTILHADO****************\n\n'
                self.canal.quadro.exibir()
                print '\n\n**************DESTINO ',self.canal.quadro.macDestino,' ****************\n\n'
                #calcula CRC
                if self.canal.quadro.crc32()==self.canal.quadro.FCS:
                    print self.mac,'\n ...destino aceitou quadro'
                    print self.mac,'\n ...destino retira o quadro do canal compartilhado'
                    self.quadroRecebido=self.canal.retiraQuadro()
                    print self.mac,'\n ...quadro recebido pelo destino:\n'
                    self.quadroRecebido.exibir()
                    self.quadroRecebido=None
                else:
                    print 'erro checksum'
                    print 'destino rejeitou quadro'
                    self.canal.retiraQuadro()
                
            threadLock.release()
        print '\n\n************ finishing connection... *************\n\n'

        

def segmentar(quadro):
    quadros=[]
    origem=quadro.macOrigem
    destino=quadro.macDestino
    
    #divide os dados em blocos de ate tamMaxDados
    dif=len(quadro.dados) - quadro.tamMaxDados
    d1=quadro.dados[0:(quadro.tamMaxDados)]
    d2=quadro.dados[(quadro.tamMaxDados):quadro.tamMaxDados+dif]
    
    print '\n ****divindo quadros**** \n'

    print '\ndados q1:\n',len(d1)
    print '\ndados q2:\n',len(d2)

    #adiciona quadros na lista
    q1=QuadroEthernet()
    q1.macOrigem=origem
    q1.macDestino=destino
    q1.dados=d1
    
    q2=QuadroEthernet()
    q2.macOrigem=origem
    q2.macDestino=destino
    q2.dados=d2
    
    quadros.append(q1)
    quadros.append(q2)
    return quadros
    


def aplicacao():
    print '-----------SIMULADOR QUADRO ETHERNET-----------------'
    
    #instancia quadro e canal
    q=QuadroEthernet()
    canal=Meio()
    origem='00:1D:7D:B2:34:F9'
    destino='00:1D:7D:W4:86:G5'
    counter=2
    
    #instancia thread consumidor
    consumidor=ClienteDestino(destino, 'cliente destino', counter,canal)
    consumidor.start()

    time.sleep(3)
    #recupera dados do usuario
    q.macOrigem=origem
    q.macDestino=destino
    tamDados=int(raw_input('informe o tamanho de dados que deseja transmitir:'))
    if tamDados <2000:
        tempDados='x' * tamDados
    
    #faz padding

        q.dados=tempDados
        #print q.dados
        #print tempDados
        q.obterTamQuadro()
    
        if len(q.dados)>q.tamMaxDados:
            #segmenta envio dos quadros
            quadros=segmentar(q)
            for i in quadros:
                print '\n\n**************ORIGEM ',origem,' ****************\n\n'
                i.obterTamQuadro()
                i.FCS=i.crc32()
                i.exibir()
        #coloca no canal compartilhado
                canal.addQuadro(i)
                canal.transmitirQuadro()
                time.sleep(5)
        else:
            print '\n\n**************ORIGEM ',origem,' ****************\n\n'
            #add checksum
            q.FCS=q.crc32()
            q.exibir()

            #coloca no canal compartilhado
            canal.addQuadro(q)
            canal.transmitirQuadro()
            
        #finaliza conexao
        time.sleep(5)
        canal.finish=True
    else:
        print 'o tamanho máximo de dados eh 2000 bytes'
       
    
    
    
    
    
threadLock = threading.Lock()
aplicacao()
    
        
