# Proyecto I de Simulacion 
Juan Carlos Vázquez García C-412

Link de GitHub: https://github.com/Juano97/projecto1_simulacion

## Introducción al problema

El ejercicio escogido para implementar en este proyecto fue el ejercicio #2 de los sugeridos,
Puerto Sobrecargado (Overloaded Harbor). En éste se ha de simular el funcionamiento de un puerto y determinar el tiempo promedio que demoran los barcos en cada uno de los muelles (entrada, descarga y salida del muelle). Para su resolución será utilizado el lenguaje **python** y sus librerías **numpy** y **sys**. En el problema se trabajará con las variables aleatorias uniforme (0,1), normal y exponencial, siendo éstas dos últimas implementadas por el estudiante y se desarrollará un modelo híbrido entre el Modelo de Servidores en Serie y el Modelo de Servidores en Paralelo. Todos los tiempos tenidos en cuenta en el proyecto se toman en forma de minutos, y se redondean para mejor visibilidad y fácil trabajo.

## Implementación del Ejercicio

### Variables Aleatorias:

Utilizando la librería **numpy** para crear una variable aleatoria uniforme (0,1), se siguen las fórmula de generación según TTI para implementar la generación de variables aleatorias normal y exponencial.

```python
#Variable aleatoria Normal
def gen_VA_normal(_mi, _sigma2):
    _arrayU = [np.random.uniform(0,1) for x in range(12)]
    X = _mi + np.sqrt(_sigma2)*(np.sum(_arrayU)-6)
    return X

#Variable aleatoria Exponencial
def gen_VA_exp(_lambda):
    U = np.random.uniform(0,1)
    X = -_lambda*np.log(U)
    return X
```

Éstas implementaciones se encuentran en la carpeta del proyecto, cada una en un **.py** que la contiene y que luego será importado al proyecto.

### Simulación:

Para la simuación del problema, creamos una clase **Simulacion** donde se inicializarán las variables y se desarrollarán los métodos necesarios. Teniendo en cuenta los modelos de Servidores en Serie y Servidores en Paralelo las variables inicializadas quedarían de la siguiente forma:

```python
def __init__(self):
        #Variable de tiempo (tomaremos todos los tiempos del problema en minutos)
        self.T = 24*60 #1 dia
        self.t = 0
        self.t_arribo = self.t_remolcador = sys.maxsize
        self.t_muelles = [sys.maxsize,sys.maxsize,sys.maxsize] 
        self.t_entrada_muelle = [0,0,0]
        
        #Variables Contadoras
        self.cant_arribos = self.cant_salidas = self.cola_puerto = self.sum_tiempo_muelle = 0
        
        #Variables de estado
        self.remolcador = 0
        # 0 -> está en el puerto disponible
        # 1 -> está en el muelle disponible 
        # 2 -> se dirige al muelle con tanquero
        # 3 -> se dirige al puerto con tanquero 
        # 4 -> se dirige al puerto sin tanquero 
        # 5 -> se dirige al muelle sin tanquero
        self.muelles = [True,True,True]
        # True -> muelle vacío
```

El método `simulacion_evento` se encarga de correr la simulación, que comienza generando un primer arribo utilizando una variable aleatoria exponencial con *lambda* = 480 minutos y luego corriendo un *loop* de tipo `while` hasta que se cumplan los parámetros de finalización de la simulación. Para saber el estado de la simulación en que nos encontramos, seleccionamos el mínimo valor entre las variables de tiempo (a excepción de `t_entrada_muelle` que se utiliza para calcular el promedio de tiempo en los muelles de los cargueros) y con ayuda de `switch_t` (método implmentado para simular en **python** los *switch* de lenguajes como **C#** y **JavaScript**) definimos el método a utilizar. En caso que el mínimo tiempo sea `t_remolcador` entonces se utiliza otro *switch* para diferenciar el estado en que se encuentra el remolcador.

```python
#Switch para definir el método a utilizar
def switch_t(self, value):
        dic_t = {
            self.t_arribo: self.suc_arribo,
            min(self.t_muelles): self.suc_carga,
            self.t_remolcador : self.switch_remolcador(self.remolcador),
        }
        dic_t.get(value)()

#Método que controla el arribo de cargueros al puerto
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
        #print("Arribó un barco a los: {} minutos".format(self.t)) 

```
Al finalizar la simulación se devuelve el promedio de tiempo de espera en los muelles de los barcos cargueros.

## Observaciones

Luego de realizar la simulación de este ejercicio se puede comprobar que la cantidad de barcos que entran, salen, así como el tiempo que demoran cada uno de los procesos, dependen en gran medida de las variables aleatorias. Esto hace que sea muy difícil que se repitan simulaciones, probabilidad que sólo disminuye mientras aumente el tiempo total de la simulación (`self.T`). 

![](https://github.com/Juano97/projecto1_simulacion/blob/main/Images/Figure_2.png?raw=true)

![](https://github.com/Juano97/projecto1_simulacion/blob/main/Images/Figure_3.png?raw=true)

![](https://github.com/Juano97/projecto1_simulacion/blob/main/Images/Figure_4.png?raw=true)

Como se puede apreciar en las gráficas anteriores, a medida que aumenta `T`, los diferentes valores de promedio de tiempo en los muelles se vuelven menos erráticos y dispersos, aunque siempre se mantienen la mayoría de estos valores en un radio alrededor de 60 minutos.

![](https://github.com/Juano97/projecto1_simulacion/blob/main/Images/Figure_6.png?raw=true)

A medida que aumenta el número de simulaciones, se vuelve más marcado lo planteado anteriormente.

Todas éstas imágenes fueron generadas en **distribucion.py** utilizando la librería **matplotlib**