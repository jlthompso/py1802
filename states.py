from __future__ import annotations
from abc import ABC, abstractmethod
from instructions import decode
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from cpu import CPU


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


class Execute(State):
    def tick(self) -> None:
        decode(self.context, self.context.I, self.context.N)

    def reset(self) -> None:
        self.context.set_state(Reset())
        self.context.tick()

    def run(self) -> None:
        self.context.tick()

    def pause(self) -> None:
        self.context.set_state(Pause(prev_state=self))
        self.context.tick()


class Fetch(State):
    def tick(self) -> None:
        opcode = self.context.M[self.context.R[self.context.P]]
        self.context.I = (opcode >> 4) & 0x0F
        self.context.N = opcode & 0x0F
        self.context.increment_register(self.context.P)  # increment program counter
        self.context.set_state(Execute())

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
