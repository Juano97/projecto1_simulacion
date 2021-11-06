import numpy as np

def genVAexp(_lambda):
    U = np.random.uniform(0,1)
    X = -_lambda*np.log(U)
    return X

print(genVAexp(15))