from __future__ import annotations
import states
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cpu import CPU


def decode(cpu: CPU, I: int, N: int):
    match I, N:
        case 0x0, 0x0: IDL(cpu)
        case 0x0, N: LDN(cpu, N)
        case 0x1, N: INC(cpu, N)
        case 0x2, N: DEC(cpu, N)
        case 0x6, 0x0: IRX(cpu)
        case 0x8, N: GLO(cpu, N)
        case 0x9, N: GHI(cpu, N)
        case 0xA, N: PLO(cpu, N)
        case 0xB, N: PHI(cpu, N)
        case 0xC, 0x4: NOP(cpu)
        case _, _:
            raise NotImplementedError("Attempted to execute invalid instruction.")


def DEC(cpu: CPU, N: int):
    # Decrement Register N (0x2N)
    #   R(N)-1
    cpu.R[N] = cpu.R[N] - 1 if cpu.R[N] - 1 >= 0 else 0xFFFF
    cpu.set_state(states.Fetch())


def IDL(cpu: CPU):
    # Idle (0x00):
    #   M(R(0))-->BUS
    cpu.BUS = cpu.M[cpu.R[0]]


def INC(cpu: CPU, N: int):
    # Increment Register N (0x1N):
    #   R(N)+1
    cpu.R[N] = (cpu.R[N] + 1) % 0xFFFF
    cpu.set_state(states.Fetch())


def IRX(cpu: CPU):
    # Increment Register X (0x60)
    #   R(X)+1
    cpu.R[cpu.X] = (cpu.R[cpu.X] + 1) % 0xFFFF
    cpu.set_state(states.Fetch())


def GHI(cpu: CPU, N: int):
    # Get High Register N
    #   R(N).1-->D
    cpu.D = (cpu.R[N] >> 8) & 0xFF
    cpu.set_state(states.Fetch())


def GLO(cpu: CPU, N: int):
    # Get Low Register N
    #   R(N).0-->D
    cpu.D = cpu.R[N] & 0xFF
    cpu.set_state(states.Fetch())


def LDN(cpu: CPU, N: int):
    # Load via N (0x0N):
    #   M(R(N))-->D (for N>0)
    cpu.D = cpu.R[N]
    cpu.set_state(states.Fetch())


def PHI(cpu: CPU, N: int):
    # Put High Register N
    #   D-->R(N).1
    cpu.R[N] &= ((cpu.D << 8) & 0xFF00) | 0x00FF
    cpu.set_state(states.Fetch())


def PLO(cpu: CPU, N: int):
    # Put Low Register N
    #   D-->R(N).0
    cpu.R[N] &= 0xFF00 + cpu.D
    cpu.set_state(states.Fetch())


def NOP(cpu: CPU):
    # No Operation (0xC4):
    #   CONTINUE
    cpu.set_state(states.ForceExecute())
    cpu.tick()


