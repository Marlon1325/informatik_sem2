class Tape:
    def __init__(self, content: str, start_index: int = 0):
        self.tape = list(content)
        self.head = 0
        self.zero_index = start_index  # Position im Tape, die logischer Index 0 ist

    def left(self):
        self.head -= 1
        absolute_pos = self.head + self.zero_index
        self.__ensure_bounds(absolute_pos)

    def right(self):
        self.head += 1
        absolute_pos = self.head + self.zero_index
        self.__ensure_bounds(absolute_pos)

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


def r(tape: Tape):
    tape.right()
    return tape

def l(tape: Tape):
    tape.left()
    return tape

def L(tape: Tape, n=1):
    "große Links-Maschine"
    for i in range(n):
        tape.left()
        while tape.read() != "-":
            tape.left()
    return tape

def R(tape: Tape, n=1):
    "große Rechts-Maschine"
    for i in range(n):
        tape.right()
        while tape.read() != "-":
            tape.right()
    return tape

def blank(tape: Tape):
    tape.write("-")
    return tape

def line(tape: Tape):
    tape.write("|")
    return tape


def kopier(n: int, tape: Tape):
    """
    Implements the n-copy machine Kₙ from the script.
    
    Transforms: ...w₁␣w₂␣...␣wₙ␣... → ...w₁␣w₂␣...␣wₙ␣w₁␣...
    where ␣ is represented by "-" in our Tape class.
    
    Args:
        n: Number of words to skip (n-1 intervening words)
        tape: The Tape object with input
    """
    # 1. Move to the start of w₁ (first blank left of w₁)
    while tape.read() != "-":
        l(tape)
    
    # Now at the blank before w₁
    start_pos = tape.head
    
    # 2. Move to the end of w₁ (first blank right of w₁)
    r(tape)  # Move into w₁
    while tape.read() != "-":
        r(tape)
    end_pos = tape.head - 1  # Last position of w₁
    
    # 3. Move to the end of the n words (n+1 blanks right of w₁)
    for _ in range(n):
        while tape.read() != "-":
            r(tape)
        r(tape)  # Skip the blank
    
    # Now at the position where we'll start copying w₁
    copy_pos = tape.head
    
    # 4. Copy w₁ to this position
    current_pos = start_pos + 1  # Start of w₁
    while current_pos <= end_pos:
        # Move to current symbol in w₁
        tape.head = current_pos
        symbol = tape.read()
        
        # Move to copy position and write symbol
        tape.head = copy_pos
        tape.write(symbol)
        copy_pos += 1
        current_pos += 1
    
    # 5. Add final blank after copied w₁
    tape.head = copy_pos
    blank(tape)
    
    # 6. Return head to start of original w₁ (optional)
    tape.head = start_pos + 1
    return tape