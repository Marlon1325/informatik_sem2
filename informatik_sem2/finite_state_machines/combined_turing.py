class Combined_Turing:
    def __init__(self, content: str, start_index: int = 0):
        self.tape = list(content)
        self.head = 0
        self.zero_index = start_index  # Position im Tape, die logischer Index 0 ist

    def l(self, n=1):
        for _ in range(n):
            self.head -= 1
            absolute_pos = self.head + self.zero_index
            self.__ensure_bounds(absolute_pos)
        return self

    def r(self, n=1):
        for _ in range(n):
            self.head += 1
            absolute_pos = self.head + self.zero_index
            self.__ensure_bounds(absolute_pos)
        return self

    def write(self, symbol: str):
        absolute_pos = self.head + self.zero_index
        self.__ensure_bounds(absolute_pos)
        self.tape[absolute_pos] = symbol

    def read(self) -> str:
        absolute_pos = self.head + self.zero_index
        self.__ensure_bounds(absolute_pos)
        return self.tape[absolute_pos]

    def __ensure_bounds(self, absolute_pos: int):
        while absolute_pos < 0:
            self.tape.insert(0, "-")
            self.zero_index += 1
            absolute_pos += 1
        while absolute_pos >= len(self.tape):
            self.tape.append("-")

    def __repr__(self):
        # Markiert die aktuelle Position mit Unterstreichung
        display_tape = self.tape.copy()
        absolute_pos = self.head + self.zero_index
        self.__ensure_bounds(absolute_pos)
        display_tape[absolute_pos] = f"\033[4m\033[91m{display_tape[absolute_pos]}\033[0m"
        return f"...{''.join(display_tape)}..."



    def L(self, n=1):
        "große Links-Maschine"
        for _ in range(n):
            self.l()
            while self.read() != "-":
                self.l()
        return self

    def R(self, n=1):
        "große Rechts-Maschine"
        for _ in range(n):
            self.r()
            while self.read() != "-":
                self.r()
        return self

    def b(self):
        "schreibt blank"
        self.write("-")
        return self

    def line(self):
        "schreibt |"
        self.write("|")
        return self


    def T_l(self):
        "linke Translationsmaschine"
        while True:
            self.r(2)
            if self.read() == "-":
                self.l()
                break
            self.b()
            self.l()
            self.line()
        return self


    def K(self, m=1, n=1):
        "Kopiermaschine K_n^m"

        for _ in range(n):
            for _ in range(m):
                self.L()

            self.r()
            word = ""
            while self.read() != "-":
                word += self.read()
                self.r()

            for _ in range(m-1):
                self.R()
    
            for x in word:
                self.r()
                self.write(x)
            self.r()
        return self
    
    def Ls(self, n=1):
        for _ in range(n):
            self.l()
            if self.read() == "|":
                return self
            
    def Rs(self, n=1):
        for _ in range(n):
            self.R()
            if self.read() == "|":
                return self



