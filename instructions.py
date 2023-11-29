from __future__ import annotations
import states
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cpu import CPU


def decode(cpu: CPU, I: int, N: int):
    match I, N:
        case 0x0, 0x0:
            IDL(cpu)
        case 0x0, N:
            LDN(cpu, N)
        case 0x1, N:
            INC(cpu, N)
        case 0xC, 0x4:
            NOP(cpu)
        case _, _:
            raise NotImplementedError("Attempted to execute invalid instruction.")


def IDL(cpu: CPU):
    # Idle (0x00):
    #   M(R(0))-->BUS
    cpu.BUS = cpu.M[cpu.R[0]]


def LDN(cpu: CPU, N: int):
    # Load via N (0x0N):
    #   M(R(N))-->D (for N>0)
    cpu.D = cpu.R[N]
    cpu.set_state(states.Fetch())


def INC(cpu: CPU, N: int):
    # Increment Register N (0x1N):
    #   R(N)+1
    cpu.R[cpu.N] = (cpu.R[N] + 1) % 0xFFFF
    cpu.set_state(states.Fetch())


def NOP(cpu: CPU):
    # No Operation (0xC4):
    #   CONTINUE
    cpu.set_state(states.ForceExecute())
    cpu.tick()


