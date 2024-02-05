import unittest
from cpu import CPU
from common_test_functions import force_two_cycle_instruction, force_three_cycle_instruction
from states import Fetch, Execute


class ShortBranchTests(unittest.TestCase):
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

    def test_BN(self):
        cpu = CPU()
        cpu.run()

        for ef in range(1, 5):
            expected = 0x1242
            opcode = 0x34 + ef - 1  # B1/B2/B3/B4
            pc = 0x1234
            pc_reg = 0
            payload = 0x5542
            branch = True

            cpu.P = pc_reg
            cpu.R[pc_reg] = pc
            cpu.M[pc + 1] = payload
            cpu.set_external_flag(ef, int(branch))
            force_two_cycle_instruction(cpu, opcode)
            self.assertEqual(expected, cpu.R[pc_reg])  # PC should jump to low byte stored in next mem address
            self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_BN_no_branch(self):
        cpu = CPU()
        cpu.run()

        for ef in range(1, 5):
            expected = 0x1236
            opcode = 0x34 + ef - 1  # B1/B2/B3/B4
            pc = 0x1234
            pc_reg = 0
            payload = 0x5542
            branch = False

            cpu.P = pc_reg
            cpu.R[pc_reg] = pc
            cpu.M[pc + 1] = payload
            cpu.set_external_flag(ef, int(branch))
            force_two_cycle_instruction(cpu, opcode)
            self.assertEqual(expected, cpu.R[pc_reg])  # PC should skip next byte
            self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_BNN(self):
        cpu = CPU()
        cpu.run()

        for ef in range(1, 5):
            expected = 0x1242
            opcode = 0x3C + ef - 1  # BN1/BN2/BN3/BN4
            pc = 0x1234
            pc_reg = 0
            payload = 0x5542
            branch = True

            cpu.P = pc_reg
            cpu.R[pc_reg] = pc
            cpu.M[pc + 1] = payload
            cpu.set_external_flag(ef, int(not branch))
            force_two_cycle_instruction(cpu, opcode)
            self.assertEqual(expected, cpu.R[pc_reg])  # PC should jump to low byte stored in next mem address
            self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_BNN_no_branch(self):
        cpu = CPU()
        cpu.run()

        for ef in range(1, 5):
            expected = 0x1236
            opcode = 0x3C + ef - 1  # BN1/BN2/BN3/BN4
            pc = 0x1234
            pc_reg = 0
            payload = 0x5542
            branch = False

            cpu.P = pc_reg
            cpu.R[pc_reg] = pc
            cpu.M[pc + 1] = payload
            cpu.set_external_flag(ef, int(not branch))
            force_two_cycle_instruction(cpu, opcode)
            self.assertEqual(expected, cpu.R[pc_reg])  # PC should skip next byte
            self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0


class LongBranchTests(unittest.TestCase):
    def test_LBZ(self):
        cpu = CPU()
        cpu.run()

        expected = 0x5542
        opcode = 0xC2  # LBZ
        pc = 0x1234
        pc_reg = 0
        payload = [0x55, 0x42]
        branch = True

        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = payload[0]
        cpu.M[pc + 2] = payload[1]
        cpu.D = int(not branch)
        force_three_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.R[pc_reg])  # PC should jump to word stored in next two mem addresses
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_LBZ_no_branch(self):
        cpu = CPU()
        cpu.run()

        expected = 0x1237
        opcode = 0xC2  # LBZ
        pc = 0x1234
        pc_reg = 0
        payload = [0x55, 0x42]
        branch = False

        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = payload[0]
        cpu.M[pc + 2] = payload[1]
        cpu.D = int(not branch)
        force_three_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.R[pc_reg])  # PC should skip next two bytes
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_LBNZ(self):
        cpu = CPU()
        cpu.run()

        expected = 0x5542
        opcode = 0xCA  # LBNZ
        pc = 0x1234
        pc_reg = 0
        payload = [0x55, 0x42]
        branch = True

        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = payload[0]
        cpu.M[pc + 2] = payload[1]
        cpu.D = int(branch)
        force_three_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.R[pc_reg])  # PC should jump to word stored in next two mem addresses
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0

    def test_LBNZ_no_branch(self):
        cpu = CPU()
        cpu.run()

        expected = 0x1237
        opcode = 0xCA  # LBNZ
        pc = 0x1234
        pc_reg = 0
        payload = [0x55, 0x42]
        branch = False

        cpu.P = pc_reg
        cpu.R[pc_reg] = pc
        cpu.M[pc + 1] = payload[0]
        cpu.M[pc + 2] = payload[1]
        cpu.D = int(branch)
        force_three_cycle_instruction(cpu, opcode)
        self.assertEqual(expected, cpu.R[pc_reg])  # PC should skip next two bytes
        self.assertIsInstance(cpu._state, Fetch)  # CPU should be in S0


if __name__ == '__main__':
    unittest.main()
