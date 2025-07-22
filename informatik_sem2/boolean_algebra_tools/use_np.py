from decorator import decorator
from types import FunctionType
import numpy as np
    
        
@decorator
def use_np(function: FunctionType, *args, **kwargs):
    "decorator der jedes arg zu einer Instanz der np.bool_-Klasse macht"
    args = tuple(map(np.bool_, args))
    kwargs = {key: np.bool_(value) for key, value in kwargs}
    return np.bool_(function(*args, **kwargs))

