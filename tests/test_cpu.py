import unittest
from cpu import CPU
from common_test_functions import force_two_cycle_instruction


class InternalTests(unittest.TestCase):
    def test_increment_program_counter(self):
        cpu = CPU()
        cpu.run()

        expected = 5
        opcode = 0xC4  # NOP
        pc_reg = 0
        executions = 5

        force_two_cycle_instruction(cpu, opcode, executions)
        self.assertEqual(expected, cpu.R[pc_reg])  # PC should increment for each fetch

    def test_program_counter_overflow(self):
        cpu = CPU()
        cpu.run()

        expected = 5
        opcode = 0xC4  # NOP
        pc_reg = 1
        executions = 0xFFFF + 5

        cpu.P = pc_reg
        force_two_cycle_instruction(cpu, opcode, executions)
        self.assertEqual(expected, cpu.R[pc_reg])  # PC should roll over to zero after 0xFFFF fetches


if __name__ == '__main__':
    unittest.main()
