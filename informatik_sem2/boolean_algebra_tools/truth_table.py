
import inspect
import pandas as pd
import numpy as np
from types import FunctionType


def truth_table(*functions: FunctionType, dtype:type = np.int8)->pd.Series | pd.DataFrame:
    "Gibt Dataframe/Series zurück mit allen Kombinationen der Parameter"
    if not functions:
        raise ValueError("Mindestens eine Funktion muss übergeben werden!")
    
    num_args = max([len(inspect.signature(f).parameters) for f in functions] )

    outputs:dict[str, list] = {}
    lambda_counter = 0
    for f in functions: 
        if f.__name__ == "<lambda>":
            name =f"lambda_{lambda_counter}"
            lambda_counter += 1
        else:
            name = f.__name__
        outputs[name] = []

    index = []
    for i in range(2**num_args):
        b_str = f"{i:0{num_args}b}"
        b_int = tuple(map(int, b_str))

        index.append(b_str)
        lambda_counter = 0

        for f in functions:
            m = len(inspect.signature(f).parameters)
            erg = np.bool(f(*b_int[:m])) # max m parameter
            name:str
            if f.__name__ == "<lambda>":
                name = f"lambda_{lambda_counter}"
                lambda_counter += 1
            else:
                name = f.__name__
            outputs[name].append(erg)

    df: pd.DataFrame = pd.DataFrame(outputs, index=index, dtype=dtype)
        
    if len(functions) == 1:
        return df.squeeze()
    else:
        return df
    

