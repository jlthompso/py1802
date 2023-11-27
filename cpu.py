from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


class CPU:
    _state: State = None

    def __init__(self) -> None:
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

    def set_state(self, state: State) -> None:
        self._state = state
        self._state.context = self

    def tick(self) -> None:
        self._state.tick()


class State(ABC):
    def __init__(self) -> None:
        self._context: Optional[CPU] = None

    @property
    def context(self) -> CPU:
        return self._context

    @context.setter
    def context(self, context: CPU) -> None:
        self._context = context

    @abstractmethod
    def tick(self) -> None:
        pass


class Reset(State):
    def tick(self) -> None:
        self.context.I = 0x0
        self.context.N = 0x0
        self.context.Q = 0
        self.context.IE = 1


class Run(State):
    def tick(self) -> None:
        self.context.R[self.context.P] = (self.context.R[self.context.P] + 1) % 0xFFFF
