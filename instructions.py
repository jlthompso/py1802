from __future__ import annotations
import states
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cpu import CPU


def decode(cpu: CPU, I: int, N: int):
    match I, N:
        case 0x0, 0x0:  IDL(cpu)
        case 0x0, N:    LDN(cpu, N)
        case 0x1, N:    INC(cpu, N)
        case 0x2, N:    DEC(cpu, N)
        case 0x4, N:    LDA(cpu, N)
        case 0x5, N:    STR(cpu, N)
        case 0x6, 0x0:  IRX(cpu)
        case 0x7, 0x2:  LDXA(cpu)
        case 0x7, 0x3:  STXD(cpu)
        case 0x7, 0xA:  REQ(cpu)
        case 0x7, 0xB:  SEQ(cpu)
        case 0x8, N:    GLO(cpu, N)
        case 0x9, N:    GHI(cpu, N)
        case 0xA, N:    PLO(cpu, N)
        case 0xB, N:    PHI(cpu, N)
        case 0xC, 0x4:  NOP(cpu)
        case 0xD, N:    SEP(cpu, N)
        case 0xE, N:    SEX(cpu, N)
        case 0xF, 0x0:  LDX(cpu)
        case 0xF, 0x8:  LDI(cpu)
        case _, _: raise NotImplementedError("Attempted to execute invalid instruction.")


def DEC(cpu: CPU, N: int):
    # Decrement Register N (0x2N)
    #   R(N)-1
    cpu.decrement_register(N)
    cpu.set_state(states.Fetch())


def IDL(cpu: CPU):
    # Idle (0x00):
    #   M(R(0))-->BUS
    cpu.BUS = cpu.M[cpu.R[0]]


def INC(cpu: CPU, N: int):
    # Increment Register N (0x1N):
    #   R(N)+1
    cpu.increment_register(N)
    cpu.set_state(states.Fetch())


def IRX(cpu: CPU):
    # Increment Register X (0x60)
    #   R(X)+1
    cpu.increment_register(cpu.X)
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


def LDA(cpu: CPU, N: int):
    # Load Advance (0x4N):
    #   M(R(N))-->D; R(N)+1
    cpu.D = cpu.M[cpu.R[N]]
    cpu.increment_register(N)
    cpu.set_state(states.Fetch())


def LDI(cpu: CPU):
    # Load Immediate (0xF8)
    #   M(R(P))-->D; R(P)+1
    cpu.D = cpu.M[cpu.R[cpu.P]]
    cpu.R[cpu.P] += 1
    cpu.set_state(states.Fetch())


def LDN(cpu: CPU, N: int):
    # Load via N (0x0N):
    #   M(R(N))-->D (for N>0)
    cpu.D = cpu.M[cpu.R[N]]
    cpu.set_state(states.Fetch())


def LDX(cpu: CPU):
    # Load via X (0xF0):
    #   M(R(X))-->D
    cpu.D = cpu.M[cpu.R[cpu.X]]
    cpu.set_state(states.Fetch())


def LDXA(cpu: CPU):
    # Load via X and Advance (0x72):
    #   M(R(X))-->D; R(X)+1
    cpu.D = cpu.M[cpu.R[cpu.X]]
    cpu.increment_register(cpu.X)
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


def REQ(cpu: CPU):
    # Reset Q (0x7A)
    #   0-->Q
    cpu.Q = 0
    cpu.set_state(states.Fetch())


def SEP(cpu: CPU, N: int):
    # Set P (0xDN)
    #   N-->P
    cpu.P = N
    cpu.set_state(states.Fetch())


def SEQ(cpu: CPU):
    # Set Q (0x7B)
    #   1-->Q
    cpu.Q = 1
    cpu.set_state(states.Fetch())


def SEX(cpu: CPU, N: int):
    # Set X (0xEN)
    #   N-->X
    cpu.X = N
    cpu.set_state(states.Fetch())


def STR(cpu: CPU, N: int):
    # Store via N (0x5N)
    #   D-->M(R(N))
    cpu.M[cpu.R[N]] = cpu.D
    cpu.set_state(states.Fetch())


def STXD(cpu: CPU):
    # Store via X and Decrement (0x73)
    #   D-->M(R(X)); R(X)-1
    cpu.M[cpu.R[cpu.X]] = cpu.D
    cpu.decrement_register(cpu.X)
    cpu.set_state(states.Fetch())
