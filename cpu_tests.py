import unittest
from cpu import CPU


class InternalTests(unittest.TestCase):
    def test_increment_program_counter(self):
        cpu = CPU()
        cpu.run()
        # PC should increment for each fetch
        for _ in range(10):
            cpu.I, cpu.N = 0xC, 0x4  # NOP
            cpu.tick()
        self.assertEqual(5, cpu.R[0])  # NOP requires two cycles
        # IDL shouldn't increment PC
        for _ in range(10):
            cpu.I, cpu.N = 0x0, 0x0  # IDL
            cpu.tick()
        self.assertEqual(6, cpu.R[0])
        # PC should roll over to 0 after 0xFFFF
        for _ in range(2 * 0xFFFF):
            cpu.I, cpu.N = 0xC, 0x4  # NOP
            cpu.tick()
        self.assertEqual(6, cpu.R[0])


class RegisterOperationsTests(unittest.TestCase):
    def test_INC(self):
        cpu = CPU()
        cpu.run()
        # register value should increment
        for _ in range(10):
            cpu.I, cpu.N = 0x1, 0x1  # INC R(1)
            cpu.tick()
        self.assertEqual(5, cpu.R[1])
        # register value should roll over to 0 after 0xFFFF
        for _ in range(2 * 0xFFFF + 10):
            cpu.I, cpu.N = 0x1, 0x1  # INC R(1)
            cpu.tick()
        self.assertEqual(10, cpu.R[1])

    def test_DEC(self):
        cpu = CPU()
        cpu.run()
        # register value should roll over to 0xFFFF after 0
        for _ in range(2):
            cpu.I, cpu.N = 0x2, 0x1  # DEC R(1)
            cpu.tick()
        self.assertEqual(0xFFFF, cpu.R[1])
        # register value should decrement
        for _ in range(10):
            cpu.I, cpu.N = 0x2, 0x1  # DEC R(1)
            cpu.tick()
        self.assertEqual(0xFFFA, cpu.R[1])

    def test_IRX(self):
        cpu = CPU()
        cpu.run()
        cpu.X = 5
        # register value should increment
        for _ in range(10):
            cpu.I, cpu.N = 0x6, 0x0  # INC R(X)
            cpu.tick()
        self.assertEqual(5, cpu.R[5])
        # register value should roll over to 0 after 0xFFFF
        for _ in range(2 * 0xFFFF + 10):
            cpu.I, cpu.N = 0x6, 0x0  # INC R(X)
            cpu.tick()
        self.assertEqual(10, cpu.R[5])

    def test_GLO(self):
        cpu = CPU()
        cpu.run()
        cpu.R[3] = 0x1234
        cpu.N = 0x3
        cpu.tick()
        # D should be set to low byte of R(3)
        cpu.I, cpu.N = 0x8, 0x3
        cpu.tick()  # 2 cycle instruction
        self.assertEqual(0x34, cpu.D)

    def test_PLO(self):
        cpu = CPU()
        cpu.run()
        cpu.N = 0x3
        cpu.R[3] = 0xFFFF
        cpu.D = 0x42
        cpu.tick()
        # Low byte of R(4) should be set to D
        cpu.I, cpu.N = 0xA, 0x3
        cpu.tick()  # 2 cycle instruction
        self.assertEqual(0xFF42, cpu.R[3])

    def test_GHI(self):
        cpu = CPU()
        cpu.run()
        cpu.R[3] = 0x1234
        cpu.N = 0x3
        cpu.tick()
        # D should be set to high byte of R(3)
        cpu.I, cpu.N = 0x9, 0x3
        cpu.tick()  # 2 cycle instruction
        self.assertEqual(0x12, cpu.D)

    def test_PHI(self):
        cpu = CPU()
        cpu.run()
        cpu.N = 0x3
        cpu.R[3] = 0xFFFF
        cpu.D = 0x42
        cpu.tick()
        # High byte of R(4) should be set to D
        cpu.I, cpu.N = 0xB, 0x3
        cpu.tick()  # 2 cycle instruction
        self.assertEqual(0x42FF, cpu.R[3])


if __name__ == '__main__':
    unittest.main()
