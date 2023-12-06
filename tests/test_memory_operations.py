import unittest
from cpu import CPU
from common_test_functions import force_two_cycle_instruction
from states import Fetch, Execute


class MemoryReferenceTests(unittest.TestCase):
    def test_LDN(self):
        cpu = CPU()
        cpu.run()

        expected = 42
        opcode = 0x09  # LDN R(9)
        mem_addr = 0x1234

        cpu.M[mem_addr] = expected
        cpu.R[opcode & 0xF] = mem_addr
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.D)  # D should contain contents of mem_addr
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

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
        self.assertEqual(expected, cpu.M[mem_addr])  # Memory should not be modified
        self.assertIsInstance(cpu._state, Execute)  # CPU should be in S1

    def test_LDA(self):
        cpu = CPU()
        cpu.run()

        expected_data = 42
        expected_mem_addr = 0x1235
        opcode = 0x49  # LDA R(9)
        mem_addr = 0x1234

        cpu.M[mem_addr] = expected_data
        cpu.R[opcode & 0xF] = mem_addr
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_data, cpu.D)  # D should contain contents of memory address
        self.assertEqual(expected_mem_addr, cpu.R[opcode & 0xF])  # Memory address should increment
        self.assertEqual(expected_data, cpu.M[mem_addr])  # Memory should not be modified
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_LDX(self):
        cpu = CPU()
        cpu.run()

        expected = 42
        opcode = 0xF0  # LDX
        reg = 2
        mem_addr = 0x1234

        cpu.M[mem_addr] = expected
        cpu.R[reg] = mem_addr
        cpu.X = reg
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.D)  # D should contain contents of memory address X
        self.assertEqual(expected, cpu.M[mem_addr])  # Memory should not be modified
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_LDXA(self):
        cpu = CPU()
        cpu.run()

        expected_data = 42
        expected_mem_addr = 0x1235
        opcode = 0x72  # LDXA
        reg = 6
        mem_addr = 0x1234

        cpu.M[mem_addr] = expected_data
        cpu.R[reg] = mem_addr
        cpu.X = reg
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_data, cpu.D)  # D should contain contents of memory address
        self.assertEqual(expected_mem_addr, cpu.R[reg])  # Memory address should increment
        self.assertEqual(expected_data, cpu.M[mem_addr])  # Memory should not be modified
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_LDI(self):
        cpu = CPU()
        cpu.run()

        expected = 42
        opcode = 0xF8  # LDI
        pc = 0x1234
        pc_reg = 0

        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = expected
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.D)  # D should contain contents of memory at next program counter address
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_STR(self):
        cpu = CPU()
        cpu.run()

        expected = 222
        opcode = 0x5F  # STR R(15)
        mem_addr = 0x7300

        cpu.D = expected
        cpu.R[opcode & 0xF] = mem_addr
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.M[mem_addr])  # Memory address should contain value of D
        self.assertEqual(expected, cpu.D)  # D should not be modified
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_STXD(self):
        cpu = CPU()
        cpu.run()

        expected_data = 57
        expected_mem_addr = 0x5554
        opcode = 0x73  # STXD
        reg = 6
        mem_addr = 0x5555

        cpu.D = expected_data
        cpu.X = reg
        cpu.R[reg] = mem_addr
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_data, cpu.M[mem_addr])  # Memory address should contain value of D
        self.assertEqual(expected_mem_addr, cpu.R[reg])  # Register value should decrement
        self.assertEqual(expected_data, cpu.D)  # D should not be modified
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0


if __name__ == '__main__':
    unittest.main()
