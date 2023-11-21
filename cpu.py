from enum import Enum


class CPU:
    def __init__(self):
        # power on into RESET mode
        self.CLEAR = 0
        self.WAIT = 1

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

    def set_control_mode(self, mode):
        self.CLEAR, self.WAIT = mode.value & 0x02, mode.value & 0x01

        match mode:
            case ControlMode.RESET:
                self.I = 0x0
                self.N = 0x0
                self.Q = 0
                self.IE = 1

    def tick(self):
        if self.CLEAR | self.WAIT == ControlMode.RUN.value:
            self.R[self.P] = (self.R[self.P] + 1) % 0xFF


class ControlMode(Enum):
    LOAD = 0
    RESET = 1
    PAUSE = 2
    RUN = 3
