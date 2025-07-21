from .truth_table import truth_table
import pandas as pd
import string
from .use_np import use_np
from types import FunctionType

__all__ = ["McCluskey", "create_function_from_prims", "prim_implicants_table"]

def McCluskey(funktion, printl=True)->list[str]:
    # Wahrheitstafel erzeugen
    tabelle: pd.Series = truth_table(funktion)
    tabelle = tabelle[tabelle == 1]
    minterms = tabelle.index.tolist()

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

    def group_by_ones(terms):
        """Gruppiert Terme nach der Anzahl Einsen."""
        groups = {}
        for term in terms:
            ones = term.count('1')
            groups.setdefault(ones, []).append(term)
        return groups

    def print_groups(groups, step):
        if not printl: return
        print(f"\n=== Schritt {step}: Gruppierung nach Einsen ===")
        for ones_count, terms in sorted(groups.items()):
            print(f"{ones_count} Eins(en): {terms}")

    def get_prime_implicants(minterms):
        """Hauptschritt des Quine-McCluskey-Verfahrens."""
        terms = minterms[:]
        prime_implicants = set()
        step = 1

        while True:
            groups = group_by_ones(terms)
            print_groups(groups, step)

            new_terms = set()
            marked = set()

            sorted_groups = sorted(groups.items())
            for i in range(len(sorted_groups) - 1):
                group1 = sorted_groups[i][1]
                group2 = sorted_groups[i + 1][1]
                for term1 in group1:
                    for term2 in group2:
                        combined = combine(term1, term2)
                        if combined:
                            marked.add(term1)
                            marked.add(term2)
                            new_terms.add(combined)

            # Nicht kombinierte Terme sind Prime-Implicants dieser Runde
            non_combined = [term for term in terms if term not in marked]
            if non_combined:
                if printl:
                    # print(f"Nicht kombinierbare Terme (Prime-Implicants dieser Runde): {non_combined}")
                    print("Nicht kombinierbare Terme (Prime-Implicants dieser Runde):")
                    print(sorted(non_combined, key=lambda x: x.count("1") ), end="\n"*2)
                prime_implicants.update(non_combined)

            if not new_terms:
                break
            if printl:
                # print(f"Neue kombinierte Terme: {sorted(new_terms)}")
                print("Neue kombinierte Terme:")
                print(sorted(new_terms, key=lambda x: x.count("1") ), end="\n"*2)
            terms = list(new_terms)
            step += 1

        return list(prime_implicants)

    # Prime-Implicants berechnen
    prime_implicants = get_prime_implicants(minterms)

    if printl:
        print("\n=== Endgültige Prime-Implicants ===")
        for imp in prime_implicants:
            print(imp)

    return prime_implicants


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

