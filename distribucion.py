from project import Simulacion
import matplotlib.pyplot as plt 
import numpy as np
import sys

def grapher(rep = 500, T = 115200, cant_bars = 5):
    v_min = sys.maxsize
    v_max = 0
    values = []
    x = []
    y = [0 for i in range(cant_bars)]
    x_name = []
    values = [Simulacion(T).simulacion_evento() for value in range(rep)]
    v_max = max(values)
    v_min = min(values)
    a = ((v_max - v_min) / cant_bars).__floor__() 
    for i in range(cant_bars):
        temp_min = v_min + (a*i)
        temp_max = v_min + (a*(i+1)) if i < (cant_bars - 1) else v_max
        x.append(temp_max)
        x_name.append("{} - {} ".format(temp_min, temp_max))
    for value in values:
        for limit, i in zip(x, range(cant_bars)):
            if value < limit:
                y[i] += 1
                break
    fig = plt.figure(figsize = (10, 5))
    # creating the bar plot
    plt.bar(x_name, y, color ='maroon',
        width = 0.4)
    plt.xlabel("Promedio de Tiempo en los Muelles")
    plt.ylabel("No. de Repeticiones")
    plt.title("Simulación del Problema 2 con T = {}, en {} repeticiones".format(T, rep))
    plt.show()


        


grapher()