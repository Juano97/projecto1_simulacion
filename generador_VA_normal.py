import numpy as np

def gen_VA_normal(_mi, _sigma2):
    _arrayU = [np.random.uniform(0,1) for x in range(12)]
    X = _mi + np.sqrt(_sigma2)*(np.sum(_arrayU)-6)
    return X
