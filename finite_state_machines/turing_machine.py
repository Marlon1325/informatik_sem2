import pandas as pd

class Turing:
    def __init__(self, table, start_state):
        self.df = pd.DataFrame(table, columns=["state", "input", "newstate", "output"])
        self.start_state = start_state

    def __print(self, steps, head, tape, state,absolute_pos ):
        # Anzeige vorbereiten
        display_tape = tape.copy()
        display_tape[absolute_pos] = f"\033[4m\033[91m{display_tape[absolute_pos]}\033[0m"
        print(f"\033[90m{steps:>2}{":"}\033[0m"+" "*3 +f"{head}, ...{''.join(display_tape)}..., {state}")


    def __call__(self, tape: str, start_index: int):
        tape = list(tape)
        head = 0  # Kopf startet bei logischer Position 0
        zero_index = start_index  # Das ist der Index im Band, der Position 0 entspricht
        steps = 0
        max_steps = 10_000
        state = self.start_state

        while True:
            if steps > max_steps:
                raise RuntimeError("endless loop")
            steps += 1

            # Band links erweitern, falls nötig
            while head + zero_index < 0:
                tape.insert(0, "-")
                zero_index += 1  # verschiebe Nullpunkt mit
            # Band rechts erweitern, falls nötig
            while head + zero_index >= len(tape):
                tape.append("-")

            absolute_pos = head + zero_index
            current_symbol = tape[absolute_pos]

            self.__print(steps,head,tape,state, absolute_pos)

            # Übergang suchen
            match = self.df[
                (self.df["state"] == state) &
                (self.df["input"] == current_symbol)
            ]

            if match.empty:
                break  # Kein Übergang = stoppen

            row = match.iloc[0]
            state = row["newstate"]
            output = row["output"]

            if output == "l":
                head -= 1
            elif output == "r":
                head += 1
            elif output == "h":
                self.__print(steps+1,head,tape,state, absolute_pos)
                break
            else:
                tape[absolute_pos] = output
