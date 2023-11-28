from __future__ import annotations
from typing import TYPE_CHECKING
from states import Reset
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

        self.BUS = 0            # Data Bus, 8b

        self.M = [0]*(2**16)    # Standard RAM and ROM up to 65,536B

    def set_state(self, state: State) -> None:
        self._state = state
        self._state.context = self

    def tick(self) -> None:
        self._state.tick()

    def reset(self) -> None:
        self._state.reset()

    def run(self) -> None:
        self._state.run()

    def pause(self) -> None:
        self._state.pause()
