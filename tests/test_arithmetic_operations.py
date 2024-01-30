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

    def test_SD(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x34
        expected_borrow = 1
        opcode = 0xF5  # SD
        operands = [0x42, 0x0E]
        reg = 2
        mem_addr = 0x1234

        cpu.D = operands[1]
        cpu.M[mem_addr] = operands[0]
        cpu.R[reg] = mem_addr
        cpu.X = reg
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(expected_borrow, cpu.DF)  # subtraction shouldn't borrow
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SD_with_borrow(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0xCB
        expected_borrow = 0
        opcode = 0xF5  # SD
        operands = [0x42, 0x77]
        reg = 2
        mem_addr = 0x1234

        cpu.D = operands[1]
        cpu.M[mem_addr] = operands[0]
        cpu.R[reg] = mem_addr
        cpu.X = reg
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(expected_borrow, cpu.DF)  # subtraction should borrow
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SDI(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x34
        expected_borrow = 1
        opcode = 0xFD  # SDI
        operands = [0x42, 0x0E]
        pc = 0x1234
        pc_reg = 0

        cpu.D = operands[1]
        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = operands[0]
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(expected_borrow, cpu.DF)  # subtraction shouldn't borrow
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SDI_with_carry(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0xCB
        expected_borrow = 0
        opcode = 0xFD  # SDI
        operands = [0x42, 0x77]
        pc = 0x1234
        pc_reg = 0

        cpu.D = operands[1]
        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = operands[0]
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(expected_borrow, cpu.DF)  # subtraction should borrow
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SDB_positive(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x32
        expected_borrow = 0
        opcode = 0x75  # SDB
        operands = [0x64, 0x32]
        reg = 5
        mem_addr = 0x0042
        borrow = 0

        cpu.D = operands[1]
        cpu.M[mem_addr] = operands[0]
        cpu.R[reg] = mem_addr
        cpu.X = reg
        cpu.DF = ~borrow & 0x01
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(~expected_borrow & 0x01, cpu.DF)  # subtraction shouldn't borrow
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SDB_negative(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x7F
        expected_borrow = 1
        opcode = 0x75  # SDB
        operands = [0x71, 0xF2]
        reg = 5
        mem_addr = 0x0042
        borrow = 0

        cpu.D = operands[1]
        cpu.M[mem_addr] = operands[0]
        cpu.R[reg] = mem_addr
        cpu.X = reg
        cpu.DF = ~borrow & 0x01
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(~expected_borrow & 0x01, cpu.DF)  # subtraction should borrow
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SDB_with_borrow_positive(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x1F
        expected_borrow = 0
        opcode = 0x75  # SDB
        operands = [0x40, 0x20]
        reg = 5
        mem_addr = 0x0042
        borrow = 1

        cpu.D = operands[1]
        cpu.M[mem_addr] = operands[0]
        cpu.R[reg] = mem_addr
        cpu.X = reg
        cpu.DF = ~borrow & 0x01
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(~expected_borrow & 0x01, cpu.DF)  # subtraction shouldn't borrow
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SDB_with_borrow_negative(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x88
        expected_borrow = 1
        opcode = 0x75  # SDB
        operands = [0x4A, 0xC1]
        reg = 5
        mem_addr = 0x0042
        borrow = 1

        cpu.D = operands[1]
        cpu.M[mem_addr] = operands[0]
        cpu.R[reg] = mem_addr
        cpu.X = reg
        cpu.DF = ~borrow & 0x01
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(~expected_borrow & 0x01, cpu.DF)  # subtraction should borrow
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SDBI_positive(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x32
        expected_borrow = 0
        opcode = 0x7D  # SDBI
        operands = [0x64, 0x32]
        pc_reg = 5
        pc = 0x0042
        borrow = 0

        cpu.D = operands[1]
        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = operands[0]
        cpu.DF = ~borrow & 0x01
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(~expected_borrow & 0x01, cpu.DF)  # subtraction shouldn't borrow
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SDBI_negative(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x7F
        expected_borrow = 1
        opcode = 0x7D  # SDBI
        operands = [0x71, 0xF2]
        pc_reg = 5
        pc = 0x0042
        borrow = 0

        cpu.D = operands[1]
        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = operands[0]
        cpu.DF = ~borrow & 0x01
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(~expected_borrow & 0x01, cpu.DF)  # subtraction should borrow
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SDBI_with_borrow_positive(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x1F
        expected_borrow = 0
        opcode = 0x7D  # SDBI
        operands = [0x40, 0x20]
        pc_reg = 5
        pc = 0x0042
        borrow = 1

        cpu.D = operands[1]
        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = operands[0]
        cpu.DF = ~borrow & 0x01
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(~expected_borrow & 0x01, cpu.DF)  # subtraction shouldn't borrow
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SDBI_with_borrow_negative(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x88
        expected_borrow = 1
        opcode = 0x7D  # SDBI
        operands = [0x4A, 0xC1]
        pc_reg = 5
        pc = 0x0042
        borrow = 1

        cpu.D = operands[1]
        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = operands[0]
        cpu.DF = ~borrow & 0x01
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(~expected_borrow & 0x01, cpu.DF)  # subtraction should borrow
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SM(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x34
        expected_borrow = 1
        opcode = 0xF7  # SM
        operands = [0x42, 0x0E]
        reg = 2
        mem_addr = 0x1234

        cpu.D = operands[0]
        cpu.M[mem_addr] = operands[1]
        cpu.R[reg] = mem_addr
        cpu.X = reg
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(expected_borrow, cpu.DF)  # subtraction shouldn't borrow
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SMI(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x34
        expected_borrow = 1
        opcode = 0xFF  # SMI
        operands = [0x42, 0x0E]
        pc = 0x1234
        pc_reg = 0

        cpu.D = operands[0]
        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = operands[1]
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(expected_borrow, cpu.DF)  # subtraction shouldn't borrow
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SMI_with_carry(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0xCB
        expected_borrow = 0
        opcode = 0xFF  # SMI
        operands = [0x42, 0x77]
        pc = 0x1234
        pc_reg = 0

        cpu.D = operands[0]
        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = operands[1]
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(expected_borrow, cpu.DF)  # subtraction should borrow
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SMB_positive(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x32
        expected_borrow = 0
        opcode = 0x77  # SMB
        operands = [0x64, 0x32]
        reg = 5
        mem_addr = 0x0042
        borrow = 0

        cpu.D = operands[0]
        cpu.M[mem_addr] = operands[1]
        cpu.R[reg] = mem_addr
        cpu.X = reg
        cpu.DF = ~borrow & 0x01
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(~expected_borrow & 0x01, cpu.DF)  # subtraction shouldn't borrow
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SMB_negative(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x7F
        expected_borrow = 1
        opcode = 0x77  # SMB
        operands = [0x71, 0xF2]
        reg = 5
        mem_addr = 0x0042
        borrow = 0

        cpu.D = operands[0]
        cpu.M[mem_addr] = operands[1]
        cpu.R[reg] = mem_addr
        cpu.X = reg
        cpu.DF = ~borrow & 0x01
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(~expected_borrow & 0x01, cpu.DF)  # subtraction should borrow
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SMB_with_borrow_positive(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x1F
        expected_borrow = 0
        opcode = 0x77  # SMB
        operands = [0x40, 0x20]
        reg = 5
        mem_addr = 0x0042
        borrow = 1

        cpu.D = operands[0]
        cpu.M[mem_addr] = operands[1]
        cpu.R[reg] = mem_addr
        cpu.X = reg
        cpu.DF = ~borrow & 0x01
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(~expected_borrow & 0x01, cpu.DF)  # subtraction shouldn't borrow
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SMB_with_borrow_negative(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x88
        expected_borrow = 1
        opcode = 0x77  # SMB
        operands = [0x4A, 0xC1]
        reg = 5
        mem_addr = 0x0042
        borrow = 1

        cpu.D = operands[0]
        cpu.M[mem_addr] = operands[1]
        cpu.R[reg] = mem_addr
        cpu.X = reg
        cpu.DF = ~borrow & 0x01
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(~expected_borrow & 0x01, cpu.DF)  # subtraction should borrow
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SMBI_positive(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x32
        expected_borrow = 0
        opcode = 0x7F  # SMBI
        operands = [0x64, 0x32]
        pc_reg = 5
        pc = 0x0042
        borrow = 0

        cpu.D = operands[0]
        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = operands[1]
        cpu.DF = ~borrow & 0x01
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(~expected_borrow & 0x01, cpu.DF)  # subtraction shouldn't borrow
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SMBI_negative(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x7F
        expected_borrow = 1
        opcode = 0x7F  # SMBI
        operands = [0x71, 0xF2]
        pc_reg = 5
        pc = 0x0042
        borrow = 0

        cpu.D = operands[0]
        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = operands[1]
        cpu.DF = ~borrow & 0x01
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(~expected_borrow & 0x01, cpu.DF)  # subtraction should borrow
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SMBI_with_borrow_positive(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x1F
        expected_borrow = 0
        opcode = 0x7F  # SMBI
        operands = [0x40, 0x20]
        pc_reg = 5
        pc = 0x0042
        borrow = 1

        cpu.D = operands[0]
        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = operands[1]
        cpu.DF = ~borrow & 0x01
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(~expected_borrow & 0x01, cpu.DF)  # subtraction shouldn't borrow
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_SMBI_with_borrow_negative(self):
        cpu = CPU()
        cpu.run()

        expected_val = 0x88
        expected_borrow = 1
        opcode = 0x7F  # SMBI
        operands = [0x4A, 0xC1]
        pc_reg = 5
        pc = 0x0042
        borrow = 1

        cpu.D = operands[0]
        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = operands[1]
        cpu.DF = ~borrow & 0x01
        force_two_cycle_instruction(cpu, opcode)
        self.assertEqual(expected_val, cpu.D)  # D should be difference
        self.assertEqual(~expected_borrow & 0x01, cpu.DF)  # subtraction should borrow
        self.assertEqual(0, cpu.M[pc])  # Memory should not be modified
        self.assertEqual(pc + 2, cpu.R[pc_reg])  # PC should advance to next instruction
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0


if __name__ == '__main__':
    unittest.main()
