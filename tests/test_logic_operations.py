import unittest
from cpu import CPU
from common_test_functions import force_two_cycle_instruction
from states import Fetch


class LogicOperationTests(unittest.TestCase):
    def test_OR(self):
        cpu = CPU()
        cpu.run()

        expected = {
            (0, 0): 0,
            (0, 1): 1,
            (1, 0): 1,
            (1, 1): 1,
        }
        opcode = 0xF1  # OR
        reg = 8
        mem_addr = 0x1111

        cpu.X = reg
        cpu.R[reg] = mem_addr
        for (a, b), result in expected.items():
            cpu.M[mem_addr] = a
            cpu.D = b
            force_two_cycle_instruction(cpu, opcode)
            self.assertEqual(result, cpu.D)  # D should contain result of operation
            self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_ORI(self):
        cpu = CPU()
        cpu.run()

        expected = {
            (0, 0, 0x1235): 0,
            (0, 1, 0x1237): 1,
            (1, 0, 0x1239): 1,
            (1, 1, 0x123B): 1,
        }
        opcode = 0xF9  # ORI
        pc = 0x1234
        pc_reg = 0

        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        for (a, b, operand_addr), result in expected.items():
            cpu.M[operand_addr] = a
            cpu.D = b
            force_two_cycle_instruction(cpu, opcode)
            self.assertEqual(result, cpu.D)  # D should contain result of operation
            self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0
            self.assertEqual(operand_addr + 1, cpu.R[pc_reg])  # PC should increment to immediate operand

    def test_XOR(self):
        cpu = CPU()
        cpu.run()

        expected = {
            (0, 0): 0,
            (0, 1): 1,
            (1, 0): 1,
            (1, 1): 0,
        }
        opcode = 0xF3  # XOR
        reg = 8
        mem_addr = 0x1111

        cpu.X = reg
        cpu.R[reg] = mem_addr
        for (a, b), result in expected.items():
            cpu.M[mem_addr] = a
            cpu.D = b
            force_two_cycle_instruction(cpu, opcode)
            self.assertEqual(result, cpu.D)  # D should contain result of operation
            self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_XRI(self):
        cpu = CPU()
        cpu.run()

        expected = {
            (0, 0, 0x1235): 0,
            (0, 1, 0x1237): 1,
            (1, 0, 0x1239): 1,
            (1, 1, 0x123B): 0,
        }
        opcode = 0xFB  # XRI
        pc = 0x1234
        pc_reg = 0

        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        for (a, b, operand_addr), result in expected.items():
            cpu.M[operand_addr] = a
            cpu.D = b
            force_two_cycle_instruction(cpu, opcode)
            self.assertEqual(result, cpu.D)  # D should contain result of operation
            self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0
            self.assertEqual(operand_addr + 1, cpu.R[pc_reg])  # PC should increment to immediate operand

    def test_AND(self):
        cpu = CPU()
        cpu.run()

        expected = {
            (0, 0): 0,
            (0, 1): 0,
            (1, 0): 0,
            (1, 1): 1,
        }
        opcode = 0xF2  # AND
        reg = 8
        mem_addr = 0x1111

        cpu.X = reg
        cpu.R[reg] = mem_addr
        for (a, b), result in expected.items():
            cpu.M[mem_addr] = a
            cpu.D = b
            force_two_cycle_instruction(cpu, opcode)
            self.assertEqual(result, cpu.D)  # D should contain result of operation
            self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_ANI(self):
        cpu = CPU()
        cpu.run()

        expected = {
            (0, 0, 0x1235): 0,
            (0, 1, 0x1237): 0,
            (1, 0, 0x1239): 0,
            (1, 1, 0x123B): 1,
        }
        opcode = 0xFA  # ANI
        pc = 0x1234
        pc_reg = 0

        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        for (a, b, operand_addr), result in expected.items():
            cpu.M[operand_addr] = a
            cpu.D = b
            force_two_cycle_instruction(cpu, opcode)
            self.assertEqual(result, cpu.D)  # D should contain result of operation
            self.assertEqual(operand_addr + 1, cpu.R[pc_reg])  # PC should increment to immediate operand
            self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SHR_carry_zero(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0b00010000
        expected_carry = 0
        opcode = 0xF6  # SHR
        operand = 0b00100000

        cpu.D = operand
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be divided by two
        self.assertEqual(expected_carry, cpu.DF)  # DF should contain previous LSB
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SHR_carry_one(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0b01111111
        expected_carry = 1
        opcode = 0xF6  # SHR
        operand = 0b11111111

        cpu.D = operand
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be divided by two
        self.assertEqual(expected_carry, cpu.DF)  # DF should contain previous LSB
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SHRC_carry_zero(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0b10010000
        expected_carry = 0
        opcode = 0x76  # SHRC
        operand = 0b00100000
        carry_bit = 1

        cpu.D = operand
        cpu.DF = carry_bit
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be shifted one bit right and MSB should be previous DF
        self.assertEqual(expected_carry, cpu.DF)  # DF should contain previous LSB
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SHRC_carry_one(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0b00010000
        expected_carry = 1
        opcode = 0x76  # SHRC
        operand = 0b00100001
        carry_bit = 0

        cpu.D = operand
        cpu.DF = carry_bit
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be shifted one bit right and MSB should be previous DF
        self.assertEqual(expected_carry, cpu.DF)  # DF should contain previous LSB
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SHL_carry_zero(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0b00100000
        expected_carry = 0
        opcode = 0xFE  # SHL
        operand = 0b00010000

        cpu.D = operand
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be multiplied by two
        self.assertEqual(expected_carry, cpu.DF)  # DF should contain previous MSB
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SHL_carry_one(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0b10100010
        expected_carry = 0
        opcode = 0xFE  # SHL
        operand = 0b01010001

        cpu.D = operand
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be multiplied by two
        self.assertEqual(expected_carry, cpu.DF)  # DF should contain previous MSB
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SHLC_carry_zero(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0b01000001
        expected_carry = 0
        opcode = 0x7E  # SHLC
        operand = 0b00100000
        carry_bit = 1

        cpu.D = operand
        cpu.DF = carry_bit
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be shifted one bit left and MSB should be previous DF
        self.assertEqual(expected_carry, cpu.DF)  # DF should contain previous MSB
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SHLC_carry_one(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0b11100001
        expected_carry = 1
        opcode = 0x7E  # SHLC
        operand = 0b11110000
        carry_bit = 1

        cpu.D = operand
        cpu.DF = carry_bit
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be shifted one bit left and MSB should be previous DF
        self.assertEqual(expected_carry, cpu.DF)  # DF should contain previous MSB
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0


if __name__ == '__main__':
    unittest.main()
