import os
import subprocess
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, Frame, Button, Label, StringVar

class FileExecutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Executor")
        self.root.geometry('600x400')  # Set the window size

        # Set up the main frame
        self.main_frame = Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create initial widgets
        self.create_main_menu()

    def create_main_menu(self):
        # Clear existing widgets
        self.clear_main_frame()

        # Title label
        self.title_label = Label(self.main_frame, text="File Executor Menu", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=(0, 20))

        # Buttons for different file types
        self.python_button = Button(self.main_frame, text="Execute Python Files", command=self.show_python_files, font=("Arial", 14), width=25)
        self.python_button.pack(pady=10)

        self.executable_button = Button(self.main_frame, text="Execute Executable Files", command=self.show_executable_files, font=("Arial", 14), width=25)
        self.executable_button.pack(pady=10)

        self.batch_button = Button(self.main_frame, text="Execute Batch Files", command=self.show_batch_files, font=("Arial", 14), width=25)
        self.batch_button.pack(pady=10)

        self.quit_button = Button(self.main_frame, text="Quit", command=self.root.quit, font=("Arial", 14), width=25)
        self.quit_button.pack(pady=(20, 0))

        # Status label
        self.status_var = StringVar()
        self.status_var.set("Select a file type to start.")
        self.status_label = Label(self.main_frame, textvariable=self.status_var, font=("Arial", 12), fg="blue")
        self.status_label.pack(pady=(10, 0))

    def list_files(self, extension):
        return [f for f in os.listdir('.') if f.endswith(extension)]

    def show_files(self, extension, file_type):
        self.clear_main_frame()
        files = self.list_files(extension)

        if not files:
            messagebox.showinfo("No Files Found", f"No {file_type} files found.")
            self.create_main_menu()
            return

        self.file_listbox = Listbox(self.main_frame, selectmode=tk.SINGLE, width=50, height=15)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the Listbox
        self.scrollbar = Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=self.scrollbar.set)

        for file in files:
            self.file_listbox.insert(tk.END, file)

        self.execute_button = Button(self.main_frame, text="Execute Selected File", command=lambda: self.execute_selected_file(extension), font=("Arial", 14))
        self.execute_button.pack(pady=10)

        self.back_button = Button(self.main_frame, text="Back to Main Menu", command=self.create_main_menu, font=("Arial", 14))
        self.back_button.pack(pady=10)

    def execute_selected_file(self, extension):
        try:
            selected_file = self.file_listbox.get(tk.ACTIVE)
            if selected_file:
                self.execute_file(selected_file)
                self.status_var.set(f"Execution of {selected_file} finished.")
            else:
                messagebox.showwarning("No File Selected", "Please select a file to execute.")
        except Exception as e:
            messagebox.showerror("Execution Error", f"Error: {str(e)}")
            self.status_var.set("Execution failed. Please check the error message.")

    def execute_file(self, file_path):
        if file_path.endswith('.py'):
            self.execute_python_file(file_path)
        elif file_path.endswith('.exe'):
            self.execute_executable_file(file_path)
        elif file_path.endswith('.bat'):
            self.execute_batch_file(file_path)
        else:
            messagebox.showerror("Unsupported File Type", f"Unsupported file type: {file_path}")

    def execute_python_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
                exec(code, globals())
        except SyntaxError as e:
            messagebox.showerror("Syntax Error", f"Syntax Error in the file: {str(e)}")
        except Exception as e:
            messagebox.showerror("Execution Error", f"Error executing Python file: {str(e)}")

    def execute_executable_file(self, file_path):
        try:
            if os.name == 'nt':  # Windows
                os.system(file_path)
            else:
                messagebox.showwarning("Unsupported Operation", "Execution of .exe files is not supported on Unix/macOS.")
        except Exception as e:
            messagebox.showerror("Execution Error", f"Error executing executable file: {str(e)}")

    def execute_batch_file(self, file_path):
        try:
            if os.name == 'nt':  # Windows
                subprocess.Popen(['cmd.exe', '/c', file_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                messagebox.showwarning("Unsupported Operation", "Execution of .bat files is not supported on Unix/macOS.")
        except Exception as e:
            messagebox.showerror("Execution Error", f"Error executing batch file: {str(e)}")

    def show_python_files(self):
        self.show_files('.py', 'Python')

    def show_executable_files(self):
        self.show_files('.exe', 'Executable')

    def show_batch_files(self):
        self.show_files('.bat', 'Batch')

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = FileExecutorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
