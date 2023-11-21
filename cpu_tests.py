import unittest
from cpu import CPU, ControlMode


class ControlModeTests(unittest.TestCase):
    def test_init_mode(self):
        cpu = CPU()
        self.assertFalse(cpu.CLEAR)
        self.assertTrue(cpu.WAIT)

    def test_set_load_mode(self):
        cpu = CPU()
        cpu.set_control_mode(ControlMode.LOAD)
        self.assertFalse(cpu.CLEAR)
        self.assertFalse(cpu.WAIT)

    def test_set_reset_mode(self):
        cpu = CPU()
        cpu.set_control_mode(ControlMode.RESET)
        self.assertFalse(cpu.CLEAR)
        self.assertTrue(cpu.WAIT)

    def test_set_pause_mode(self):
        cpu = CPU()
        cpu.set_control_mode(ControlMode.PAUSE)
        self.assertTrue(cpu.CLEAR)
        self.assertFalse(cpu.WAIT)

    def test_set_run_mode(self):
        cpu = CPU()
        cpu.set_control_mode(ControlMode.RUN)
        self.assertTrue(cpu.CLEAR)
        self.assertTrue(cpu.WAIT)

    def test_tick(self):
        cpu = CPU()
        cpu.set_control_mode(ControlMode.RUN)
        self.assertEqual(0, cpu.R[0])
        for _ in range(10): cpu.tick()
        self.assertEqual(10, cpu.R[0])


if __name__ == '__main__':
    unittest.main()
