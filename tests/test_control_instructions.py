import unittest
from cpu import CPU
from common_test_functions import force_two_cycle_instruction


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


if __name__ == '__main__':
    unittest.main()
