from abc import ABC, abstractmethod


class CPU:
    _state = None

    def __init__(self):
        self.set_state(Reset())

        # setup registers
        self.D = 0x00           # Data Register (Accumulator), 8b
        self.DF = 0             # Data Flag (ALU Carry), 1b
        self.B = 0x00           # Auxiliary Holding Register, 8b
        self.R = [0x0000]*16    # Scratchpad Registers, 16x16b
        self.P = 0x0            # Designates Program Counter register, 4b
        self.X = 0x0            # Designates Data Pointer register, 4b
        self.N = 0x0            # Low-Order Instruction Digit, 4b
        self.I = 0x0            # High-Order Instruction Digit, 4b
        self.T = 0x00           # Previous X, P after Interrupt (X is high nibble), 8b
        self.IE = 1             # Interrupt Enable, 1b
        self.Q = 0              # Output Flip-Flop, 1b

    def set_state(self, state):
        self._state = state
        self._state.cpu = self

    def tick(self):
        self._state.tick()


class State(ABC):
    @property
    def cpu(self):
        return self._cpu

    @cpu.setter
    def cpu(self, cpu):
        self._cpu = cpu

    @abstractmethod
    def tick(self):
        pass


class Reset(State):
    def tick(self):
        self.cpu.I = 0x0
        self.cpu.N = 0x0
        self.cpu.Q = 0
        self.cpu.IE = 1


class Run(State):
    def tick(self):
        self.cpu.R[self.cpu.P] = (self.cpu.R[self.cpu.P] + 1) % 0xFFFF
