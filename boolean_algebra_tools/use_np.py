from decorator import decorator
from types import FunctionType
import numpy as np
    
        
@decorator
def use_np(function: FunctionType, *args, **kwargs):
    "decorator der jedes arg zu einer Instanz der np.bool-Klasse macht"
    args = tuple(map(np.bool, args))
    kwargs = {key: np.bool(value) for key, value in kwargs}
    return np.bool(function(*args, **kwargs))

