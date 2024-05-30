import io
import os
import sys
import argparse
from cpu import CPU
import keyboard


def main(source_file: io.TextIOWrapper) -> None:
    cpu = CPU()
    load_mem(source_file, cpu)
    disp_header(source_file.name)

    keyboard.add_hotkey('ctrl+1', lambda: cpu.toggle_external_flag(1))
    keyboard.add_hotkey('ctrl+2', lambda: cpu.toggle_external_flag(2))
    keyboard.add_hotkey('ctrl+3', lambda: cpu.toggle_external_flag(3))
    keyboard.add_hotkey('ctrl+4', lambda: cpu.toggle_external_flag(4))

    cpu.run()
    while True:
        cpu.tick()
        disp_cpu_status(cpu)

        if keyboard.is_pressed('space'):
            main_menu(cpu, source_file.name)

        if keyboard.is_pressed('esc'): exit(0)

        if keyboard.is_pressed('ctrl+r'):
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
    sys.stdin.flush()
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


def clear():
    os.system('cls')


def disp_header(fname, truncate=False):
    clear()
    print(f"Executing {fname}")
    if not truncate:
        print("<Esc> to exit.")
        print("<Space> to open main menu.")
        print("<Ctrl+R> to reset processor.")
        print("<Ctrl+[1:4]> to toggle external flag.")


def disp_cpu_status(cpu):
    print(f"DATA: 0x{'{:02X}'.format(cpu.BUS)}\tQ: {cpu.Q}\tEF1-4: {''.join([str(val) for val in cpu.EF])}"
          f"\t{'Running' if cpu.running else 'Paused'}", end='\r')


def main_menu(cpu, fname):
    while True:
        disp_header(fname, truncate=True)
        disp_cpu_status(cpu)
        print(f"\nExecution halted at instruction {hex(cpu.R[cpu.P])}.")
        print("[1] Run")
        print("[2] Pause")
        print("[3] Reset")
        print("[4] Modify External Flags")
        print("[5] Write Data Bus")
        flush_input()
        match input("Enter menu option or leave blank to resume program execution >> "):
            case "":
                break
            case "1":
                cpu.run()
                break
            case "2":
                cpu.pause()
                break
            case "3":
                cpu.reset()
                cpu.run()
                break
            case "4":
                while True:
                    disp_header(fname, truncate=True)
                    disp_cpu_status(cpu)
                    ef = input("\nEnter external flag number (1/2/3/4) or leave blank to exit menu >> ")
                    if not ef: break
                    if ef in ['1', '2', '3', '4']: cpu.EF[int(ef) - 1] ^= 1
            case "5":
                if user_input := input("Hex data bus value >> "):
                    val = int(user_input, 0)
                    if 0 <= val <= 0xFF:
                        cpu.BUS = val
                    else:
                        print("Invalid data bus value.")

    disp_header(fname)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute assembly code on an emulated RCA 1802 processor.')
    parser.add_argument('infile', type=argparse.FileType('r'))
    args = parser.parse_args()
    main(args.infile)
    exit(0)
