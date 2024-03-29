import unittest
from cpu import CPU
from common_test_functions import force_three_cycle_instruction
from states import Fetch


class InternalTests(unittest.TestCase):
    def test_increment_program_counter(self):
        cpu = CPU()
        cpu.run()

        expected = 5
        opcode = 0xC4  # NOP
        pc_reg = 0
        executions = 5

        force_three_cycle_instruction(cpu, opcode, executions)
        self.assertEqual(expected, cpu.R[pc_reg])  # PC should increment for each fetch
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

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

    def test_set_external_flag(self):
        cpu = CPU()

        self.assertEqual(0, cpu.get_external_flag(3))
        cpu.set_external_flag(3, 1)
        self.assertEqual(1, cpu.get_external_flag(3))


if __name__ == '__main__':
    unittest.main()
