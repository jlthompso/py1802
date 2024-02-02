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
        case 0x3, 0x0:  BR(cpu)
        case 0x4, N:    LDA(cpu, N)
        case 0x5, N:    STR(cpu, N)
        case 0x6, 0x0:  IRX(cpu)
        case 0x7, 0x2:  LDXA(cpu)
        case 0x7, 0x3:  STXD(cpu)
        case 0x7, 0x4:  ADC(cpu)
        case 0x7, 0x5:  SDB(cpu)
        case 0x7, 0x6:  SHRC(cpu)
        case 0x7, 0x7:  SMB(cpu)
        case 0x7, 0xA:  REQ(cpu)
        case 0x7, 0xB:  SEQ(cpu)
        case 0x7, 0xC:  ADCI(cpu)
        case 0x7, 0xD:  SDBI(cpu)
        case 0x7, 0xE:  SHLC(cpu)
        case 0x7, 0xF:  SMBI(cpu)
        case 0x8, N:    GLO(cpu, N)
        case 0x9, N:    GHI(cpu, N)
        case 0xA, N:    PLO(cpu, N)
        case 0xB, N:    PHI(cpu, N)
        case 0xC, 0x4:  NOP(cpu)
        case 0xD, N:    SEP(cpu, N)
        case 0xE, N:    SEX(cpu, N)
        case 0xF, 0x0:  LDX(cpu)
        case 0xF, 0x1:  OR(cpu)
        case 0xF, 0x2:  AND(cpu)
        case 0xF, 0x3:  XOR(cpu)
        case 0xF, 0x4:  ADD(cpu)
        case 0xF, 0x5:  SD(cpu)
        case 0xF, 0x6:  SHR(cpu)
        case 0xF, 0x7:  SM(cpu)
        case 0xF, 0x8:  LDI(cpu)
        case 0xF, 0x9:  ORI(cpu)
        case 0xF, 0xA:  ANI(cpu)
        case 0xF, 0xB:  XRI(cpu)
        case 0xF, 0xC:  ADI(cpu)
        case 0xF, 0xD:  SDI(cpu)
        case 0xF, 0xE:  SHL(cpu)
        case 0xF, 0xF:  SMI(cpu)
        case _, _: raise NotImplementedError("Attempted to execute invalid instruction.")


def ADC(cpu: CPU):
    # ADC (0x74)
    #   M(R(X))+D+DF-->DF,D
    cpu.DF = 0 if (sum := cpu.D + cpu.M[cpu.R[cpu.X]] + cpu.DF) <= 0xFF else 1
    cpu.D = sum & 0xFF
    cpu.set_state(states.Fetch())


def ADCI(cpu: CPU):
    # ADCI (0x7C)
    #   M(R(P))+D+DF-->DF,D; R(P)+1
    cpu.DF = 0 if (sum := cpu.D + cpu.M[cpu.R[cpu.P]] + cpu.DF) <= 0xFF else 1
    cpu.R[cpu.P] += 1
    cpu.D = sum & 0xFF
    cpu.set_state(states.Fetch())


def ADD(cpu: CPU):
    # ADD (0xF4)
    #   M(R(X))+D-->DF,D
    cpu.DF = 0 if (sum := cpu.D + cpu.M[cpu.R[cpu.X]]) <= 0xFF else 1
    cpu.D = sum & 0xFF
    cpu.set_state(states.Fetch())


def ADI(cpu: CPU):
    # ADI (0xFC)
    #   M(R(P))+D-->DF,D; R(P)+1
    cpu.DF = 0 if (sum := cpu.D + cpu.M[cpu.R[cpu.P]]) <= 0xFF else 1
    cpu.R[cpu.P] += 1
    cpu.D = sum & 0xFF
    cpu.set_state(states.Fetch())


def AND(cpu: CPU):
    # AND (0xF2)
    #   M(R(X)) AND D-->D
    cpu.D &= cpu.M[cpu.R[cpu.X]]
    cpu.set_state(states.Fetch())


def ANI(cpu: CPU):
    # ANI (0xFA)
    #   M(R(P)) AND D-->R(P)+1
    cpu.D &= cpu.M[cpu.R[cpu.P]]
    cpu.increment_register(cpu.P)
    cpu.set_state(states.Fetch())


def BR(cpu: CPU):
    # BR (0x30)
    #   M(R(P))-->R(P).0
    cpu.R[cpu.P] = (cpu.R[cpu.P] & 0xFF00) | (cpu.M[cpu.R[cpu.P]] & 0xFF)
    cpu.set_state(states.Fetch())


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


def NOP(cpu: CPU):
    # No Operation (0xC4):
    #   CONTINUE
    cpu.set_state(states.ForceExecute())


def OR(cpu: CPU):
    # OR (0xF1)
    #   M(R(X)) OR D-->D
    cpu.D |= cpu.M[cpu.R[cpu.X]]
    cpu.set_state(states.Fetch())


def ORI(cpu: CPU):
    # ORI (0xF9)
    #   M(R(P)) OR D-->R(P)+1
    cpu.D |= cpu.M[cpu.R[cpu.P]]
    cpu.increment_register(cpu.P)
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


