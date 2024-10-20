import tkinter as tk
from tkinter import messagebox

def add_bill():
    try:
        bill_amount = float(bill_entry.get())
        bills_listbox.insert(tk.END, f"£{bill_amount:.2f}")
        update_total_bills()
        bill_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid bill amount.")

def update_total_bills():
    total = 0
    for i in range(bills_listbox.size()):
        bill = bills_listbox.get(i)
        total += float(bill.replace('£', ''))
    total_bills_label.config(text=f"Total Bills: £{total:.2f}")

def calculate_remaining():
    try:
        wage = float(wage_entry.get())
        misc = float(misc_entry.get()) if misc_entry.get() else 0
        
        total_bills = 0
        for i in range(bills_listbox.size()):
            bill = bills_listbox.get(i)
            total_bills += float(bill.replace('£', ''))
        
        food = float(food_entry.get())
        total_expenses = total_bills + food + misc
        remaining = wage - total_expenses

        if remaining < 0:
            result_label.config(text="You are overspending!")
        else:
            result_label.config(text=f"Remaining: £{remaining:.2f}")
            remaining_amount.set(remaining)
    
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for wage, expenses, and bills.")

def allocate_funds():
    try:
        allocation = float(allocation_entry.get())
        remaining = remaining_amount.get()
        
        if allocation > remaining:
            messagebox.showerror("Input Error", "Allocation exceeds remaining funds!")
        else:
            remaining -= allocation
            remaining_amount.set(remaining)
            allocated_listbox.insert(tk.END, f"{category_entry.get()}: £{allocation:.2f}")
            remaining_label.config(text=f"Remaining: £{remaining:.2f}")
            allocation_entry.delete(0, tk.END)
            category_entry.delete(0, tk.END)
    
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid allocation amount.")

root = tk.Tk()
root.title("Custom Finance Manager")

remaining_amount = tk.DoubleVar()

tk.Label(root, text="Monthly Wage:").grid(row=0, column=0, padx=10, pady=5)
wage_entry = tk.Entry(root)
wage_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Add Bill:").grid(row=1, column=0, padx=10, pady=5)
bill_entry = tk.Entry(root)
bill_entry.grid(row=1, column=1, padx=10, pady=5)

add_bill_button = tk.Button(root, text="Add Bill", command=add_bill)
add_bill_button.grid(row=1, column=2, padx=10, pady=5)

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

calculate_button = tk.Button(root, text="Calculate Remaining", command=calculate_remaining)
calculate_button.grid(row=6, columnspan=3, pady=10)

result_label = tk.Label(root, text="")
result_label.grid(row=7, columnspan=3, pady=5)

tk.Label(root, text="Allocate Remaining Funds").grid(row=8, columnspan=3, pady=10)

tk.Label(root, text="Category:").grid(row=9, column=0, padx=10, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=9, column=1, padx=10, pady=5)

tk.Label(root, text="Amount:").grid(row=10, column=0, padx=10, pady=5)
allocation_entry = tk.Entry(root)
allocation_entry.grid(row=10, column=1, padx=10, pady=5)

allocate_button = tk.Button(root, text="Allocate", command=allocate_funds)
allocate_button.grid(row=11, columnspan=3, pady=10)

allocated_listbox = tk.Listbox(root, height=5)
allocated_listbox.grid(row=12, column=1, padx=10, pady=5)

remaining_label = tk.Label(root, text="Remaining: £0.00")
remaining_label.grid(row=13, column=1, padx=10, pady=5)

root.mainloop()
