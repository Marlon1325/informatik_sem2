from .truth_table import truth_table
import pandas as pd
import string
from .use_np import use_np
from types import FunctionType
import itertools

__all__ = ["McCluskey", "create_function_from_prims", "prim_implicants_table"]

def combine(term1, term2):
    """Versucht zwei Terme zu kombinieren. Gibt kombinierten Term zurück oder None."""
    diff = 0
    combined = []
    for a, b in zip(term1, term2):
        if a != b:
            if a == '-' or b == '-':
                return None
            diff += 1
            combined.append('-')
        else:
            combined.append(a)
    if diff == 1:
        return ''.join(combined)
    return None


def printStep(round, combined_groups:set):
    print(f"\n=== Runde {round}  ===")
    for key, value in sorted(combined_groups.items()):
        print(f"Einsen: {key}    {str(value).replace("'", " ").replace(",", " ")}")

def sort_in_groups(minterms:set) -> dict[int,set]:
    groups = dict()
    for term in minterms:
        ones = term.count('1')
        groups.setdefault(ones, set()).add(term)  
    return groups



def McCluskey(function: FunctionType, printl=True)->set[str]:
    "Minimiert Funktion mit dem Quine-McCluskey verfahren"
    tabelle: pd.Series = truth_table(function)
    tabelle = tabelle[tabelle == 1]
    minterms = tabelle.index.tolist()
    groups = sort_in_groups(minterms)

    round = 1
    
    if printl: printStep(1, groups)

    while True:
        changed = False
        combined = set()
        marked = set()

        for i in range(min(groups.keys()), max(groups.keys())):
            if i not in groups or i + 1 not in groups:
                continue
            for term1, term2 in itertools.product(groups[i], groups[i + 1]):
                combined_term = combine(term1, term2)
                if combined_term is not None:
                    marked.add(term1)
                    marked.add(term2)
                    combined.add(combined_term)
                    changed = True

        # --- Neue Gruppen aus kombinierten Termen ---
        combined_groups = sort_in_groups(combined)

        # --- Alle nicht kombinierten (unmarkierten) Terme sollen mitgegeben werden ---
        for group_key, term_set in groups.items():
            unmarked = term_set.difference(marked)
            if unmarked:
                combined_groups.setdefault(group_key, set()).update(unmarked)

        if changed:
            round += 1
            groups = combined_groups
            if printl:
                printStep(round, combined_groups)

        else:
            break
    
    prims_implicants = set()
    for value in combined_groups.values():
        prims_implicants.update(value)
    return prims_implicants


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

