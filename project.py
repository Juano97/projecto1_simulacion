from typing import Match
import generador_VA_exp as gVAe
import generador_VA_normal as gVAn
import numpy as np



class Simulacion:    
    def __init__(self):
        #Variable de tiempo (tomaremos todos los tiempos del problema en minutos)
        self.T = 28800 #20 dias
        self.t = 0
        self.t_arribo = self.t_remolcador = None
        self.t_muelles = [None,None,None] 
        #Variables Contadoras
        self.cant_arribos = self.cant_ent_carg = self.cant_cargas = self.cant_sal_car = 0
        #Variables de estado0
        self.remolcador = 0
        # 0 -> esta en el puerto disponible
        # 1 -> esta en el muelle disponible 
        # 2 -> se dirige al muelle con tanquero
        # 3 -> se dirige al puerto con tanquero 
        # 4 -> se dirige al puerto sin tanquero 
        # 5 -> se dirige al muelle sin tanquero
        self.cola_puerto = 0
    

    def simulacion_evento(self):
        self.t, self.t_arribo = gVAe.gen_VA_exp(8*60)
        while(self.t<self.T):
            t_min = min(self.t_arribo, self.t_remolcador, min(self.t_muelles))
            self.switch_t(t_min)


    def switch_t(self, value):
        return{
            self.t_arribo : self.suc_arribo(),
            min(self.t_muelles) : self.suc_carga(),
        }[value]

    def suc_arribo(self): #_lambda = 8*60
        self.t = self.t_arribo
        self.cant_arribos+=1
        self.t_arribo = self.t + gVAe.gen_VA_exp(8*60)
        if(self.t_muelles.__contains__(None) and self.remolcador == 0):
            self.remolcador = 2
            self.t_remolcador = self.t + gVAe.gen_VA_exp(2*60)
        else:
            self.cola+=1
            
        

    #trasladó desde el puerto al muelle al tanquero
    def suc_tras_p_m_tanq(self): #_lambda = 2*60
        self.t = self.t_remolcador
        self.remolcador = 1
        for muelle in self.t_muelles:
            if not muelle:
                muelle = self.t + self.gen_t_carga()
        self.cant_cargas += 1
        pass

    def suc_carga(self):
        for muelle in self.t_muelles:
            if muelle == min(self.t_muelles):
                muelle = None
                
        pass

    def suc_tras_m_p_tanq(self): #_lambda = 60
        pass

    #se trasladó desde el muelle al puerto el remolcador 
    def suc_tras_m_p_rem(self): #_lambda = 15
        pass
    
    def suc_tras_p_m_rem(self): #_lambda=15
        pass
    
    def gen_t_carga():
        ran = np.random.uniform(0,1)
        if (ran <0.25):
            t_carga = gVAn.gen_VA_normal(9,1)
        elif (ran > 0.5):
            t_carga = gVAn.gen_VA_normal(12,2)
        else:
            t_carga = gVAn.gen_VA_normal(18,3)
        return t_carga

    

a = None
if not a:
    print("si")