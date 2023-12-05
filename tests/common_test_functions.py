from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cpu import CPU


def force_two_cycle_instruction(cpu: CPU, opcode: int, repeat: int = 1):
    for _ in range(repeat):
        cpu.tick()  # fetch
        cpu.I, cpu.N = (opcode >> 4) & 0xF, opcode & 0xF  # overwrite fetched instruction
        cpu.tick()  # execute
