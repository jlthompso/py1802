import unittest
from cpu import CPU
from common_test_functions import force_two_cycle_instruction
from states import Fetch, Execute


class BranchingTests(unittest.TestCase):
    def test_BR(self):
        cpu = CPU()
        cpu.run()

        expected = 0x1242
        opcode = 0x30  # BR
        pc = 0x1234
        pc_reg = 0
        payload = 0x5542

        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = payload
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.R[pc_reg])  # PC should jump to low byte stored in next mem address
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0


if __name__ == '__main__':
    unittest.main()
