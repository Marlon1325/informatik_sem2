from ..truth_table import truth_table
import string
from ..use_np import use_np
import pandas as pd
from types import FunctionType


def minterm(prims, variables=string.ascii_lowercase, AND="*", NOT="~"):
        term = []
        for i,x in enumerate(prims):
            match(x):
                case "1": term.append(variables[i])
                case "0": term.append(NOT+variables[i])
        return AND.join(term)


def create_function_from_prims(primlist:list, variables=string.ascii_lowercase, AND="*", OR="+", NOT="~", name=None)->tuple[FunctionType, str]:
    l = max(map(len, primlist))
    variables = variables[:l]

    term = f" {OR} ".join(map(lambda x: minterm(x, variables, AND, NOT), primlist))

    variables = ",".join(variables)
    function = eval(f"lambda {variables}: {term}")
    if name:
        function.__name__ = name
    return use_np(function), f"({variables})" + " =>  "+term



def prim_implicants_table(prim_implicants, variables=string.ascii_lowercase)->pd.Series:
    minterms = tuple(map(lambda x: minterm(x, variables, AND=" "), prim_implicants))
    functions =  tuple(create_function_from_prims([x], name=term)[0] for x, term in zip(prim_implicants, minterms) )
    wt = truth_table(*functions)
    return wt[wt.T.sum() > 0].T

