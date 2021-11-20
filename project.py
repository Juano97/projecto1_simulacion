import generador_VA_exp as gVAe
import generador_VA_normal as gVAn
import numpy as np
import sys

class Simulacion:    
    def __init__(self):
        #Variable de tiempo (tomaremos todos los tiempos del problema en minutos)
        self.T = 24*60 #1 dia
        self.t = 0
        self.t_arribo = self.t_remolcador = sys.maxsize
        self.t_muelles = [sys.maxsize,sys.maxsize,sys.maxsize] 
        self.t_entrada_muelle = [0,0,0]
        #Variables Contadoras
        self.cant_arribos = self.cant_salidas = self.cola_puerto = self.sum_tiempo_muelle = 0
        #Variables de estado0
        self.remolcador = 0
        # 0 -> esta en el puerto disponible
        # 1 -> esta en el muelle disponible 
        # 2 -> se dirige al muelle con tanquero
        # 3 -> se dirige al puerto con tanquero 
        # 4 -> se dirige al puerto sin tanquero 
        # 5 -> se dirige al muelle sin tanquero
        self.muelles = [True,True,True]
        # True -> muelle vacio
        
        
        

    def switch_remolcador(self, value):
        dic_remolcador = { 
            2 : self.suc_tras_p_m_tanq,
            3 : self.suc_tras_m_p_tanq,
            4 : self.suc_tras_m_p_rem,
            5 : self.suc_tras_p_m_rem,
            0 : self.scapegoat,
            1 : self.scapegoat
        }
        return dic_remolcador.get(value)
    
    def scapegoat(self):
        pass

    def switch_t(self, value):
        dic_t = {
            self.t_arribo: self.suc_arribo,
            min(self.t_muelles): self.suc_carga,
            self.t_remolcador : self.switch_remolcador(self.remolcador),
        }
        dic_t.get(value)()

    def simulacion_evento(self):
        self.t = self.t_arribo = gVAe.gen_VA_exp(8*60).__round__()
        while(self.t<self.T or self.cant_arribos > self.cant_salidas):
            t_min = min(self.t_arribo, self.t_remolcador, min(self.t_muelles))
            self.switch_t(t_min)
            if(t_min == sys.maxsize):
                break
        promedio = 0 if not self.cant_arribos else (self.sum_tiempo_muelle/self.cant_arribos).__round__()
        print("Entraron {} cargueros".format(self.cant_arribos))
        print("Salieron {} cargueros".format(self.cant_salidas))
        print("Promedio de tiempo de espera en muelles: {} minutos".format(promedio))



    



    def suc_arribo(self): #_lambda = 8*60
        if(self.t_arribo > self.T):
            self.t_arribo = sys.maxsize
            return
        self.t = self.t_arribo
        self.cant_arribos+=1
        self.t_arribo = self.t + gVAe.gen_VA_exp(8*60).__round__()
        if(self.muelles.__contains__(True) and self.remolcador == 0):
            self.remolcador = 2
            self.t_remolcador = self.t + gVAe.gen_VA_exp(2*60).__round__()
        else:
            self.cola_puerto+=1
        print("Arribó un barco a los: {} minutos".format(self.t))
            
        

    #trasladó desde el puerto al muelle al tanquero
    def suc_tras_p_m_tanq(self): #_lambda = 2*60
        self.t = self.t_remolcador
        # Controla si ya puso el barco que trajo en el muelle
        muelle = True
        # Controla si ya recogio un barco para llevar al puerto
        remolcador = True
        for i in range(3):
            if self.muelles[i] and muelle:
                self.t_muelles[i] = self.t + self.gen_t_carga().__round__()
                self.muelles[i] = False
                muelle = False
                self.t_entrada_muelle[i]=self.t
                if remolcador:
                    if self.cola_puerto and self.muelles.__contains__(True):
                        self.t_remolcador = self.t + gVAe.gen_VA_exp(15).__round__()
                        self.remolcador = 4
                    else:
                        self.t_remolcador = sys.maxsize
                        self.remolcador = 1
            elif self.t_muelles[i]==sys.maxsize and not self.muelles[i] and remolcador:
                self.muelles[i] = True
                self.t_remolcador = self.t + gVAe.gen_VA_exp(60).__round__()
                self.remolcador = 3
                self.sum_tiempo_muelle += (self.t - self.t_entrada_muelle[i])
                remolcador = False
        
        print("Trasladó un carguero al muelle a los: {} minutos".format(self.t))



    def suc_carga(self):
        self.t = min(self.t_muelles)
        for i in range(3):
            if self.t_muelles[i] == min(self.t_muelles):
                self.t_muelles[i] = sys.maxsize
                if self.remolcador == 1:
                    self.muelles[i]=True
                    self.remolcador = 3
                    self.sum_tiempo_muelle += (self.t - self.t_entrada_muelle[i])
                    self.t_remolcador = self.t + gVAe.gen_VA_exp(60).__round__()
                    break
        print("Un muelle terminó a los: {} minutos".format(self.t))


    #trasladó desde el muelle al puerto al carguero, remolcador == 3
    def suc_tras_m_p_tanq(self): #_lambda = 60
        self.t = self.t_remolcador
        self.cant_salidas+=1
        if self.cola_puerto:
            self.cola_puerto-=1
            self.t_remolcador = self.t + gVAe.gen_VA_exp(2*60).__round__()
            self.remolcador = 2
        else:
            if self.muelles.__contains__(False):
                self.remolcador = 5
                self.t_remolcador = self.t + gVAe.gen_VA_exp(15).__round__()
            else:
                self.remolcador = 0
                self.t_remolcador = sys.maxsize
        print("Trasladó al puerto a un carguero a los: {} minutos".format(self.t))

    #se trasladó desde el muelle al puerto el remolcador, remolcador == 4
    def suc_tras_m_p_rem(self): #_lambda = 15
        self.t = self.t_remolcador
        self.cola_puerto -= 1
        self.t_remolcador = self.t + gVAe.gen_VA_exp(2*60).__round__()
        self.remolcador = 2
        print("El remolcador fue del muelle al puerto vacío a los: {} minutos".format(self.t))

    
    #se trasladó desde el puerto al muelle el remolcador, remolcador == 5 
    def suc_tras_p_m_rem(self): #_lambda=15
        self.t = self.t_remolcador
        self.t_remolcador = sys.maxsize
        self.remolcador = 1
        for i in range(3):
            if self.muelles[i] == False and self.t_muelles[i] == sys.maxsize:
                self.muelles[i]= True
                self.t_remolcador = self.t + gVAe.gen_VA_exp(60).__round__()
                self.remolcador = 3
                self.sum_tiempo_muelle += (self.t - self.t_entrada_muelle[i])
                break
        
        print("El remolcador fue del puerto al muelle vacío a los: {} minutos".format(self.t))

    
    def gen_t_carga(self):
        ran = np.random.uniform(0,1)
        if (ran <0.25):
            t_carga = gVAn.gen_VA_normal(9,1)
        elif (ran > 0.5):
            t_carga = gVAn.gen_VA_normal(18,3)
        else:
            t_carga = gVAn.gen_VA_normal(12,2)
        return t_carga



Simulacion().simulacion_evento()