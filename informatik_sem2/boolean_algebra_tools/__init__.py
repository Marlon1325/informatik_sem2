from .truth_table import truth_table
from .kv_diagramm import KV_Diagramm
from .use_np import use_np
from .McCluskey import  McCluskey
import pandas as pd

__all__ = [
    "truth_table",
    "KV_Diagramm",
    "use_np",
    "McCluskey",
    "highlight_df"
]


def highlight_df(df: pd.DataFrame, color="red", value=1):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    return df.style.map(lambda val: f'color: {color}' if val == value else '')