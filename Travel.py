#Team Bren (Miranda, Benedict and Lansangan, Renalene Mae) BSCpE 1A
#Travel Itinerary and Expense Tracker
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import sqlite3

# Initialize database
def init_db():
    conn = sqlite3.connect("travel_planner.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS itineraries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        title TEXT,
                        date TEXT,
                        description TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        item TEXT,
                        cost REAL,
                        date TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

class TravelPlannerApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Travel Itinerary Planner and Expense Tracker")
        self.geometry("850x610")
        self.resizable(False, False)

        self.current_user = None

        self.configure(bg="#F0F0F5")  # Light grey background for iOS feel

        self.create_login_screen()

    def create_login_screen(self):
        self.clear_frame()

        self.login_frame = ctk.CTkFrame(self, width=400, height=300, corner_radius=15)
        self.login_frame.pack(expand=True, pady=50)

        self.label_username = ctk.CTkLabel(self.login_frame, text="Username:", font=("Helvetica Neue", 14), text_color="#333333")
        self.label_username.pack(pady=(20, 5))

        self.entry_username = ctk.CTkEntry(self.login_frame, corner_radius=10, fg_color="#F0F0F5", border_color="#D1D1D6")
        self.entry_username.pack(pady=5)

        self.label_password = ctk.CTkLabel(self.login_frame, text="Password:", font=("Helvetica Neue", 14), text_color="#333333")
        self.label_password.pack(pady=5)

        self.entry_password = ctk.CTkEntry(self.login_frame, show="*", corner_radius=10, fg_color="#F0F0F5", border_color="#D1D1D6")
        self.entry_password.pack(pady=5)

        self.button_login = ctk.CTkButton(self.login_frame, text="Login", command=self.login, corner_radius=10, fg_color="#007AFF", text_color="#FFFFFF")
        self.button_login.pack(pady=20)

        self.button_register = ctk.CTkButton(self.login_frame, text="Register", command=self.register, corner_radius=10, fg_color="#34C759", text_color="#FFFFFF")
        self.button_register.pack(pady=5)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        conn = sqlite3.connect("travel_planner.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.current_user = user[0]
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        conn = sqlite3.connect("travel_planner.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        conn.close()

    def create_main_screen(self):
        self.clear_frame()

        self.main_frame = ctk.CTkFrame(self, width=800, height=600, corner_radius=15, bg_color="#D1D1D6")
        self.main_frame.pack(expand=True, fill='both')

        self.button_logout = ctk.CTkButton(self.main_frame, text="Logout", command=self.logout, corner_radius=10, fg_color="#FF3B30", text_color="#FFFFFF")
        self.button_logout.pack(pady=10, anchor='e', padx=20)

        self.tabview = ctk.CTkTabview(self.main_frame, width=780, height=500, corner_radius=10, fg_color="#FFFFFF")
        self.tabview.pack(pady=10)

        self.tab_itinerary = self.tabview.add("Itinerary")
        self.tab_expenses = self.tabview.add("Expenses")

        self.create_itinerary_tab()
        self.create_expenses_tab()

    def create_itinerary_tab(self):
        self.left_frame = ctk.CTkFrame(self.tab_itinerary, width=390, height=400, corner_radius=10, bg_color="#FFFFFF")
        self.left_frame.pack(side='left', padx=10, pady=10)

        self.right_frame = ctk.CTkFrame(self.tab_itinerary, width=390, height=400, corner_radius=10, bg_color="#FFFFFF")
        self.right_frame.pack(side='right', padx=10, pady=10)

        self.label_itinerary_title = ctk.CTkLabel(self.left_frame, text="Destination:", font=("Helvetica Neue", 14), text_color="#333333")
        self.label_itinerary_title.pack(pady=(10, 5))

        self.entry_itinerary_title = ctk.CTkEntry(self.left_frame, corner_radius=10, fg_color="#F0F0F5", border_color="#D1D1D6")
        self.entry_itinerary_title.pack(pady=5)

        self.label_itinerary_date = ctk.CTkLabel(self.left_frame, text="Date:", font=("Helvetica Neue", 14), text_color="#333333")
        self.label_itinerary_date.pack(pady=5)

        self.entry_itinerary_date = ctk.CTkEntry(self.left_frame, corner_radius=10, fg_color="#F0F0F5", border_color="#D1D1D6")
        self.entry_itinerary_date.pack(pady=5)

        self.label_itinerary_desc = ctk.CTkLabel(self.left_frame, text="Activity:", font=("Helvetica Neue", 14), text_color="#333333")
        self.label_itinerary_desc.pack(pady=5)

        self.entry_itinerary_desc = ctk.CTkEntry(self.left_frame, corner_radius=10, fg_color="#F0F0F5", border_color="#D1D1D6")
        self.entry_itinerary_desc.pack(pady=5)

        self.button_add_itinerary = ctk.CTkButton(self.left_frame, text="Add Itinerary", command=self.add_itinerary, corner_radius=10, fg_color="#007AFF", text_color="#FFFFFF")
        self.button_add_itinerary.pack(pady=10)

        self.listbox_itineraries = tk.Listbox(self.right_frame, width=50, height=20)
        self.listbox_itineraries.pack(pady=10)

        self.button_edit_itinerary = ctk.CTkButton(self.right_frame, text="Edit Itinerary", command=self.edit_itinerary, corner_radius=10, fg_color="#FF9500", text_color="#FFFFFF")
        self.button_edit_itinerary.pack(pady=5)

        self.button_delete_itinerary = ctk.CTkButton(self.right_frame, text="Delete Itinerary", command=self.delete_itinerary, corner_radius=10, fg_color="#FF3B30", text_color="#FFFFFF")
        self.button_delete_itinerary.pack(pady=5)

        self.load_itineraries()

    def create_expenses_tab(self):
        self.left_frame_expense = ctk.CTkFrame(self.tab_expenses, width=390, height=400, corner_radius=10, bg_color="#FFFFFF")
        self.left_frame_expense.pack(side='left', padx=10, pady=10)

        self.right_frame_expense = ctk.CTkFrame(self.tab_expenses, width=390, height=400, corner_radius=10, bg_color="#FFFFFF")
        self.right_frame_expense.pack(side='right', padx=10, pady=10)

        self.label_expense_item = ctk.CTkLabel(self.left_frame_expense, text="Item:", font=("Helvetica Neue", 14), text_color="#333333")
        self.label_expense_item.pack(pady=(10, 5))

        self.entry_expense_item = ctk.CTkEntry(self.left_frame_expense, corner_radius=10, fg_color="#F0F0F5", border_color="#D1D1D6")
        self.entry_expense_item.pack(pady=5)

        self.label_expense_cost = ctk.CTkLabel(self.left_frame_expense, text="Cost:", font=("Helvetica Neue", 14), text_color="#333333")
        self.label_expense_cost.pack(pady=5)

        self.entry_expense_cost = ctk.CTkEntry(self.left_frame_expense, corner_radius=10, fg_color="#F0F0F5", border_color="#D1D1D6")
        self.entry_expense_cost.pack(pady=5)

        self.label_expense_date = ctk.CTkLabel(self.left_frame_expense, text="Date:", font=("Helvetica Neue", 14), text_color="#333333")
        self.label_expense_date.pack(pady=5)

        self.entry_expense_date = ctk.CTkEntry(self.left_frame_expense, corner_radius=10, fg_color="#F0F0F5", border_color="#D1D1D6")
        self.entry_expense_date.pack(pady=5)

        self.button_add_expense = ctk.CTkButton(self.left_frame_expense, text="Add Expense", command=self.add_expense, corner_radius=10, fg_color="#007AFF", text_color="#FFFFFF")
        self.button_add_expense.pack(pady=10)

        self.listbox_expenses = tk.Listbox(self.right_frame_expense, width=50, height=20)
        self.listbox_expenses.pack(pady=10)

        self.button_edit_expense = ctk.CTkButton(self.right_frame_expense, text="Edit Expense", command=self.edit_expense, corner_radius=10, fg_color="#FF9500", text_color="#FFFFFF")
        self.button_edit_expense.pack(pady=5)

        self.button_delete_expense = ctk.CTkButton(self.right_frame_expense, text="Delete Expense", command=self.delete_expense, corner_radius=10, fg_color="#FF3B30", text_color="#FFFFFF")
        self.button_delete_expense.pack(pady=5)

        self.load_expenses()

    def load_itineraries(self):
        self.listbox_itineraries.delete(0, tk.END)
        conn = sqlite3.connect("travel_planner.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, date, description FROM itineraries WHERE user_id=?", (self.current_user,))
        self.itineraries = cursor.fetchall()
        conn.close()

        for itinerary in self.itineraries:
            self.listbox_itineraries.insert(tk.END, f"{itinerary[1]} - {itinerary[2]} - {itinerary[3]}")

    def load_expenses(self):
        self.listbox_expenses.delete(0, tk.END)
        conn = sqlite3.connect("travel_planner.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, item, cost, date FROM expenses WHERE user_id=?", (self.current_user,))
        self.expenses = cursor.fetchall()
        conn.close()

        for expense in self.expenses:
            self.listbox_expenses.insert(tk.END, f"{expense[1]} - {expense[2]} - {expense[3]}")

    def add_itinerary(self):
        title = self.entry_itinerary_title.get()
        date = self.entry_itinerary_date.get()
        description = self.entry_itinerary_desc.get()

        if title and date and description:
            conn = sqlite3.connect("travel_planner.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO itineraries (user_id, title, date, description) VALUES (?, ?, ?, ?)",
                           (self.current_user, title, date, description))
            conn.commit()
            conn.close()
            self.load_itineraries()
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def edit_itinerary(self):
        selected_index = self.listbox_itineraries.curselection()
        if selected_index:
            itinerary_id = self.itineraries[selected_index[0]][0]
            title = self.entry_itinerary_title.get()
            date = self.entry_itinerary_date.get()
            description = self.entry_itinerary_desc.get()

            if title and date and description:
                conn = sqlite3.connect("travel_planner.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE itineraries SET title=?, date=?, description=? WHERE id=?",
                               (title, date, description, itinerary_id))
                conn.commit()
                conn.close()
                self.load_itineraries()
            else:
                messagebox.showerror("Error", "Please fill in all fields")
        else:
            messagebox.showerror("Error", "Please select an itinerary to edit")

    def delete_itinerary(self):
        selected_index = self.listbox_itineraries.curselection()
        if selected_index:
            itinerary_id = self.itineraries[selected_index[0]][0]

            conn = sqlite3.connect("travel_planner.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM itineraries WHERE id=?", (itinerary_id,))
            conn.commit()
            conn.close()
            self.load_itineraries()
        else:
            messagebox.showerror("Error", "Please select an itinerary to delete")

    def add_expense(self):
        item = self.entry_expense_item.get()
        cost = self.entry_expense_cost.get()
        date = self.entry_expense_date.get()

        if item and cost and date:
            conn = sqlite3.connect("travel_planner.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO expenses (user_id, item, cost, date) VALUES (?, ?, ?, ?)",
                           (self.current_user, item, float(cost), date))
            conn.commit()
            conn.close()
            self.load_expenses()
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def edit_expense(self):
        selected_index = self.listbox_expenses.curselection()
        if selected_index:
            expense_id = self.expenses[selected_index[0]][0]
            item = self.entry_expense_item.get()
            cost = self.entry_expense_cost.get()
            date = self.entry_expense_date.get()

            if item and cost and date:
                conn = sqlite3.connect("travel_planner.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE expenses SET item=?, cost=?, date=? WHERE id=?",
                               (item, float(cost), date, expense_id))
                conn.commit()
                conn.close()
                self.load_expenses()
            else:
                messagebox.showerror("Error", "Please fill in all fields")
        else:
            messagebox.showerror("Error", "Please select an expense to edit")

    def delete_expense(self):
        selected_index = self.listbox_expenses.curselection()
        if selected_index:
            expense_id = self.expenses[selected_index[0]][0]

            conn = sqlite3.connect("travel_planner.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
            conn.commit()
            conn.close()
            self.load_expenses()
        else:
            messagebox.showerror("Error", "Please select an expense to delete")

    def logout(self):
        self.current_user = None
        self.create_login_screen()

if __name__ == "__main__":
    init_db()
    app = TravelPlannerApp()
    app.mainloop()