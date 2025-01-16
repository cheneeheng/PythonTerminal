import cmd
import sys
from typing import List, Optional


class TerminalUI(cmd.Cmd):
    """A simple terminal CLI UI with command history."""

    intro = 'Welcome to the Terminal UI. Type help or ? to list commands.\n'
    prompt = '> '

    def __init__(self) -> None:
        super().__init__()
        self.command_history: List[str] = []

    def precmd(self, line: str) -> str:
        """Store command in history before execution."""
        if line and not line.startswith(('history', '?', 'help')):
            self.command_history.append(line)
        return line

    def do_history(self, arg: str) -> None:
        """Show command history. Usage: history"""
        if not self.command_history:
            print("No commands in history.")
            return

        for idx, command in enumerate(self.command_history, 1):
            print(f"{idx}. {command}")

    def do_clear(self, arg: str) -> None:
        """Clear the screen. Usage: clear"""
        print('\n' * 100)

    def do_echo(self, arg: str) -> None:
        """Echo the input string. Usage: echo [message]"""
        print(arg)

    def do_exit(self, arg: str) -> bool:
        """Exit the terminal UI. Usage: exit"""
        print("Goodbye!")
        return True

    def emptyline(self) -> bool:
        """Do nothing on empty line."""
        return False

    # Aliases
    do_quit = do_exit
    do_bye = do_exit

    def do_shell(self, arg: str) -> None:
        """Execute a system command. Usage: shell [command]"""
        import subprocess
        try:
            output = subprocess.check_output(arg, shell=True, text=True)
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    def do_history_clear(self, arg: str) -> None:
        """Clear command history. Usage: history_clear"""
        self.command_history.clear()
        print("Command history cleared.")

    def default(self, line: str) -> None:
        """Handle unknown commands."""
        print(f"Unknown command: {line}")
        print("Type 'help' or '?' to see available commands.")

    def completenames(self, text: str, *ignored) -> List[str]:
        """Enable tab completion for commands."""
        commands = [cmd[3:] for cmd in self.get_names() if cmd.startswith('do_')]
        return [cmd for cmd in commands if cmd.startswith(text)]


def main() -> None:
    terminal = TerminalUI()
    try:
        terminal.cmdloop()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)


if __name__ == '__main__':
    main()
