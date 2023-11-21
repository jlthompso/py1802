import unittest
from cpu import CPU, Run


class ControlModeTests(unittest.TestCase):
    def test_tick(self):
        cpu = CPU()
        self.assertEqual(0, cpu.R[0])
        cpu.set_state(Run())
        for _ in range(10): cpu.tick()
        self.assertEqual(10, cpu.R[0])


if __name__ == '__main__':
    unittest.main()
