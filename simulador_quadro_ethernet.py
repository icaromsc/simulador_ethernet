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
        self.tamQuadro=pream + tOri + tDes + SD + length + tDados + crc
        #algoritmo padding
        if(tDados<self.tamMinDados):
            self.padding(tDados)

        
    def crc32(self):
        return crc.crc32(self.dados)
        


    def padding(self,tDados):
        self.pad=self.tamMinDados-tDados
        print 'padding add:',self.pad
        self.dados=''.join(('',self.dados, '0' * self.pad))

            
    def exibir(self):
        print 'Quadro Ethernet: \n',' preambulo---> ',self.preambulo,'\n mac origem--->',self.macOrigem,'\n mac destino--->',self.macDestino,'\n dados---> ',self.dados,'\n CRC 32---> ',bin(self.FCS)




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
        while(True):
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

        
def segmentar(quadro):
    queue=collections.deque()
    


def aplicacao():
    print '-----------SIMULADOR QUADRO ETHERNET-----------------'
    #instancia quadro e canal 
    q=QuadroEthernet()
    canal=Meio()
    origem='00:1D:7D:B2:34:F9'
    destino='00:1D:7D:W4:86:G5'
    counter=5
    #recupera dados do usuario
    q.macOrigem=origem
    q.macDestino=destino
    tamDados=int(raw_input('informe o tamanho de dados que deseja transmitir:'))
    tempDados='x' * tamDados
    print '\n\n**************ORIGEM ',origem,' ****************\n\n'

    #faz padding

    q.dados=tempDados
    #print q.dados
    #print tempDados
    q.obterTamQuadro()
    #if q.tamQuadro>q.tamMaxDados:
        
        
    
    
    #add checksum
    q.FCS=q.crc32()
    
    
    q.exibir()

    #coloca no canal compartilhado
    canal.addQuadro(q)
    canal.transmitirQuadro()
    
    
    #instancia thread consumidor
    consumidor=ClienteDestino(destino, 'cliente destino', counter,canal)
    consumidor.start()
    
threadLock = threading.Lock()
aplicacao()
    
        
