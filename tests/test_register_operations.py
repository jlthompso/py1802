import unittest
from cpu import CPU
from common_test_functions import force_two_cycle_instruction
from states import Fetch


class RegisterOperationsTests(unittest.TestCase):
    def test_INC(self):
        cpu = CPU()
        cpu.run()

        expected = 5
        opcode = 0x11  # INC R(1)
        executions = 5

        force_two_cycle_instruction(cpu, opcode, executions)
        self.assertEqual(expected, cpu.R[opcode & 0xF])  # register value should increment
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_DEC(self):
        cpu = CPU()
        cpu.run()

        expected = 0xFFFB
        opcode = 0x21  # DEC R(1)
        executions = 5

        force_two_cycle_instruction(cpu, opcode, executions)
        self.assertEqual(expected, cpu.R[opcode & 0xF])  # register value should roll over to 0xFFFF then decrement
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_IRX(self):
        cpu = CPU()
        cpu.run()

        expected = 5
        opcode = 0x60  # INC R(X)
        reg = 5
        executions = 5

        cpu.X = reg
        force_two_cycle_instruction(cpu, opcode, executions)
        self.assertEqual(expected, cpu.R[reg])  # register X value should increment
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_GLO(self):
        cpu = CPU()
        cpu.run()

        expected = 0x34
        opcode = 0x83  # GLO R(3)
        data = 0x1234

        cpu.R[opcode & 0xF] = data
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.D)  # D should be set to low byte of R(3)
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_PLO(self):
        cpu = CPU()
        cpu.run()

        expected = 0xFF42
        opcode = 0xA3  # PLO R(3)
        reg_contents = 0xFFFF
        data = 0x42

        cpu.R[opcode & 0xF] = reg_contents
        cpu.D = data
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.R[opcode & 0xF])  # Low byte of R(3) should be set to D
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_GHI(self):
        cpu = CPU()
        cpu.run()

        expected = 0x12
        opcode = 0x93  # GHI R(3)
        data = 0x1234

        cpu.R[opcode & 0xF] = data
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.D)  # D should be set to high byte of R(3)
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_PHI(self):
        cpu = CPU()
        cpu.run()

        expected = 0x42FF
        opcode = 0xB3  # PHI R(3)
        reg_contents = 0xFFFF
        data = 0x42

        cpu.R[opcode & 0xF] = reg_contents
        cpu.D = data
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.R[3])  # High byte of R(3) should be set to D
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0


if __name__ == '__main__':
    unittest.main()
