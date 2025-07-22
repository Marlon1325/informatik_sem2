import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import itertools
import copy


import pandas as pd

class Delta:
    "Zustandübergangsfunktion"
    def __init__(self,table:dict):
        n=len(list(table.values())[0])
        states = list(range(n))
        self.df = pd.DataFrame(table, index=states, dtype=np.int16).T
        
    def __call__(self, state, input):
        if state not in self.df.columns:
            raise ValueError(f"State {state} is not in {list(self.df.columns)}")
        if input not in self.df.index:
            raise ValueError(f"Input {state} is not in {list(self.df.index)}")
        return int(self.df.loc[input, state])

    def __repr__(self):
        return self.df.__repr__()
    
    def _repr_markdown_(self):
        df = self.df.copy()
        df.index.name = r"$$\delta$$"
        df = df.reset_index()
        return df.to_markdown(index=False)


class Beta:
    "Ausgabefunktion"
    def __init__(self, array):
        states = list(range(len(array)))
        self.S = pd.Series(array, index=states, dtype=np.int16)

    def __call__(self, state):
        if not state in self.S.index:
            raise ValueError(f"State {state} is not in {list(self.S.index)}")
        return int(self.S.loc[state])
    
    def __repr__(self):
        return self.S.__repr__()
    
    def _repr_markdown_(self):
        S = pd.DataFrame({r"$$\beta$$": self.S})
        return S.T.to_markdown()



