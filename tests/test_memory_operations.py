import unittest
from cpu import CPU
from common_test_functions import force_two_cycle_instruction


class MemoryReferenceTests(unittest.TestCase):
    def test_LDN(self):
        cpu = CPU()
        cpu.run()

        expected = 42
        opcode = 0x09
        mem_addr = 0x1234

        cpu.M[mem_addr] = expected
        cpu.R[opcode & 0xF] = mem_addr
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.D)  # D should contain contents of mem_addr

    def test_LDN_ignores_reg_zero(self):
        cpu = CPU()
        cpu.run()

        expected = 0
        opcode = 0x00  # IDL
        mem_addr = 0x1234

        cpu.M[mem_addr] = expected
        cpu.R[opcode & 0xF] = mem_addr
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.D)  # D should not be modified (0x00 is IDL, not LDN)

    def test_LDA(self):
        cpu = CPU()
        cpu.run()

        expected = 0x1235
        opcode = 0x49
        mem_addr = 0x1234

        cpu.R[opcode & 0xF] = mem_addr
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.R[opcode & 0xF])  # D should contain contents of mem_addr

    def test_LDA_overflow(self):
        cpu = CPU()
        cpu.run()

        expected = 0x0000
        opcode = 0x45
        mem_addr = 0xFFFF

        cpu.R[opcode & 0xF] = mem_addr
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.R[opcode & 0xF])  # D should contain contents of mem_addr


if __name__ == '__main__':
    unittest.main()