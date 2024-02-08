import io
import sys
import argparse
from cpu import CPU
import keyboard


def main(source_file: io.TextIOWrapper) -> None:
    cpu = CPU()
    load_mem(source_file, cpu)

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


def load_mem(source_file: io.TextIOWrapper, cpu: CPU) -> None:
    for line in source_file:
        if line.startswith(';'): continue
        tokens = line.split()
        if len(tokens) < 2: raise SyntaxError("Lines must contain at least memory address and opcode.")

        try:
            addr = int(tokens[0], 16)
            opcodes = [int(tokens[1][i:i + 2], 16) for i in range(0, len(tokens[1]), 2)]
        except ValueError:
            print(f'Invalid syntax: {line}')
            exit(1)

        for i, opcode in enumerate(opcodes):
            cpu.M[addr + i] = opcode
    source_file.close()


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
    parser = argparse.ArgumentParser(description='Execute assembly code on an emulated RCA 1802 processor.')
    parser.add_argument('infile', type=argparse.FileType('r'))
    args = parser.parse_args()
    main(args.infile)
    exit(0)
