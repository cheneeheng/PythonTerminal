import cmd
import sys
import tkinter as tk
from tkinter import scrolledtext
from typing import List, Optional
from queue import Queue
from threading import Thread


class TerminalUI(cmd.Cmd):
    """A simple terminal CLI UI with command history."""

    intro = 'Welcome to the Terminal UI. Type help or ? to list commands.\n'
    prompt = '> '

    def __init__(self, output_queue: Queue) -> None:
        super().__init__()
        self.command_history: List[str] = []
        self.output_queue = output_queue
        self.stdout_original = sys.stdout
        sys.stdout = self

    def write(self, text: str) -> None:
        """Override write to redirect output to queue."""
        self.output_queue.put(text)

    def flush(self) -> None:
        """Required for stdout compatibility."""
        pass


class TerminalWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Terminal UI")
        self.root.geometry("600x400")
        
        # Create text widget
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both')
        
        # Create input field
        self.input_field = tk.Entry(self.root)
        self.input_field.pack(fill='x', padx=5, pady=5)
        self.input_field.bind('<Return>', self.handle_input)
        
        # Queue for communication between CLI and GUI
        self.output_queue: Queue = Queue()
        
        # Create CLI instance
        self.cli = TerminalUI(self.output_queue)
        
        # Start CLI in separate thread
        self.cli_thread = Thread(target=self.cli.cmdloop, daemon=True)
        self.cli_thread.start()
        
        # Start output checking
        self.check_output()
        
        # Display intro message
        self.text_area.insert(tk.END, self.cli.intro)
        self.text_area.insert(tk.END, self.cli.prompt)
        
        self.input_field.focus()

    def handle_input(self, event: Optional[tk.Event] = None) -> None:
        """Handle input from the entry field."""
        command = self.input_field.get()
        self.text_area.insert(tk.END, f"{command}\n")
        self.input_field.delete(0, tk.END)
        
        # Process the command
        self.cli.onecmd(command)
        self.text_area.insert(tk.END, self.cli.prompt)
        self.text_area.see(tk.END)

    def check_output(self) -> None:
        """Check for new output in the queue."""
        while not self.output_queue.empty():
            text = self.output_queue.get()
            self.text_area.insert(tk.END, text)
            self.text_area.see(tk.END)
        self.root.after(100, self.check_output)

    def run(self) -> None:
        """Start the GUI main loop."""
        self.root.mainloop()


def main() -> None:
    terminal_window = TerminalWindow()
    try:
        terminal_window.run()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)


if __name__ == '__main__':
    main()
