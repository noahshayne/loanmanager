import tkinter as tk
from tkinter import messagebox


class LoanManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loan Manager")
        self.root.geometry("1000x700")
        
        self.loan_types = []  # where we store the loan types
        self.loans = {}  # here we keep all loans grouped by loan type

        self.create_widgets()

    def create_widgets(self):
        # title label
        self.title_label = tk.Label(self.root, text="Loan Manager", font=("Arial", 16))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # loan type input & add button
        self.loan_type_label = tk.Label(self.root, text="Enter Loan Type:")
        self.loan_type_label.grid(row=1, column=0, padx=10, pady=5)
        
        self.loan_type_entry = tk.Entry(self.root)
        self.loan_type_entry.grid(row=1, column=1, padx=10, pady=5)

        self.add_loan_type_button = tk.Button(self.root, text="Add Loan Type", command=self.add_loan_type)
        self.add_loan_type_button.grid(row=1, column=2, padx=10, pady=5)

        # frame for dynamic loan types & loans
        self.loan_type_frame = tk.Frame(self.root)
        self.loan_type_frame.grid(row=2, column=0, columnspan=3, pady=20)

    def add_loan_type(self):
        loan_type = self.loan_type_entry.get().strip()
        
        if not loan_type:
            messagebox.showerror("Error", "Please enter a valid loan type!")
            return
        
        if loan_type in self.loan_types:
            messagebox.showerror("Error", "Loan type already added!")
            return
        
        # add the new loan type to the list and clear the entry field
        self.loan_types.append(loan_type)
        self.loan_type_entry.delete(0, tk.END)
        
        # create a new frame for this loan type
        loan_type_frame = tk.LabelFrame(self.loan_type_frame, text=loan_type, padx=50, pady=50)
        loan_type_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # store this loan type in the loans dictionary
        self.loans[loan_type] = []

        # add fields to enter loans under this loan type
        self.add_loan_fields(loan_type_frame, loan_type)

        # add delete button for this loan type
        delete_loan_type_button = tk.Button(loan_type_frame, text="Delete Loan Type", command=lambda: self.delete_loan_type(loan_type, loan_type_frame))
        delete_loan_type_button.grid(row=3, column=0, columnspan=2, pady=10)

    def add_loan_fields(self, parent_frame, loan_type):
        # creating fields for adding a loan (sub-loan) under the selected loan type
        loan_amount_label = tk.Label(parent_frame, text="Loan Amount:")
        loan_amount_label.grid(row=0, column=0, padx=5, pady=5)

        # crea
        loan_date_label = tk.Label(parent_frame, text="Loan Date (YYYY-MM-DD):")
        loan_date_label.grid(row=0, column=1, padx=5, pady=5)

        loan_amount_entry = tk.Entry(parent_frame)
        loan_amount_entry.grid(row=1, column=0, padx=5, pady=5)

        loan_date_entry = tk.Entry(parent_frame)
        loan_date_entry.grid(row=1, column=1, padx=5, pady=5)

        # add loan button for adding loans under this loan type
        add_loan_button = tk.Button(parent_frame, text="Add Loan", command=lambda: self.add_loan(loan_type, loan_amount_entry, loan_date_entry, parent_frame))
        add_loan_button.grid(row=2, column=0, columnspan=2, pady=10)

    def add_loan(self, loan_type, amount_entry, date_entry, parent_frame):
        amount = amount_entry.get().strip()
        date = date_entry.get().strip()
        
        if not amount or not date:
            messagebox.showerror("Error", "Please enter both amount and date!")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Loan amount must be a number!")
            return
        
        # add the loan to the list under the selected loan type
        self.loans[loan_type].append({"amount": amount, "date": date})
        
        # create a label showing the loan info
        loan_info = f"Amount: ${amount} | Date: {date}"
        loan_label = tk.Label(parent_frame, text=loan_info)
        loan_label.grid(row=len(self.loans[loan_type]) + 3, column=0, columnspan=2, pady=5)

        # add a delete button for this loan
        delete_loan_button = tk.Button(parent_frame, text="Delete Loan", command=lambda: self.delete_loan(loan_type, loan_label, delete_loan_button, amount, date, parent_frame))
        delete_loan_button.grid(row=len(self.loans[loan_type]) + 3, column=2, padx=5, pady=5)

        # clear the fields after adding the loan
        amount_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", f"Loan for {loan_type} added successfully!")

    def delete_loan(self, loan_type, loan_label, delete_loan_button, amount, date, parent_frame):
        """delete a specific loan (sub-loan) and its associated button"""
        # remove the loan from the loan list
        self.loans[loan_type] = [loan for loan in self.loans[loan_type] if not (loan["amount"] == amount and loan["date"] == date)]

        # remove the loan label and delete button from the UI
        loan_label.destroy()
        delete_loan_button.destroy()

        # show success message
        messagebox.showinfo("Success", f"Loan of amount ${amount} on {date} deleted successfully!")

    def delete_loan_type(self, loan_type, loan_type_frame):
        """delete a loan type and all loans under it"""
        # remove the loan type and its associated loans
        del self.loans[loan_type]
        self.loan_types.remove(loan_type)

        # remove the loan type frame from the UI
        loan_type_frame.destroy()

        # show success message
        messagebox.showinfo("Success", f"Loan type '{loan_type}' and all its loans deleted successfully!")


# create the main window
root = tk.Tk()

#Create the LoanManagerApp instance
app = LoanManagerApp(root)

# run the application
root.mainloop()
