import numpy as np

def genVAexp(_lambda):
    U = np.random.uniform(0,1)
    X = -(1/_lambda)*np.log(U)
    return X
