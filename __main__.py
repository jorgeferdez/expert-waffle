import tkinter as tk
from tkinter import messagebox
import bin_packing as bp


class MultiplierValueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Bin Packing Example")

        self.rows = []

        tk.Label(root, text="Bin Capacity").pack()

        self.entry = tk.Entry(root, width=10)
        self.entry.pack(padx=10, pady=10)

        self.table_frame = tk.Frame(root)
        self.table_frame.pack(padx=10, pady=10)

        tk.Label(self.table_frame, text="Amount of Items").grid(row=0, column=0, padx=5)
        tk.Label(self.table_frame, text="Weight").grid(row=0, column=1, padx=5)

        self.add_row_button = tk.Button(root, text="Add Row", command=self.add_row)
        self.add_row_button.pack(pady=5)

        self.clear_button = tk.Button(root, text="Remove Row", command=self.remove_row)
        self.clear_button.pack(pady=5)

        self.process_button = tk.Button(root, text="Process", command=self.process_rows)
        self.process_button.pack(pady=5)

        self.result_label = tk.Label(root, text="Result: ")
        self.result_label.pack(pady=10)

        self.add_row()

    def remove_row(self):
        if self.rows:
            mult_entry, val_entry = self.rows.pop()
            mult_entry.destroy()
            val_entry.destroy()
        else:
            messagebox.showinfo("Info", "No more rows to remove")

    def add_row(self):
        row_index = len(self.rows) + 1
        mult_entry = tk.Entry(self.table_frame, width=10)
        val_entry = tk.Entry(self.table_frame, width=10)

        mult_entry.grid(row=row_index, column=0, padx=5, pady=2)
        val_entry.grid(row=row_index, column=1, padx=5, pady=2)

        self.rows.append((mult_entry, val_entry))

    def process_rows(self):
        weights = []
        try:
            for mult_entry, val_entry in self.rows:
                mult = int(mult_entry.get())
                val = int(val_entry.get())
                weights.extend([val] * mult)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers in all fields.")
            return

        num_bins, packed, error_message = bp.solve(weights, int(self.entry.get()))

        if error_message:
            messagebox.showerror(error_message)

        self.result_label.config(text=f"Result: {packed}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MultiplierValueApp(root)
    root.mainloop()
