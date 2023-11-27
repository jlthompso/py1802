from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


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

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def pause(self) -> None:
        pass


class Reset(State):
    def tick(self) -> None:
        self.context.I = 0
        self.context.N = 0
        self.context.Q = 0
        self.context.IE = 1
        self.context.BUS = 0

    def reset(self) -> None:
        self.context.tick()

    def run(self) -> None:
        self.context.set_state(Init())
        self.context.tick()

    def pause(self) -> None:
        self.context.set_state(Pause(prev_state=self))
        self.context.tick()


class Init(State):
    def tick(self) -> None:
        self.context.X = 0
        self.context.P = 0
        self.context.R[0] = 0

        self.context.set_state(Fetch())

    def reset(self) -> None:
        self.context.set_state(Reset())
        self.context.tick()

    def run(self) -> None:
        pass  # not implemented, INIT state is only entered when transitioning from RESET to RUN

    def pause(self) -> None:
        self.context.set_state(Pause(prev_state=self))
        self.context.tick()


class Pause(State):
    def __init__(self, prev_state):
        super().__init__()
        self._prev_state = prev_state

    def tick(self) -> None:
        pass  # do nothing

    def reset(self) -> None:
        self.context.set_state(Reset())
        self.context.tick()

    def run(self) -> None:
        self.context.set_state(self._prev_state)
        self.context.tick()

    def pause(self) -> None:
        self.context.tick()


class Fetch(State):
    def tick(self) -> None:
        opcode = self.context.M[self.context.R[self.context.P]]
        self.context.I = (opcode >> 4) & 0x0F
        self.context.N = opcode & 0x0F
        self.context.R[self.context.P] = (self.context.R[self.context.P] + 1) % 0xFFFF  # increment program counter
        self.context.set_state(Execute())

    def reset(self) -> None:
        self.context.set_state(Reset())
        self.context.tick()

    def run(self) -> None:
        self.context.tick()

    def pause(self) -> None:
        self.context.set_state(Pause(prev_state=self))
        self.context.tick()


class Execute(State):
    def tick(self) -> None:
        match self.context.I, self.context.N:
            case 0x0, 0x0:
                # IDL (00): idle
                #   M(R(0))-->BUS
                self.context.BUS = self.context.M[self.context.R[0]]
            case 0x0, N:
                # LDN (0N): load via N
                #   M(R(N))-->D (for N>0)
                self.context.D = self.context.R[N]
                self.context.set_state(Fetch())
            case 0x1, N:
                # INC: increment register N
                #   R(N)+1
                self.context.R[self.context.N] = (self.context.R[N] + 1) % 0xFFFF
                self.context.set_state(Fetch())
            case 0xC, 0x4:
                # NOP: no operation
                #   continue
                self.context.set_state(ForceExecute())
                self.context.tick()
            case _, _:
                raise NotImplementedError("Attempted to execute invalid instruction.")

    def reset(self) -> None:
        self.context.set_state(Reset())
        self.context.tick()

    def run(self) -> None:
        self.context.tick()

    def pause(self) -> None:
        self.context.set_state(Pause(prev_state=self))
        self.context.tick()


class ForceExecute(State):
    def tick(self) -> None:
        self.context.set_state(Fetch())

    def reset(self) -> None:
        self.context.set_state(Reset())
        self.context.tick()

    def run(self) -> None:
        self.context.tick()

    def pause(self) -> None:
        self.context.set_state(Pause(prev_state=self))
        self.context.tick()