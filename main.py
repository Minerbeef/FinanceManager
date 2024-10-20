import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import json

class FinanceManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Finance Manager")
        
        self.remaining_amount = tk.DoubleVar()  # Variable to track remaining funds

        # Create frames for better organization
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.summary_frame = tk.Frame(self.root)
        self.summary_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.create_widgets()

    def create_widgets(self):
        # Input section
        tk.Label(self.input_frame, text="Monthly Wage:").grid(row=0, column=0, padx=10, pady=5)
        self.wage_entry = tk.Entry(self.input_frame)
        self.wage_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.input_frame, text="Add Bill:").grid(row=1, column=0, padx=10, pady=5)
        self.bill_entry = tk.Entry(self.input_frame)
        self.bill_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.input_frame, text="Add Bill", command=self.add_bill).grid(row=1, column=2, padx=10, pady=5)
        
        # Button to remove selected bill
        tk.Button(self.input_frame, text="Remove Bill", command=self.remove_bill).grid(row=1, column=3, padx=10, pady=5)

        self.bills_listbox = tk.Listbox(self.input_frame, height=5)
        self.bills_listbox.grid(row=2, column=1, padx=10, pady=5)

        self.total_bills_label = tk.Label(self.input_frame, text="Total Bills: £0.00")
        self.total_bills_label.grid(row=3, column=1, padx=10, pady=5)

        # Expenses section
        tk.Label(self.input_frame, text="Miscellaneous (One-Offs):").grid(row=4, column=0, padx=10, pady=5)
        self.misc_entry = tk.Entry(self.input_frame)
        self.misc_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.input_frame, text="Food Expenses:").grid(row=5, column=0, padx=10, pady=5)
        self.food_entry = tk.Entry(self.input_frame)
        self.food_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Button(self.input_frame, text="Calculate Remaining", command=self.calculate_remaining).grid(row=6, columnspan=3, pady=10)

        self.result_label = tk.Label(self.input_frame, text="")
        self.result_label.grid(row=7, columnspan=3, pady=5)

        # Allocation section
        tk.Label(self.input_frame, text="Allocate Remaining Funds").grid(row=8, columnspan=3, pady=10)

        tk.Label(self.input_frame, text="Category:").grid(row=9, column=0, padx=10, pady=5)
        self.category_entry = tk.Entry(self.input_frame)
        self.category_entry.grid(row=9, column=1, padx=10, pady=5)

        tk.Label(self.input_frame, text="Amount:").grid(row=10, column=0, padx=10, pady=5)
        self.allocation_entry = tk.Entry(self.input_frame)
        self.allocation_entry.grid(row=10, column=1, padx=10, pady=5)

        tk.Button(self.input_frame, text="Allocate", command=self.allocate_funds).grid(row=11, columnspan=3, pady=10)

        self.allocated_listbox = tk.Listbox(self.input_frame, height=5)
        self.allocated_listbox.grid(row=12, column=1, padx=10, pady=5)

        self.remaining_label = tk.Label(self.input_frame, text="Remaining: £0.00")
        self.remaining_label.grid(row=13, columnspan=3, pady=5)

        # Summary section
        tk.Label(self.summary_frame, text="Summary Dashboard").grid(row=0, columnspan=2)

        self.total_expenses_label = tk.Label(self.summary_frame, text="Total Expenses: £0.00")
        self.total_expenses_label.grid(row=1, columnspan=2, pady=5)

        self.savings_label = tk.Label(self.summary_frame, text="Savings: £0.00")
        self.savings_label.grid(row=2, columnspan=2, pady=5)

        tk.Label(self.summary_frame, text="Progress:").grid(row=3, columnspan=2)

        self.total_expenses_bar = ttk.Progressbar(self.summary_frame, length=200, maximum=100)
        self.total_expenses_bar.grid(row=4, columnspan=2, pady=5)

        self.savings_bar = ttk.Progressbar(self.summary_frame, length=200, maximum=100)
        self.savings_bar.grid(row=5, columnspan=2, pady=5)

        self.bills_percentage_label = tk.Label(self.summary_frame, text="Bills: 0.00%")
        self.bills_percentage_label.grid(row=6, column=0, pady=5)

        self.food_percentage_label = tk.Label(self.summary_frame, text="Food: 0.00%")
        self.food_percentage_label.grid(row=6, column=1, pady=5)

        self.misc_percentage_label = tk.Label(self.summary_frame, text="Miscellaneous: 0.00%")
        self.misc_percentage_label.grid(row=7, columnspan=2, pady=5)

        # Menu bar for saving and loading data
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Data", command=self.save_data)
        file_menu.add_command(label="Load Data", command=self.load_data)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    # Helper function to validate and return a float value from an entry widget
    def get_float_value(self, entry, default=0):
        try:
            return float(entry.get())
        except ValueError:
            return default

    # Function to update total bills from the listbox
    def update_total_bills(self):
        total = sum(float(bill.replace('£', '')) for bill in self.bills_listbox.get(0, tk.END))  # Sum all values in the listbox
        self.total_bills_label.config(text=f"Total Bills: £{total:.2f}")
        return total

    # Function to add a bill to the list and update the total
    def add_bill(self):
        bill_amount = self.get_float_value(self.bill_entry)  # Get and validate the bill amount
        if bill_amount > 0:  # If the amount is valid and non-zero
            self.bills_listbox.insert(tk.END, f"£{bill_amount:.2f}")  # Add the bill to the listbox
            self.update_total_bills()  # Recalculate the total bills
            self.bill_entry.delete(0, tk.END)  # Clear the entry
        else:
            messagebox.showerror("Input Error", "Please enter a valid bill amount.")  # Error if input is invalid

    # Function to remove the selected bill from the listbox
    def remove_bill(self):
        try:
            selected_index = self.bills_listbox.curselection()[0]  # Get the selected bill index
            self.bills_listbox.delete(selected_index)  # Remove the selected bill
            self.update_total_bills()  # Recalculate the total bills
        except IndexError:
            messagebox.showerror("Selection Error", "Please select a bill to remove.")  # Error if no selection is made

    # Function to calculate the remaining funds after expenses
    def calculate_remaining(self):
        wage = self.get_float_value(self.wage_entry)
        misc = self.get_float_value(self.misc_entry)
        food = self.get_float_value(self.food_entry)

        total_bills = self.update_total_bills()  # Get updated total bills
        total_expenses = total_bills + food + misc  # Calculate total expenses
        remaining = wage - total_expenses  # Calculate remaining balance

        if remaining < 0:
            self.result_label.config(text="You are overspending!")  # Show overspending message if expenses exceed income
        else:
            self.result_label.config(text=f"Remaining: £{remaining:.2f}")  # Show remaining balance
            self.remaining_amount.set(remaining)  # Update remaining amount for allocations
            self.update_summary(remaining, wage, total_bills, food, misc)  # Update summary dashboard

    # Function to allocate funds to different categories
    def allocate_funds(self):
        allocation = self.get_float_value(self.allocation_entry)
        remaining = self.remaining_amount.get()

        if allocation <= 0:  # Check for non-positive allocation
            messagebox.showerror("Input Error", "Allocation must be a positive value!")
            return

        if allocation > remaining:  # Check if allocation exceeds remaining funds
            messagebox.showerror("Input Error", "Allocation exceeds remaining funds!")
        else:
            remaining -= allocation  # Deduct allocation from remaining balance
            self.remaining_amount.set(remaining)  # Update the remaining amount
            self.allocated_listbox.insert(tk.END, f"{self.category_entry.get()}: £{allocation:.2f}")  # Add allocation to listbox
            self.remaining_label.config(text=f"Remaining: £{remaining:.2f}")  # Update remaining label
            self.allocation_entry.delete(0, tk.END)  # Clear allocation entry
            self.category_entry.delete(0, tk.END)  # Clear category entry

    # Function to update summary dashboard
    def update_summary(self, remaining, wage, total_bills, food, misc):
        total_expenses = total_bills + food + misc
        savings = remaining
        total = wage

        self.total_expenses_label.config(text=f"Total Expenses: £{total_expenses:.2f}")
        self.savings_label.config(text=f"Savings: £{savings:.2f}")

        # Update progress bars
        self.total_expenses_bar['value'] = (total_expenses / total * 100) if total > 0 else 0
        self.savings_bar['value'] = (savings / total * 100) if total > 0 else 0

        # Update expense breakdown
        if total > 0:
            bills_percentage = (total_bills / total) * 100
            food_percentage = (food / total) * 100
            misc_percentage = (misc / total) * 100

            self.bills_percentage_label.config(text=f"Bills: {bills_percentage:.2f}%")
            self.food_percentage_label.config(text=f"Food: {food_percentage:.2f}%")
            self.misc_percentage_label.config(text=f"Miscellaneous: {misc_percentage:.2f}%")

    # Function to save input data to a file
    def save_data(self):
        data = {
            "wage": self.wage_entry.get(),
            "bills": [self.bills_listbox.get(i) for i in range(self.bills_listbox.size())],
            "misc": self.misc_entry.get(),
            "food": self.food_entry.get(),
            "allocations": [self.allocated_listbox.get(i) for i in range(self.allocated_listbox.size())]
        }
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(data, file)

    # Function to load input data from a file
    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.wage_entry.delete(0, tk.END)
                self.wage_entry.insert(0, data.get("wage", ""))
                self.misc_entry.delete(0, tk.END)
                self.misc_entry.insert(0, data.get("misc", ""))
                self.food_entry.delete(0, tk.END)
                self.food_entry.insert(0, data.get("food", ""))
                self.bills_listbox.delete(0, tk.END)
                for bill in data.get("bills", []):
                    self.bills_listbox.insert(tk.END, bill)
                self.allocated_listbox.delete(0, tk.END)
                for allocation in data.get("allocations", []):
                    self.allocated_listbox.insert(tk.END, allocation)
                self.update_total_bills()
                self.calculate_remaining()  # Recalculate remaining after loading data

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceManager(root)
    root.mainloop()
