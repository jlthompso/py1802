import unittest
from cpu import CPU
from common_test_functions import force_two_cycle_instruction
from states import Fetch


class ArithmeticOperationTests(unittest.TestCase):
    def test_ADD(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x85
        expected_carry = 0
        opcode = 0xF4  # ADD
        operands = [0x3A, 0x4B]
        reg = 2
        mem_addr = 0x1234

        cpu.D = operands[0]
        cpu.M[mem_addr] = operands[1]
        cpu.R[reg] = mem_addr
        cpu.X = reg
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be sum
        self.assertEqual(expected_carry, cpu.DF)  # addition shouldn't carry
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_ADD_with_carry(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x2A
        expected_carry = 1
        opcode = 0xF4  # ADD
        operands = [0x3A, 0xF0]
        reg = 2
        mem_addr = 0x1234

        cpu.D = operands[0]
        cpu.M[mem_addr] = operands[1]
        cpu.R[reg] = mem_addr
        cpu.X = reg
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be sum
        self.assertEqual(expected_carry, cpu.DF)  # addition should carry
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_ADI(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x85
        expected_carry = 0
        opcode = 0xFC  # ADI
        operands = [0x3A, 0x4B]
        pc = 0x1234
        pc_reg = 0

        cpu.D = operands[0]
        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = operands[1]
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be sum
        self.assertEqual(expected_carry, cpu.DF)  # addition shouldn't carry
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_ADI_with_carry(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x2A
        expected_carry = 1
        opcode = 0xFC  # ADI
        operands = [0x3A, 0xF0]
        pc = 0x1234
        pc_reg = 0

        cpu.D = operands[0]
        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = operands[1]
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be sum
        self.assertEqual(expected_carry, cpu.DF)  # addition should carry
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_ADC(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x68
        expected_carry = 0
        opcode = 0x74  # ADC
        operands = [0x3A, 0x2D]
        data_flag = 1
        reg = 2
        mem_addr = 0x1234

        cpu.D = operands[0]
        cpu.DF = data_flag
        cpu.M[mem_addr] = operands[1]
        cpu.R[reg] = mem_addr
        cpu.X = reg
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be sum
        self.assertEqual(expected_carry, cpu.DF)  # addition shouldn't carry
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_ADC_with_carry(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x00
        expected_carry = 1
        opcode = 0x74  # ADC
        operands = [0xC2, 0x3D]
        data_flag = 1
        reg = 2
        mem_addr = 0x1234

        cpu.D = operands[0]
        cpu.DF = data_flag
        cpu.M[mem_addr] = operands[1]
        cpu.R[reg] = mem_addr
        cpu.X = reg
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be sum
        self.assertEqual(expected_carry, cpu.DF)  # addition should carry
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_ADCI(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x86
        expected_carry = 0
        opcode = 0x7C  # ADCI
        operands = [0x3A, 0x4B]
        data_flag = 1
        pc = 0x1234
        pc_reg = 0

        cpu.D = operands[0]
        cpu.DF = data_flag
        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = operands[1]
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be sum
        self.assertEqual(expected_carry, cpu.DF)  # addition shouldn't carry
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_ADCI_with_carry(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x00
        expected_carry = 1
        opcode = 0x7C  # ADCI
        operands = [0xC2, 0x3D]
        data_flag = 1
        pc = 0x1234
        pc_reg = 0

        cpu.D = operands[0]
        cpu.DF = data_flag
        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = operands[1]
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be sum
        self.assertEqual(expected_carry, cpu.DF)  # addition shouldn't carry
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0


if __name__ == '__main__':
    unittest.main()
