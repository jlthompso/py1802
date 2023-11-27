import unittest
from cpu import CPU


class InternalTests(unittest.TestCase):
    def test_increment_program_counter(self):
        cpu = CPU()
        cpu.run()
        self.assertEqual(0, cpu.P)
        self.assertEqual(0, cpu.R[0])
        for _ in range(10):
            cpu.I, cpu.N = 0xC, 0x4  # NOP
            cpu.tick()
        self.assertEqual(5, cpu.R[0])
        for _ in range(5):
            cpu.I, cpu.N = 0x0, 0x0  # IDL
            cpu.tick()
        self.assertEqual(6, cpu.R[0])


class RegisterOperationsTests(unittest.TestCase):
    def test_INC(self):
        cpu = CPU()
        cpu.run()
        self.assertEqual(0, cpu.R[1])
        for _ in range(10):
            cpu.I, cpu.N = 0x1, 0x1  # INC R(1)
            cpu.tick()
        self.assertEqual(5, cpu.R[1])

    def test_INC_rollover(self):
        cpu = CPU()
        cpu.run()
        self.assertEqual(0, cpu.R[1])
        for _ in range(2 * 0xFFFF + 10):
            cpu.I, cpu.N = 0x1, 0x1  # INC R(1)
            cpu.tick()
        self.assertEqual(5, cpu.R[1])


if __name__ == '__main__':
    unittest.main()
