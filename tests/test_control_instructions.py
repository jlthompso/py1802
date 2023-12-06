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
        self.assertEqual(expected, cpu.R[pc_reg])
        self.assertIsInstance(cpu._state, Fetch)


if __name__ == '__main__':
    unittest.main()