def REQ(cpu: CPU):
    # Reset Q (0x7A)
    #   0-->Q
    cpu.Q = 0
    cpu.set_state(states.Fetch())


def SD(cpu: CPU):
    # Subtract D (0xF5)
    #   M(R(X))-D-->DF,D
    cpu.DF = 0 if (diff := cpu.M[cpu.R[cpu.X]] + (~cpu.D & 0xFF) + 1) <= 0xFF else 1
    cpu.D = diff & 0xFF
    cpu.set_state(states.Fetch())


def SDB(cpu: CPU):
    # Subtract D with Borrow (0x75)
    #   M(R(X))-D-(NOT DF)-->DF,D
    cpu.DF = 0 if (diff := cpu.M[cpu.R[cpu.X]] + (~cpu.D & 0xFF) + cpu.DF) <= 0xFF else 1
    cpu.D = diff & 0xFF
    cpu.set_state(states.Fetch())


def SDBI(cpu: CPU):
    # Subtract D with Borrow Immediate (0x7D)
    #   M(R(P))-D-(NOT DF)-->DF,D; R(P)+1
    cpu.DF = 0 if (diff := cpu.M[cpu.R[cpu.P]] + (~cpu.D & 0xFF) + cpu.DF) <= 0xFF else 1
    cpu.R[cpu.P] += 1
    cpu.D = diff & 0xFF
    cpu.set_state(states.Fetch())


def SDI(cpu: CPU):
    # SDI (0xFD)
    #   M(R(P))-D-->DF,D; R(P)+1
    cpu.DF = 0 if (diff := cpu.M[cpu.R[cpu.P]] + (~cpu.D & 0xFF) + 1) <= 0xFF else 1
    cpu.R[cpu.P] += 1
    cpu.D = diff & 0xFF
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


def SHL(cpu: CPU):
    # Shift Left (0xFE)
    #   Shift D Left; MSB(D)-->DF; 0-->LSB(D)
    cpu.DF = cpu.D & 0x80
    cpu.D = (cpu.D << 1) & 0xFE
    cpu.set_state(states.Fetch())


def SHLC(cpu: CPU):
    # Shift Left with Carry (0x7E)
    #   Shift D Left; MSB(D)-->DF; DF-->LSB(D)
    msb = (cpu.D >> 7) & 0x01
    cpu.D = ((cpu.D << 1) & 0xFE) | cpu.DF
    cpu.DF = msb
    cpu.set_state(states.Fetch())


def SHR(cpu: CPU):
    # Shift Right (0xF6)
    #   Shift D Right; LSB(D)-->DF; 0-->MSB(D)
    cpu.DF = cpu.D & 0x01
    cpu.D = (cpu.D >> 1) & 0x7F
    cpu.set_state(states.Fetch())


def SHRC(cpu: CPU):
    # Shift Right with Carry (0x76)
    #   Shift D Right; LSB(D)-->DF; DF-->MSB(D)
    lsb = cpu.D & 0x01
    cpu.D = (cpu.D >> 1) | ((cpu.DF << 7) & 0x80)
    cpu.DF = lsb
    cpu.set_state(states.Fetch())


def SM(cpu: CPU):
    # Subtract Memory (0xF7)
    #   D-M(R(X))-->DF,D
    cpu.DF = 0 if (diff := cpu.D + (~cpu.M[cpu.R[cpu.X]] & 0xFF) + 1) <= 0xFF else 1
    cpu.D = diff & 0xFF
    cpu.set_state(states.Fetch())


def SMB(cpu: CPU):
    # Subtract Memory with Borrow (0x77)
    #   D-M(R(X))-(NOT DF)-->DF,D
    cpu.DF = 0 if (diff := cpu.D + (~cpu.M[cpu.R[cpu.X]] & 0xFF) + cpu.DF) <= 0xFF else 1
    cpu.D = diff & 0xFF
    cpu.set_state(states.Fetch())


def SMBI(cpu: CPU):
    # Subtract Memory with Borrow Immediate (0x7F)
    #   D-M(R(P))-(NOT DF)-->DF,D; R(P)+1
    cpu.DF = 0 if (diff := cpu.D + (~cpu.M[cpu.R[cpu.P]] & 0xFF) + cpu.DF) <= 0xFF else 1
    cpu.R[cpu.P] += 1
    cpu.D = diff & 0xFF
    cpu.set_state(states.Fetch())


def SMI(cpu: CPU):
    # Subtract Memory Immediate (0xFF)
    #   D-M(R(P))-->DF,D; R(P)+1
    cpu.DF = 0 if (diff := cpu.D + (~cpu.M[cpu.R[cpu.P]] & 0xFF) + 1) <= 0xFF else 1
    cpu.R[cpu.P] += 1
    cpu.D = diff & 0xFF
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


def XOR(cpu: CPU):
    # Exclusive-OR
    #   M(R(X)) XOR D-->D
    cpu.D ^= cpu.M[cpu.R[cpu.X]]
    cpu.set_state(states.Fetch())


def XRI(cpu: CPU):
    # Exclusive-OR Immediate
    #   M(R(P)) XOR D-->D; R(P)+1
    cpu.D ^= cpu.M[cpu.R[cpu.P]]
    cpu.increment_register(cpu.P)
    cpu.set_state(states.Fetch())
