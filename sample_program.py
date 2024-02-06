from cpu import CPU
import keyboard
import sys


opcodes = [0x90, 0xB6, 0xF8, 0x29, 0xA6, 0xE0, 0x64, 0x00, 0xE6, 0x3F, 0x09, 0x6C, 0x64, 0x37, 0x0D, 0xF8, 0x60,0xA6,
           0xE0, 0x64, 0x01, 0x3F, 0x15, 0xE6, 0x6C, 0x64, 0x37, 0x1A, 0xE0, 0x64, 0x02, 0xE6, 0x3F, 0x20, 0x6C, 0x64,
           0x37, 0x24, 0x26, 0x26, 0x46, 0xC4, 0xC4, 0x26, 0x56, 0x64, 0x7A, 0xCA, 0x00, 0x20, 0x7B, 0x30, 0x20]


def main():
    cpu = CPU()
    for i, opcode in enumerate(opcodes): cpu.M[i] = opcode  # load program into memory

    # run program starting at memory address 0x00
    cpu.run()
    while True:
        cpu.tick()
        print(f"Q: {cpu.Q}\tDATA: 0x{'{:<4x}'.format(cpu.BUS)}\tEF: {''.join([str(val) for val in cpu.EF])}", end='\r')

        # process keyboard events
        for ef in range(1, 5):
            if keyboard.is_pressed(str(ef)):
                cpu.toggle_external_flag(ef)
                while keyboard.is_pressed(str(ef)): ...

        if keyboard.is_pressed('p'):
            print(f"\nExecution paused at instruction {hex(cpu.R[cpu.P])}. Press 'enter' to resume.")
            while not keyboard.is_pressed('enter'):
                if keyboard.is_pressed('esc'): exit(0)

        if keyboard.is_pressed('esc'): exit(0)

        if keyboard.is_pressed('i'):
            while keyboard.is_pressed('i'): flush_input()
            print("\nEnter data bus value: ", end='')
            if len(user_input := input()):
                val = int(user_input, 0)
                if 0 <= val <= 0xFF: cpu.BUS = val
                cpu.set_external_flag(4, 1)
                cpu.tick()
                cpu.tick()
                cpu.set_external_flag(4, 0)
                cpu.tick()
                cpu.tick()

        if keyboard.is_pressed('r'):
            cpu.reset()
            cpu.run()


def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)


def exit(val):
    print('\nExiting...')
    flush_input()
    sys.exit(val)


if __name__ == '__main__':
    main()
