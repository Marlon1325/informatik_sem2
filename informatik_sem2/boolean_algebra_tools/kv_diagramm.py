import inspect
from types import FunctionType
import matplotlib.pyplot as plt
import numpy as np
   

class KV:
    def __init__(self):
        fig, ax = plt.subplots()
        ax.set_title("Karnaugh-Veitch-Diagramm\n\n", fontsize=16)
        ax.tick_params(axis='x', which='both', labelbottom=False)
        ax.tick_params(axis='y', which='both', labelleft=False)
        ax.set_xticks(np.arange(-0.5, 4, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, 4, 1), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=1)
        ax.tick_params(which='minor', size=0)

        self.fig = fig
        self.ax  = ax


    def label(self, param_names:list[str], coordinates:list[tuple]):
        for label, coordinante in zip(param_names, coordinates):
            self.ax.text(*coordinante, label, transform=plt.gca().transAxes, 
                    fontsize=16,       # Schriftgröße
                    fontweight='bold', # fett
                    ha='center',       # horizontal zentriert
                    va='center' 
                )
    def addText(self, position:tuple, text:str):
        self.ax.text(*position, text, va='center', ha='center', fontsize=12)

    def matshow(self, m:np.ndarray):
        self.ax.matshow(m, cmap='Pastel1_r', vmin=0, vmax=1)



def KV_Diagramm(function: FunctionType):
    "plottet KV-Diagramm zu der übergebenen Funktion"
    params = inspect.signature(function).parameters
    num_params = len(params)

    if num_params not in range(2, 5):
        raise ValueError("Anzahl der Paramter muss zwischen 2 und 4 liegen!")
    
    kv = KV()
    inMatrix: np.ndarray

    if num_params == 2:
        inMatrix = np.zeros((2,2,num_params), dtype=np.int8)

        for i in range(2):
            for j in range(2):
                if i == 1: inMatrix[i,j,0] = 1
                if j == 1: inMatrix[i,j,1] = 1
                a,b = inMatrix[i][j]
                kv.addText((j,i), f"{a} {b}")

            coordinates = [(-0.1, 0.25), (0.75, 1.1)]

    if num_params == 3:
        inMatrix = np.zeros((2,4,num_params), dtype=np.int8)
        for i in range(2):
            for j in range(4):
                if i == 1: inMatrix[i][j][0] = 1
                if j in (2,3): inMatrix[i][j][1] = 1
                if j in (1,2): inMatrix[i][j][2] = 1

                a,b,c = inMatrix[i,j]
                kv.addText((j,i), f"{a} {b}\n{c}")
            
            coordinates = [(-0.1,0.25), (0.75, 1.1), (0.5, -0.1)]

    if num_params == 4:
        inMatrix = np.zeros((4,4,num_params), dtype=np.int8)

        for i in range(4):
            for j in range(4):
                if i in (1,2): inMatrix[i,j,0] = 1
                if j in (1,2): inMatrix[i,j,2] = 1
                if i in (2,3): inMatrix[i,j,1] = 1
                if j in (2,3): inMatrix[i,j,3] = 1
                a,b,c,d = inMatrix[i,j]
                kv.addText((j,i), f"{a} {b}\n{c} {d}")

        coordinates = [(-0.1, 0.5), (1.1, 0.25), (0.5, 1.1), (0.75,-0.1)]

    


    kv.label(params, coordinates)
    outMatrix:np.ndarray = np.zeros(inMatrix.shape[:2], dtype=np.int8)

    for i in range(outMatrix.shape[0]):
        for j in range(outMatrix.shape[1]):
            outMatrix[i, j] = bool(function(*inMatrix[i, j],))

        
        
    kv.matshow(outMatrix)
    plt.show()


