from __future__ import annotations
from states import Reset
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from states import State


class CPU:
    _state: State = None

    def __init__(self) -> None:
        self.set_state(Reset())

        # setup registers
        self.D = 0              # Data Register (Accumulator), 8b
        self.DF = 0             # Data Flag (ALU Carry), 1b
        self.B = 0              # Auxiliary Holding Register, 8b
        self.R = [0]*16         # Scratchpad Registers, 16x16b
        self.P = 0              # Designates Program Counter register, 4b
        self.X = 0              # Designates Data Pointer register, 4b
        self.N = 0              # Low-Order Instruction Digit, 4b
        self.I = 0              # High-Order Instruction Digit, 4b
        self.T = 0              # Previous X, P after Interrupt (X is high nibble), 8b
        self.IE = 1             # Interrupt Enable, 1b
        self.Q = 0              # Output Flip-Flop, 1b

        # setup data interfaces
        self.BUS = 0            # Data Bus, 8b
        self.EF = [0]*4         # External Flags, 4x1b
        self.N0 = 0
        self.N1 = 0
        self.N2 = 0

        # setup memory
        self.M = [0]*(2**16)    # Standard RAM and ROM up to 65,536B

    def set_state(self, state: State) -> None:
        self._state = state
        self._state.context = self

    def get_state(self) -> State:
        return self._state

    def tick(self) -> None:
        self.N2 = self.N1 = self.N0 = 0
        self._state.tick()

    def reset(self) -> None:
        self._state.reset()

    def run(self) -> None:
        self._state.run()

    def pause(self) -> None:
        self._state.pause()

    def increment_register(self, reg: int) -> None:
        # 0xFFFF + 1 = 0x000
        self.R[reg] = (self.R[reg] + 1) % 0x10000

    def decrement_register(self, reg: int) -> None:
        # 0x0000 - 1 = 0xFFFF
        self.R[reg] = self.R[reg] - 1 if self.R[reg] - 1 >= 0 else 0xFFFF

    def increment_program_counter(self) -> None:
        self.increment_register(self.P)

    def get_external_flag(self, id: int) -> int:
        return self.EF[id - 1]

    def set_external_flag(self, id: int, val: int) -> None:
        if id not in [1, 2, 3, 4]: raise IndexError
        if val not in [0, 1]: raise ValueError
        self.EF[id - 1] = val
