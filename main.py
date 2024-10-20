import tkinter as tk
from tkinter import messagebox

# Helper function to validate and return a float value from an entry widget
def get_float_value(entry, default=0):
    try:
        return float(entry.get())
    except ValueError:
        return default

# Function to update total bills from the listbox
def update_total_bills():
    total = sum(float(bill.replace('£', '')) for bill in bills_listbox.get(0, tk.END))  # Sum all values in the listbox
    total_bills_label.config(text=f"Total Bills: £{total:.2f}")
    return total

# Function to add a bill to the list and update the total
def add_bill():
    bill_amount = get_float_value(bill_entry)  # Get and validate the bill amount
    if bill_amount:  # If the amount is valid and non-zero
        bills_listbox.insert(tk.END, f"£{bill_amount:.2f}")  # Add the bill to the listbox
        update_total_bills()  # Recalculate the total bills
        bill_entry.delete(0, tk.END)  # Clear the entry
    else:
        messagebox.showerror("Input Error", "Please enter a valid bill amount.")  # Error if input is invalid

# Function to calculate the remaining funds after expenses
def calculate_remaining():
    wage = get_float_value(wage_entry)
    misc = get_float_value(misc_entry)
    food = get_float_value(food_entry)
    
    total_bills = update_total_bills()  # Get updated total bills
    total_expenses = total_bills + food + misc  # Calculate total expenses
    remaining = wage - total_expenses  # Calculate remaining balance

    if remaining < 0:
        result_label.config(text="You are overspending!")  # Show overspending message if expenses exceed income
    else:
        result_label.config(text=f"Remaining: £{remaining:.2f}")  # Show remaining balance
        remaining_amount.set(remaining)  # Update remaining amount for allocations

# Function to allocate funds to different categories
def allocate_funds():
    allocation = get_float_value(allocation_entry)
    remaining = remaining_amount.get()

    if allocation > remaining:  # Check if allocation exceeds remaining funds
        messagebox.showerror("Input Error", "Allocation exceeds remaining funds!")
    else:
        remaining -= allocation  # Deduct allocation from remaining balance
        remaining_amount.set(remaining)  # Update the remaining amount
        allocated_listbox.insert(tk.END, f"{category_entry.get()}: £{allocation:.2f}")  # Add allocation to listbox
        remaining_label.config(text=f"Remaining: £{remaining:.2f}")  # Update remaining label
        allocation_entry.delete(0, tk.END)  # Clear allocation entry
        category_entry.delete(0, tk.END)  # Clear category entry

# Main window setup
root = tk.Tk()
root.title("Custom Finance Manager")

remaining_amount = tk.DoubleVar()  # Variable to track remaining funds

# Create and position widgets
tk.Label(root, text="Monthly Wage:").grid(row=0, column=0, padx=10, pady=5)
wage_entry = tk.Entry(root)
wage_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Add Bill:").grid(row=1, column=0, padx=10, pady=5)
bill_entry = tk.Entry(root)
bill_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Add Bill", command=add_bill).grid(row=1, column=2, padx=10, pady=5)

bills_listbox = tk.Listbox(root, height=5)
bills_listbox.grid(row=2, column=1, padx=10, pady=5)

total_bills_label = tk.Label(root, text="Total Bills: £0.00")
total_bills_label.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Miscellaneous (One-Offs):").grid(row=4, column=0, padx=10, pady=5)
misc_entry = tk.Entry(root)
misc_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Food Expenses:").grid(row=5, column=0, padx=10, pady=5)
food_entry = tk.Entry(root)
food_entry.grid(row=5, column=1, padx=10, pady=5)

tk.Button(root, text="Calculate Remaining", command=calculate_remaining).grid(row=6, columnspan=3, pady=10)

result_label = tk.Label(root, text="")
result_label.grid(row=7, columnspan=3, pady=5)

tk.Label(root, text="Allocate Remaining Funds").grid(row=8, columnspan=3, pady=10)

tk.Label(root, text="Category:").grid(row=9, column=0, padx=10, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=9, column=1, padx=10, pady=5)

tk.Label(root, text="Amount:").grid(row=10, column=0, padx=10, pady=5)
allocation_entry = tk.Entry(root)
allocation_entry.grid(row=10, column=1, padx=10, pady=5)

tk.Button(root, text="Allocate", command=allocate_funds).grid(row=11, columnspan=3, pady=10)

allocated_listbox = tk.Listbox(root, height=5)
allocated_listbox.grid(row=12, column=1, padx=10, pady=5)

remaining_label = tk.Label(root, text="Remaining: £0.00")
remaining_label.grid(row=13, column=1, padx=10, pady=5)

# Start the application
root.mainloop()
