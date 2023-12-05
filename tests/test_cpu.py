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

    def test_increment_register(self):
        cpu = CPU()

        expected = 9
        reg = 0
        executions = 10
        init_val = 0xFFFF

        cpu.R[reg] = init_val
        for _ in range(executions): cpu.increment_register(reg)
        self.assertEqual(expected, cpu.R[reg])  # register value should roll over to zero after 0xFFFF

    def test_decrement_register(self):
        cpu = CPU()

        expected = 0xFFF6
        reg = 10
        executions = 10

        for _ in range(executions): cpu.decrement_register(reg)
        self.assertEqual(expected, cpu.R[reg])  # register value should roll over to 0xFFFF after zero


if __name__ == '__main__':
    unittest.main()
