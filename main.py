import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date, timedelta
import smtplib
from email.mime.text import MIMEText

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# PLEASE CHANGE THESE TO YOUR GMAIL AND APP PASSWORD
YOUR_EMAIL = "your_email@gmail.com"
YOUR_APP_PASSWORD = "your_app_password"

def send_email(to_email, subject, body):
    if not to_email or to_email.strip() == "":
        return
    if YOUR_EMAIL == "your_email@gmail.com":
        print(f"MOCK EMAIL (Config required)\nTo: {to_email}\nSub: {subject}\nBody:\n{body}\n")
        return
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = YOUR_EMAIL
        msg['To'] = to_email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(YOUR_EMAIL, YOUR_APP_PASSWORD)
            server.sendmail(YOUR_EMAIL, to_email, msg.as_string())
    except Exception as e:
        print("Email Failed:", e)

def get_db_connection():
    return mysql.connector.connect(host="localhost", user="root", password="", database="library_system")

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System - Login")
        self.geometry("500x400")
        self.resizable(False, False)
        
        self.label_title = ctk.CTkLabel(self, text="Library System Login", font=ctk.CTkFont(size=24, weight="bold"))
        self.label_title.pack(pady=(50, 30))
        
        self.entry_user = ctk.CTkEntry(self, placeholder_text="Username", width=250, height=40)
        self.entry_user.pack(pady=10)
        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=250, height=40)
        self.entry_pass.pack(pady=10)
        
        self.btn_login = ctk.CTkButton(self, text="Login", width=250, height=40, command=self.login, font=ctk.CTkFont(weight="bold"))
        self.btn_login.pack(pady=20)
        
    def login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        if not username or not password:
            messagebox.showwarning("Warning", "කරුණාකර Username සහ Password ඇතුලත් කරන්න!")
            return
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
            result = cursor.fetchone()
            conn.close()
            if result:
                self.destroy()
                app = DashboardWindow()
                app.mainloop()
            else:
                messagebox.showerror("Error", "Username හෝ Password වැරදියි!")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {e}")

class DashboardWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System - Pro")
        self.geometry("1200x750")
        
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=30, fieldbackground="#343638", bordercolor="#343638", borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=('Arial', 10, 'bold'))
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="E-Library\nSystem", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.pack(pady=(30, 40))
        
        self.btn_dashboard = ctk.CTkButton(self.sidebar, text="Dashboard", height=40, command=self.show_dashboard)
        self.btn_dashboard.pack(pady=10, padx=20, fill="x")
        self.btn_books = ctk.CTkButton(self.sidebar, text="Manage Books", height=40, command=self.show_books)
        self.btn_books.pack(pady=10, padx=20, fill="x")
        self.btn_members = ctk.CTkButton(self.sidebar, text="Manage Members", height=40, command=self.show_members)
        self.btn_members.pack(pady=10, padx=20, fill="x")
        self.btn_issue = ctk.CTkButton(self.sidebar, text="Issue/Return Book", height=40, command=self.show_issue)
        self.btn_issue.pack(pady=10, padx=20, fill="x")
        
        self.appearance_mode_om = ctk.CTkOptionMenu(self.sidebar, values=["Dark", "Light"], command=self.change_appearance_mode_event)
        self.appearance_mode_om.pack(pady=20, padx=20, fill="x", side="bottom")
        self.btn_logout = ctk.CTkButton(self.sidebar, text="Logout", height=40, fg_color="#C0392B", hover_color="#922B21", command=self.logout)
        self.btn_logout.pack(pady=(150, 0), padx=20, fill="x", side="bottom")

        self.main_container = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.main_container.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        self.current_frame = None
        self.show_dashboard()

    def clear_container(self):
        if self.current_frame:
            self.current_frame.destroy()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        style = ttk.Style(self)
        if new_appearance_mode == "Light":
            style.configure("Treeview", background="#ffffff", foreground="black", fieldbackground="#ffffff")
            style.configure("Treeview.Heading", background="#e0e0e0", foreground="black")
        else:
            style.configure("Treeview", background="#2a2d2e", foreground="white", fieldbackground="#343638")
            style.configure("Treeview.Heading", background="#565b5e", foreground="white")

    # ================= DASHBOARD ================= #
    def show_dashboard(self):
        self.clear_container()
        self.current_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(self.current_frame, text="Dashboard Overview", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=20)
        
        cards_frame = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        cards_frame.pack(pady=20, fill="x")
        
        self.c1_label = self.create_card(cards_frame, "Total Books", "0")
        self.c2_label = self.create_card(cards_frame, "Total Members", "0")
        self.c3_label = self.create_card(cards_frame, "Issued Books", "0")
        
        # Tools
        ctk.CTkButton(self.current_frame, text="Run Automated Reminders (Emails)", command=self.run_reminders).pack(pady=40)
        
        self.update_dashboard_stats()

    def create_card(self, parent, title, val):
        card = ctk.CTkFrame(parent, width=220, height=140, corner_radius=15)
        card.pack(side="left", padx=20)
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=18)).pack(pady=(20, 10))
        lbl = ctk.CTkLabel(card, text=val, font=ctk.CTkFont(size=36, weight="bold"))
        lbl.pack()
        return lbl

    def update_dashboard_stats(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(quantity) FROM books")
            books_total = cursor.fetchone()[0]
            self.c1_label.configure(text=str(books_total if books_total else 0))
            
            cursor.execute("SELECT COUNT(*) FROM members")
            self.c2_label.configure(text=str(cursor.fetchone()[0]))
            
            cursor.execute("SELECT COUNT(*) FROM issue_records WHERE return_date IS NULL")
            self.c3_label.configure(text=str(cursor.fetchone()[0]))
            conn.close()
        except: pass

    def run_reminders(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            today = date.today()
            target_7 = today + timedelta(days=7)
            target_1 = today + timedelta(days=1)
            
            query = """SELECT i.issue_id, m.email, m.name, b.title, i.due_date 
                       FROM issue_records i 
                       JOIN members m ON i.member_id = m.member_id 
                       JOIN books b ON i.book_id = b.book_id 
                       WHERE i.return_date IS NULL AND (i.due_date = %s OR i.due_date = %s)"""
            cursor.execute(query, (target_7, target_1))
            rows = cursor.fetchall()
            count = 0
            for row in rows:
                if row[1]: # if email exists
                    send_email(row[1], "Library Due Date Reminder", f"Dear {row[2]},\nYour borrowed book '{row[3]}' is due on {row[4]}. Please return it on time to avoid fine charges.")
                    count += 1
            conn.close()
            messagebox.showinfo("Done", f"Processed Reminders. {count} email(s) scheduled/sent!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= MANAGE BOOKS ================= #
    def show_books(self):
        self.clear_container()
        self.current_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(self.current_frame, text="Manage Books", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=10)
        
        tools_frame = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        tools_frame.pack(fill="x", pady=10, padx=10)
        
        self.b_search = ctk.CTkEntry(tools_frame, placeholder_text="Search Book ID...")
        self.b_search.pack(side="left", padx=5)
        ctk.CTkButton(tools_frame, text="Search", width=80, command=self.search_book).pack(side="left", padx=5)
        ctk.CTkButton(tools_frame, text="Refresh", width=80, fg_color="gray", command=self.load_books).pack(side="left", padx=5)
        
        ctk.CTkButton(tools_frame, text="Delete Selected", width=120, fg_color="#C0392B", hover_color="#922B21", command=self.delete_book).pack(side="right", padx=5)
        ctk.CTkButton(tools_frame, text="Edit Selected", width=120, command=self.open_edit_book).pack(side="right", padx=5)
        ctk.CTkButton(tools_frame, text="+ Add New Book", width=120, command=lambda: self.open_book_window("add")).pack(side="right", padx=5)
        
        columns = ("ID", "Title", "Author", "Category", "Quantity", "Status", "Date")
        self.book_tree = ttk.Treeview(self.current_frame, columns=columns, show="headings")
        for col in columns:
            self.book_tree.heading(col, text=col, anchor="center")
            self.book_tree.column(col, anchor="center", width=100)
        self.book_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.load_books()

    def load_books(self, query=None):
        for item in self.book_tree.get_children(): self.book_tree.delete(item)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            if query:
                cursor.execute("SELECT book_id, title, author, category, quantity, status, added_date FROM books WHERE book_id LIKE %s", (f"%{query}%",))
            else:
                cursor.execute("SELECT book_id, title, author, category, quantity, status, added_date FROM books")
            for row in cursor.fetchall():
                self.book_tree.insert("", "end", values=row)
            conn.close()
        except Exception as e: print(e)

    def search_book(self):
        self.load_books(self.b_search.get())

    def open_book_window(self, mode="add", data=None):
        win = ctk.CTkToplevel(self)
        win.title("Book Information")
        win.geometry("400x500")
        win.resizable(False, False)
        win.attributes("-topmost", True)
        win.grab_set()
        
        ctk.CTkLabel(win, text="Book details", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        b_id = ctk.CTkEntry(win, placeholder_text="Book ID", width=250)
        b_id.pack(pady=10)
        b_title = ctk.CTkEntry(win, placeholder_text="Title", width=250)
        b_title.pack(pady=10)
        b_author = ctk.CTkEntry(win, placeholder_text="Author", width=250)
        b_author.pack(pady=10)
        b_cat = ctk.CTkEntry(win, placeholder_text="Category", width=250)
        b_cat.pack(pady=10)
        b_qty = ctk.CTkEntry(win, placeholder_text="Quantity", width=250)
        b_qty.pack(pady=10)
        
        if mode == "edit" and data:
            b_id.insert(0, data[0])
            b_id.configure(state="disabled")
            b_title.insert(0, data[1])
            b_author.insert(0, data[2])
            b_cat.insert(0, data[3])
            b_qty.insert(0, data[4])

        def save():
            vid = b_id.get().strip()
            vtitle = b_title.get().strip()
            vaut = b_author.get().strip()
            vcat = b_cat.get().strip()
            vqty = b_qty.get().strip()
            if not vid or not vtitle or not vaut or not vqty:
                win.attributes("-topmost", False); messagebox.showwarning("Validation Error", "All fields are required!", parent=win); win.attributes("-topmost", True)
                return
            if not vqty.isdigit():
                win.attributes("-topmost", False); messagebox.showwarning("Validation Error", "Quantity must be a number!", parent=win); win.attributes("-topmost", True)
                return
                
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                if mode == "add":
                    cursor.execute("INSERT INTO books (book_id, title, author, category, quantity, added_date) VALUES (%s, %s, %s, %s, %s, %s)",
                                   (vid, vtitle, vaut, vcat, vqty, date.today()))
                else:
                    cursor.execute("UPDATE books SET title=%s, author=%s, category=%s, quantity=%s WHERE book_id=%s",
                                   (vtitle, vaut, vcat, vqty, vid))
                conn.commit()
                conn.close()
                win.attributes("-topmost", False)
                messagebox.showinfo("Success", "Saved Successfully!")
                self.load_books()
                win.destroy()
            except Exception as e:
                win.attributes("-topmost", False); messagebox.showerror("Error", str(e)); win.attributes("-topmost", True)
                
        ctk.CTkButton(win, text="Save", width=250, command=save).pack(pady=20)

    def open_edit_book(self):
        sel = self.book_tree.focus()
        if not sel:
            messagebox.showwarning("Warning", "Select a book!")
            return
        data = self.book_tree.item(sel, 'values')
        self.open_book_window("edit", data)

    def delete_book(self):
        sel = self.book_tree.focus()
        if not sel: return
        bid = self.book_tree.item(sel, 'values')[0]
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE book_id = %s", (bid,))
            conn.commit()
            conn.close()
            self.load_books()
        except Exception as e: messagebox.showerror("Error", str(e))

    # ================= MANAGE MEMBERS ================= #
    def show_members(self):
        self.clear_container()
        self.current_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(self.current_frame, text="Manage Members", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=10)
        
        tools_frame = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        tools_frame.pack(fill="x", pady=10, padx=10)
        
        self.m_search = ctk.CTkEntry(tools_frame, placeholder_text="Search ID...")
        self.m_search.pack(side="left", padx=5)
        ctk.CTkButton(tools_frame, text="Search", width=80, command=self.search_member).pack(side="left", padx=5)
        ctk.CTkButton(tools_frame, text="Refresh", width=80, fg_color="gray", command=self.load_members).pack(side="left", padx=5)
        
        ctk.CTkButton(tools_frame, text="History", width=80, fg_color="#F39C12", hover_color="#D68910", command=self.view_member_history).pack(side="right", padx=5)
        ctk.CTkButton(tools_frame, text="Delete Selected", width=120, fg_color="#C0392B", hover_color="#922B21", command=self.delete_member).pack(side="right", padx=5)
        ctk.CTkButton(tools_frame, text="Edit Selected", width=120, command=self.open_edit_member).pack(side="right", padx=5)
        ctk.CTkButton(tools_frame, text="+ Add New Member", width=120, command=lambda: self.open_member_window("add")).pack(side="right", padx=5)
        
        columns = ("ID", "Name", "Phone", "Email", "Address", "Joined")
        self.mem_tree = ttk.Treeview(self.current_frame, columns=columns, show="headings")
        for col in columns:
            self.mem_tree.heading(col, text=col, anchor="center")
            self.mem_tree.column(col, anchor="center", width=100)
        self.mem_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.load_members()

    def load_members(self, query=None):
        for item in self.mem_tree.get_children(): self.mem_tree.delete(item)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            if query:
                cursor.execute("SELECT member_id, name, phone, email, address, joined_date FROM members WHERE member_id LIKE %s", (f"%{query}%",))
            else:
                cursor.execute("SELECT member_id, name, phone, email, address, joined_date FROM members")
            for row in cursor.fetchall():
                self.mem_tree.insert("", "end", values=row)
            conn.close()
        except Exception as e: print(e)

    def search_member(self):
        self.load_members(self.m_search.get())

    def open_member_window(self, mode="add", data=None):
        win = ctk.CTkToplevel(self)
        win.title("Member Information")
        win.geometry("400x500")
        win.resizable(False, False)
        win.attributes("-topmost", True)
        win.grab_set()
        
        ctk.CTkLabel(win, text="Member Details", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        m_id = ""
        m_name = ctk.CTkEntry(win, placeholder_text="Full Name", width=250)
        m_name.pack(pady=10)
        m_phone = ctk.CTkEntry(win, placeholder_text="Phone Number", width=250)
        m_phone.pack(pady=10)
        m_email = ctk.CTkEntry(win, placeholder_text="Email Address", width=250)
        m_email.pack(pady=10)
        m_address = ctk.CTkEntry(win, placeholder_text="Address", width=250)
        m_address.pack(pady=10)
        
        if mode == "edit" and data:
            m_id = data[0]
            m_name.insert(0, data[1])
            m_phone.insert(0, data[2])
            m_email.insert(0, data[3])
            m_address.insert(0, data[4])

        def save():
            vn = m_name.get().strip()
            vp = m_phone.get().strip()
            ve = m_email.get().strip()
            va = m_address.get().strip()
            if not vn or not vp:
                win.attributes("-topmost", False); messagebox.showwarning("Error", "Name and Phone required!", parent=win); win.attributes("-topmost", True)
                return
                
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                if mode == "add":
                    cursor.execute("INSERT INTO members (name, phone, email, address, joined_date) VALUES (%s, %s, %s, %s, %s)",
                                   (vn, vp, ve, va, date.today()))
                else:
                    cursor.execute("UPDATE members SET name=%s, phone=%s, email=%s, address=%s WHERE member_id=%s",
                                   (vn, vp, ve, va, m_id))
                conn.commit()
                conn.close()
                win.attributes("-topmost", False)
                messagebox.showinfo("Success", "Saved Successfully!")
                self.load_members()
                win.destroy()
            except Exception as e:
                win.attributes("-topmost", False); messagebox.showerror("Error", str(e)); win.attributes("-topmost", True)
                
        ctk.CTkButton(win, text="Save", width=250, command=save).pack(pady=20)

    def open_edit_member(self):
        sel = self.mem_tree.focus()
        if not sel: return
        data = self.mem_tree.item(sel, 'values')
        self.open_member_window("edit", data)

    def delete_member(self):
        sel = self.mem_tree.focus()
        if not sel: return
        mid = self.mem_tree.item(sel, 'values')[0]
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM members WHERE member_id = %s", (mid,))
            conn.commit()
            conn.close()
            self.load_members()
        except Exception as e: messagebox.showerror("Error", str(e))
        
    def view_member_history(self):
        sel = self.mem_tree.focus()
        if not sel:
            messagebox.showwarning("Warning", "Select a member to view history!")
            return
        m_id = self.mem_tree.item(sel, 'values')[0]
        m_name = self.mem_tree.item(sel, 'values')[1]
        
        hist_win = ctk.CTkToplevel(self)
        hist_win.title(f"History - {m_name}")
        hist_win.geometry("800x400")
        hist_win.attributes("-topmost", True)
        
        cols = ("Issue ID", "Book ID", "Title", "Issue Date", "Due Date", "Return Date", "Fine")
        tree = ttk.Treeview(hist_win, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center")
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT i.issue_id, i.book_id, b.title, i.issue_date, i.due_date, IFNULL(i.return_date, 'Not Returned'), i.fine FROM issue_records i JOIN books b ON i.book_id = b.book_id WHERE i.member_id = %s", (m_id,))
            for r in cursor.fetchall():
                tree.insert("", "end", values=r)
            conn.close()
        except: pass

    # ================= ISSUE & RETURN BOOKS ================= #
    def show_issue(self):
        self.clear_container()
        self.current_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(self.current_frame, text="Issue & Return Books", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=10)

        tabs = ctk.CTkTabview(self.current_frame, width=500, height=400)
        tabs.pack(pady=20)
        tabs.add("Issue Book")
        tabs.add("Return Book")

        ctk.CTkLabel(tabs.tab("Issue Book"), text="Issue a Book", font=ctk.CTkFont(size=18)).pack(pady=10)
        self.i_b_id = ctk.CTkEntry(tabs.tab("Issue Book"), placeholder_text="Book ID", width=250)
        self.i_b_id.pack(pady=10)
        self.i_m_id = ctk.CTkEntry(tabs.tab("Issue Book"), placeholder_text="Member ID", width=250)
        self.i_m_id.pack(pady=10)
        ctk.CTkButton(tabs.tab("Issue Book"), text="Issue Book (14 Days)", command=self.issue_book, width=250).pack(pady=20)

        ctk.CTkLabel(tabs.tab("Return Book"), text="Return Book & Pay Fines", font=ctk.CTkFont(size=18)).pack(pady=10)
        self.r_b_id = ctk.CTkEntry(tabs.tab("Return Book"), placeholder_text="Book ID", width=250)
        self.r_b_id.pack(pady=10)
        self.r_m_id = ctk.CTkEntry(tabs.tab("Return Book"), placeholder_text="Member ID", width=250) # In case 1 book copied to multiples
        self.r_m_id.pack(pady=10)
        ctk.CTkButton(tabs.tab("Return Book"), text="Process Return", command=self.return_book, width=250).pack(pady=20)

    def issue_book(self):
        book_id = self.i_b_id.get().strip()
        member_id = self.i_m_id.get().strip()
        if not book_id.isdigit() or not member_id.isdigit():
            messagebox.showwarning("Error", "Valid IDs required!")
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check availability
            cursor.execute("SELECT quantity, title FROM books WHERE book_id=%s", (book_id,))
            res = cursor.fetchone()
            if not res or res[0] <= 0:
                messagebox.showerror("Error", "Book is not available (Quantity is 0)!")
                return
                
            cursor.execute("SELECT email, name FROM members WHERE member_id=%s", (member_id,))
            mres = cursor.fetchone()
            if not mres:
                messagebox.showerror("Error", "Member not found!")
                return
                
            # Issue
            due_date = date.today() + timedelta(days=14)
            cursor.execute("INSERT INTO issue_records (book_id, member_id, issue_date, due_date) VALUES (%s, %s, %s, %s)", 
                           (book_id, member_id, date.today(), due_date))
            cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id=%s", (book_id,))
            
            conn.commit()
            conn.close()
            
            # Send Email
            email, name = mres[0], mres[1]
            if email:
                txt = f"Hello {name},\n\nYou have successfully borrowed the book '{res[1]}' (ID: {book_id}).\nDue Date: {due_date}.\nPlease return it before the due date to avoid fine charges (Rs. 50/day).\n\nThank you,\nLibrary Management"
                send_email(email, "Book Issued Automatically", txt)

            messagebox.showinfo("Success", f"Issued! Due Date: {due_date}")
            self.i_b_id.delete(0, 'end'); self.i_m_id.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def return_book(self):
        book_id = self.r_b_id.get().strip()
        member_id = self.r_m_id.get().strip()
        if not book_id.isdigit() or not member_id.isdigit():
            messagebox.showwarning("Error", "Valid numeric IDs required!")
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT issue_id, due_date FROM issue_records WHERE book_id=%s AND member_id=%s AND return_date IS NULL", (book_id, member_id))
            record = cursor.fetchone()
            
            if not record:
                messagebox.showerror("Error", "No pending issue found for this Book and Member combination!")
                return
                
            due_date = record[1]
            today = date.today()
            fine = 0
            late_days = 0
            if today > due_date:
                late_days = (today - due_date).days
                fine = late_days * 50
                
            cursor.execute("UPDATE issue_records SET return_date=%s, fine=%s WHERE issue_id=%s", (today, fine, record[0]))
            cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE book_id=%s", (book_id,))
            conn.commit()
            conn.close()
            
            info = f"Book Returned Successfully!\nLate Days: {late_days}\nFine Applied: Rs. {fine}"
            messagebox.showinfo("Return Processed", info)
            self.r_b_id.delete(0, 'end'); self.r_m_id.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def logout(self):
        self.destroy()
        app = LoginWindow()
        app.mainloop()

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
