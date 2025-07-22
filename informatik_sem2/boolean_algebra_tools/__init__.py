from .truth_table import truth_table
from .kv_diagramm import KV_Diagramm
from .use_np import use_np
from . import  McCluskey
import pandas as pd
import numpy as np
from types import FunctionType

__all__ = [
    "truth_table",
    "KV_Diagramm",
    "use_np",
    "McCluskey",
    "highlight_df",
    "areEqual"
]


def highlight_df(df: pd.DataFrame, color="red", value=1):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    return df.style.map(lambda val: f'color: {color}' if val == value else '')

def areEqual(*functions: FunctionType) -> np.bool_:
    "returns True if boolean functions are equal"
    tt = truth_table(*functions)
    tt['='] = tt.nunique(axis=1) == 1
    return tt["="].all()