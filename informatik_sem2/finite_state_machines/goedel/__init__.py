from ..turing_machine import Turing
from sympy import factorint
from IPython.display import display, Math, HTML
import numpy as np
import pandas as pd
import string, os

__all__=["Turing_from_Goedel", "Goedel_from_Turing", "Goedel_from_tape", "get_prim_numbers", "Turing", "factorint"]


def get_prim_numbers():
    prims_path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
            ), "prim_numbers"
        )
    return np.fromfile(prims_path, dtype=np.uint32)
    

def sigma2(i,j):
    return 2**i*(2*j+1)-1





def Turing_from_Goedel(number):
    print(f"Gödelnummer: {number}")
    # primfaktorzerlegung
    prims:dict = factorint(number)
    display(Math("$$"+r"\text{Prims:}\hspace{1cm}" + r"\cdot ".join([f"{x}^{{{y}}}" for x, y in prims.items()]) + "$$"))


    m = prims[2]
    k = prims[3]

    n = (m+1)*(k+1)
    matrix: list[list] = [[],[], [0]*n, [0]*n]
    for s in range(k+1):
        for t in range(m+1):
            matrix[0].append(s)
            matrix[1].append(t)
    matrix:np.ndarray = np.array(matrix).T



    idx = np.arange(n)+1
    df = pd.DataFrame({
        "i": idx,
        "sigma2(i,3)": sigma2(idx, 3),
        "sigma2(i,4)": sigma2(idx, 4)
    }
    )
    df =df.set_index("i")
    prim_numbers = get_prim_numbers()

    for j in range(3,5):
        df[f"P_sigma2(i,{j})"] = df[f"sigma2(i,{j})"]

        df[f"P_sigma2(i,{j})"] = df[f"P_sigma2(i,{j})"].apply(lambda i: prim_numbers[i-1])


    print("")
    
    display(Math("$$"+r"\hspace{1.5cm}".join([r"\sigma_2(i,3)", r"\sigma_2(i,4)", r"p_{\sigma_2(i,3)}", r"p_{\sigma_2(i,4)}"]) +"$$"))
    display(HTML(df.to_html()))
    print("\n")

    for x in prims.keys():
        if x in (2,3):
            continue
        if not x in df["P_sigma2(i,3)"].values and not x in df["P_sigma2(i,4)"].values:
            raise ValueError(f"{x} ist not used for building the turingmachine")
        
    for p in prims.keys():
        if p in (2,3):
            continue
        for j in range(3,5):
            x =df[df[f"P_sigma2(i,{j})"] == p][f"P_sigma2(i,{j})"].head(1)
            if not x.empty:
                i = x.index.item()
                v = x.item()
                matrix[i-1,j-1] = prims[v]
        
    if not (k >= matrix.T[2]).all():
        raise ValueError(f"More that k States")
    
    if not (m+3 >= matrix.T[3]).all():
        raise ValueError(f"More than m+3 tape symbols")

    def replace_output(x):
        if x == m+1:     return "l"
        elif x== m+2:    return "r"
        elif x == m+3:   return "h"
        elif x == 0:    return "-"
        else:  return string.ascii_uppercase[x-1]

    def replace_input(x):
        if x==0:
            return "-"
        else:
            return  string.ascii_uppercase[x-1]

    print(matrix)

    matrix = matrix.astype(object)          
    matrix[:, 3:5] = np.vectorize(replace_output, otypes=['O'])(matrix[:, 3:5])
    matrix[:, 1] = np.vectorize(replace_input, otypes=['O'])(matrix[:, 1])
    
    TM = Turing(matrix, 0)
    return TM










def Goedel_from_Turing(TM: Turing, showTable=True):
    df = TM.df.copy()
    df = df.sort_values(by=["state", "input"]).reset_index(drop=True)

    k = len(set(df["state"])) - 1
    T = sorted(set(df["input"]).union(set(df["output"])).difference({"r", "l", "h"}))
    T = tuple(T)
    m = len(T) -1
    
    prims_numbers = get_prim_numbers()

    prims_factors = {
        2: m,
        3: k
    }

    def getMatrix(matrix: np.ndarray):
        matrix = matrix.copy()
        def replace(x):
            if x == "h": return m+3
            elif x=="r": return m+2
            elif x=="l": return m+1
            else: return T.index(x)
                
        for i in (1,3):
            for j in range(matrix.shape[0]):
                matrix[j,i] = replace(matrix[j,i])
        return matrix
    
    C = getMatrix(df.values)

    df = {"P_sigma2(i,3)": [], "P_sigma2(i,4)": [], "ci3":[], "ci4": []}

    for i in range(1,(k+1)*(m+1)+1):
        for j in (3,4): # (3,4)
            sigma = sigma2(i,j)
            p = int(prims_numbers[sigma-1])
            c = C[i-1,j-1]

            if j==3:
                df["P_sigma2(i,3)"].append(p)
                df["ci3"].append(c)
            else: 
                df["P_sigma2(i,4)"].append(p)
                df["ci4"].append(c)

            prims_factors[p] = c

    if showTable:  
        display(Math("$$"+r"\hspace{1cm}".join(["i", r"p_{\sigma_2(i,3)}", r"p_{\sigma_2(i,4)}", r"c_{ij}", r"c_{ij}"]) +"$$"))
        df = pd.DataFrame(df, index=pd.Series(np.arange(1,len(df["ci3"])+1), name="i"))
        display(HTML(df.to_html(escape=False)))
    
    prod_str = [f"{x}^"+"{"+f"{y}"+"}" for x,y in filter(lambda x: x[1] !=0, prims_factors.items())]

    display(Math(r"\text{Gödelnummer:}\hspace{1cm}" + f"{r"\cdot ".join(prod_str)}$$"))

    prod = 1
    for key,value in prims_factors.items():
        newprod = prod * key**value
        if prod==newprod and value!=0:
            return
        else:
            prod = newprod
    return prod










def Goedel_from_tape(tape: str, p0: int | str, alphabet: list[str]=None):
    if alphabet is None:
        alphabet = ["-"] +sorted(set(tape))
    if isinstance(p0, str):
        p0 = tape.find(p0)

    stop = max(p0*2, (len(tape)-p0)*2)
    minus = np.arange(1,p0*2,2)[::-1]
    plus = np.arange(0, (len(tape)-p0)*2, 2)

    prim_numbers = get_prim_numbers()

    S = pd.Series(
        data = list(tape),
        index= np.concat((minus, plus))
    )
    print(S)
    print("\nalphabet"," ".join(alphabet))
    prod_str = []
    for i in range(stop):
        if i in S.index:
            prod_str.append(f"{prim_numbers[i]}^"+"{"+f"{alphabet.index(S.loc[i])}" +"}")
        else:
            prod_str.append(f"{prim_numbers[i]}^0")
    
    display(Math(r"$$\text{Gödelnummer:}\hspace{1cm}" + f"{r"\cdot ".join(prod_str)}$$"))