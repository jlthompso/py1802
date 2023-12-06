import unittest
from cpu import CPU
from common_test_functions import force_two_cycle_instruction, force_three_cycle_instruction
from states import Fetch, Execute


class ControlInstructionTests(unittest.TestCase):
    def test_IDL(self):
        cpu = CPU()
        cpu.run()

        expected = 1
        opcode = 0x00  # IDL
        pc_reg = 0
        executions = 5

        force_two_cycle_instruction(cpu, opcode, executions)
        self.assertEqual(expected, cpu.R[pc_reg])  # PC shouldn't increment after first fetch
        self.assertIsInstance(cpu._state, Execute)  # CPU should be in S1

    def test_NOP(self):
        cpu = CPU()
        cpu.run()

        expected = 0x31
        opcode = 0xC4  # NOP
        pc_reg = 0
        pc = 0x30

        cpu.R[pc_reg] = pc
        force_three_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.R[pc_reg])  # PC should increment
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SEP(self):
        cpu = CPU()
        cpu.run()

        expected = 5
        opcode = 0xD5  # SEP

        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.P)  # PC register should be set to N
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SEX(self):
        cpu = CPU()
        cpu.run()

        expected = 5
        opcode = 0xE5  # SEX

        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.X)  # X register should be set to N
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SEQ(self):
        cpu = CPU()
        cpu.run()

        expected = 1
        opcode = 0x7B  # SEQ

        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.Q)  # Q register should be set
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_REQ(self):
        cpu = CPU()
        cpu.run()

        expected = 0
        opcode = 0x7A  # REQ

        cpu.Q = 1
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.Q)  # Q register should be reset
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0


if __name__ == '__main__':
    unittest.main()
