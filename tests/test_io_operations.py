import unittest
from cpu import CPU
from common_test_functions import force_two_cycle_instruction, force_three_cycle_instruction
from states import Fetch


class InputOutputByteTransferTests(unittest.TestCase):
    def test_OUT(self):
        cpu = CPU()
        cpu.run()

        expected_data = 42
        expected_mem_addr = 0x1235
        opcode = 0x62  # OUT (N = 010)
        mem_addr = 0x1234
        reg = 4

        cpu.X = reg
        cpu.R[reg] = mem_addr
        cpu.M[mem_addr] = expected_data
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_data, cpu.BUS)  # Data bus should contain contents of memory address
        self.assertEqual((opcode & 0x4) >> 2, cpu.N2)  # N2 should equal third least significant bit of N
        self.assertEqual((opcode & 0x2) >> 1, cpu.N1)  # N1 should equal second least significant bit of N
        self.assertEqual((opcode & 0x1), cpu.N0)  # N0 should equal least significant bit of N
        self.assertEqual(expected_mem_addr, cpu.R[reg])  # Memory address should increment
        self.assertEqual(expected_data, cpu.M[mem_addr])  # Memory should not be modified
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

        opcode = 0xC4  # NOP
        force_three_cycle_instruction(cpu, opcode)
        self.assertEqual(0, cpu.N2)  # N2 should be reset
        self.assertEqual(0, cpu.N1)  # N1 should be reset
        self.assertEqual(0, cpu.N0)  # N0 should be reset

    def test_INP(self):
        cpu = CPU()
        cpu.run()

        expected_data = 42
        opcode = 0x6A  # OUT (N = 010)
        mem_addr = 0x1234
        reg = 4

        cpu.X = reg
        cpu.R[reg] = mem_addr
        cpu.BUS = expected_data & 0xFF
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_data, cpu.M[mem_addr])  # Memory should contain contents of BUS
        self.assertEqual(expected_data, cpu.D)  # D should contain contents of BUS
        self.assertEqual((opcode & 0x4) >> 2, cpu.N2)  # N2 should equal third least significant bit of N
        self.assertEqual((opcode & 0x2) >> 1, cpu.N1)  # N1 should equal second least significant bit of N
        self.assertEqual((opcode & 0x1), cpu.N0)  # N0 should equal least significant bit of N
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

        opcode = 0xC4  # NOP
        force_three_cycle_instruction(cpu, opcode)
        self.assertEqual(0, cpu.N2)  # N2 should be reset
        self.assertEqual(0, cpu.N1)  # N1 should be reset
        self.assertEqual(0, cpu.N0)  # N0 should be reset


if __name__ == '__main__':
    unittest.main()