class Moore:
    """
    d = Delta({\n
    "a": [1,3,7,6,9,5,9,0,4,3,3,9,11],
    "b": [2,6,6,2,8,11,2,12,10,2,12,6,2],
    "c": [3,0,3,1,9,2,11,4,7,1,1,0,3]
})\n
b = Beta([2,1,1,0,1,0,0,2,1,0,0,1,2])\n
\n
M = Moore(
    list(range(13)),
    ("a", "b", "c"),
    (0,1,2),
    d,b
)\n
M.minimize_plot()
"""
    def __init__(self, states: tuple, inputs: tuple, outputs: tuple, delta: Delta, beta: Beta, q0=None):
        self.states = tuple(states)
        self.inputs = tuple(inputs)
        self.outputs = tuple(outputs)

        if not isinstance(delta, Delta):
            delta = Delta(delta)
        if not isinstance(beta, Beta):
            beta = Beta(beta)
        self.delta = delta
        self.beta = beta

        self.q = q0 if q0 else self.states[0]

    def __call__(self, inp, printState=False):
        if inp not in self.inputs:
            raise ValueError(f"{inp} is not in the Input-Alphabet")
        if printState:
            print(f"State: {self.q} -> ", end="")

        self.q = self.delta(self.q, inp)

        if printState:
            print(f"{self.q}")
        return self.beta(self.q)
    
    def __getitem__(self, x):
        "Moore[state, input]"
        state, inp = x
        if inp not in self.inputs:
            raise ValueError(f"{inp} is not in the Input-Alphabet")
        
        state, self.q = self.q, state
        out =self(inp)

        self.q = state
        return out

    def __repr__(self):
        return f"""
States:  {self.states}
Inputs:  {self.inputs}
Outputs: {self.outputs}

delta - "Zustandübergangsfunktion": 
{self.delta.__repr__()}

beta - Ausgabefunktion:
{self.beta.__repr__()}
"""
    
    def _repr_markdown_(self):
        return f"""
States:  {self.states}\n
Inputs:  {self.inputs}\n
Outputs: {self.outputs}\n


delta - "Zustandübergangsfunktion": 
{self.delta._repr_markdown_()}


beta - Ausgabefunktion:
{self.beta._repr_markdown_()}
"""

    def minimize_plot(M) -> list[set[int]]:
        "plots table with marked pairs and fusible state-pairs"
        if not isinstance(M, Moore):
            raise ValueError("Machine must be an instance of Moore-class")

        n = len(M.states)
        matrix = pd.DataFrame(
            np.zeros((n, n), dtype=np.int8),
            columns=M.states, index=M.states
        )

        # Runde 1: Markiere unterschiedliche Ausgaben
        round_counter = 1
        for s1, s2 in itertools.combinations(M.states, 2):
            if M.beta(s1) != M.beta(s2):
                i1, i2 = sorted((s1, s2))
                matrix.at[i1, i2] = round_counter  # R1 = unterschiedlich

        # Folge-Runden: Propagation über Übergänge
        changed = True
        while changed:
            changed = False
            round_counter += 1
            for (i, s1), (j, s2) in itertools.combinations(enumerate(M.states), 2):
                i1, i2 = sorted((s1, s2))
                if matrix.at[i1, i2] == 0:  # Noch unmarkiert
                    for a in M.inputs:
                        next_s1 = M.delta(s1, a)
                        next_s2 = M.delta(s2, a)
                        n1, n2 = sorted((next_s1, next_s2))
                        if matrix.at[n1, n2] != 0:
                            matrix.at[i1, i2] = round_counter  # markiere mit aktueller Runde
                            changed = True
                            break

        
        # Für Visualisierung: Matrix etwas auffüllen
        matrix_vis = (matrix + np.triu(np.ones((n, n), dtype=int)) - np.diag(np.ones(n))).astype(np.int8)
        max_round = matrix.values.max()
        colors = ["#ffffff", "#000000", "#FF9D00", "#00CF26", "#F81B1B", "#FFFF00", "#0000FF", "#00EAFF", "#C300FF"][:max_round + 2]

        cmap = ListedColormap(colors)
        fig, ax = plt.subplots()

        ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=0.5)

        bounds = np.arange(max_round + 3) - 0.5
        norm = BoundaryNorm(bounds, cmap.N)
        ax.set_title("Marked State Pairs by Round")
        cax = ax.matshow(matrix_vis.T, cmap=cmap, norm=norm)  # .T = visuell obere Dreiecksmatrix

        ax.set_xlabel("state")
        ax.set_ylabel("state")
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_xticklabels(list(M.states))
        ax.set_yticklabels(list(M.states))
        ax.xaxis.set_ticks_position('bottom')

        labels = ["", "remaining\nfields"] + [f"R.{r}" for r in range(1, max_round + 1)]
        cbar = plt.colorbar(cax, ticks=np.arange(max_round + 2))
        cbar.ax.set_yticklabels(labels)

        plt.show()

        # Unmarkierte Paare (matrix == 0) = verschmelzbar
        pairs = np.where(matrix_vis == 1)

        pairs = [{int(a), int(b)} for a, b in zip(*pairs)]

        return merge_sets(pairs)
    

    
    def create_minimized_moore(self, state_groups:list[set]):
        """
        Minimiert einen Moore-Automaten auf Basis gegebener Äquivalenzklassen
        und gibt einen neuen Automaten mit ganzzahligen Zuständen zurück.
        """
        # Fehlende Zustände ergänzen
        delta = copy.deepcopy(self.delta)
        beta = self.beta.S.to_dict()

        for s1,s2 in state_groups:
            delta.df = delta.df.map(lambda x: s1 if x==s2 else x)
            del delta.df[s2]
            del beta[s2]
        Map = { x: y for x,y in zip(delta.df.columns, range(len(delta.df.columns)))}
        beta = {Map[k]:v for k,v in beta.items()}
        beta = Beta(pd.Series(beta))
        delta.df = delta.df.rename(columns=Map)
        delta.df = delta.df.map(lambda x: Map[x])
        M = Moore(self.states, self.inputs, self.outputs, delta, beta)
        M.q =0
        return M


def merge_sets(sets):
    sets = [set(s) for s in sets]  # sicherstellen, dass alle Elemente Sets sind
    merged = []

    while sets:
        first, *rest = sets
        first = set(first)

        changed = True
        while changed:
            changed = False
            rest2 = []
            for s in rest:
                if first & s:  # es gibt eine Überschneidung
                    first |= s
                    changed = True
                else:
                    rest2.append(s)
            rest = rest2

        merged.append(first)
        sets = rest

    return merged
