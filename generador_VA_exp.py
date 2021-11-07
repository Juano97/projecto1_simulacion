import numpy as np

def gen_VA_exp(_lambda):
    U = np.random.uniform(0,1)
    X = -_lambda*np.log(U)
    return X