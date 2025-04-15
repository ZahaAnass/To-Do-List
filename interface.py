import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import database as db
from datetime import datetime

class TodoList:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Todo List")
        self.root.geometry("1000x600")
        self.root.configure(bg="#2C3E50")  # Dark blue-gray background
        # Create GUI elements
        self.create_gui()
        self.load_task_list()

    def create_gui(self):
        # Configure scrollbar style - simplified
        style = ttk.Style()
        style.theme_use('clam')
        
        # Simple scrollbar style
        style.configure("Vertical.TScrollbar",
                    background="#3498db",
                    troughcolor="#f0f0f0",
                    width=12,
                    arrowsize=12)
        
        # Configure Treeview
        style.configure("Treeview",
                    background="#ffffff",
                    foreground="#2C3E50",
                    fieldbackground="#ffffff",
                    rowheight=30)
        
        style.configure("Treeview.Heading",
                    background="#3498db",
                    foreground="white",
                    relief="flat",
                    font=('Helvetica', 10, 'bold'))
        
        # Configure Treeview colors and layout
        style.configure("Treeview",
                    background="#ffffff",
                    foreground="#2C3E50",
                    fieldbackground="#ffffff",
                    rowheight=30,
                    borderwidth=0,
                    font=('Helvetica', 10))
        
        # Configure Treeview header
        style.configure("Treeview.Heading",
                    background="#3498db",
                    foreground="white",
                    relief="flat",
                    font=('Helvetica', 10, 'bold'),
                    padding=5)
        
        # Configure selection colors
        style.map("Treeview",
                background=[('selected', '#2980b9')],
                foreground=[('selected', 'white')])
        
        # Configure header hover effect
        style.map("Treeview.Heading",
                background=[('active', '#2980b9')])

        # Left Panel - Task Input
        left_panel = Frame(self.root, bg="#34495E", padx=20, pady=20)  # Darker blue-gray background
        left_panel.pack(side=LEFT, fill=BOTH, expand=False, padx=10, pady=10)

        # Title
        Label(left_panel, text="Add New Task", font=("Helvetica", 16, "bold"), bg="#34495E", fg="#ECF0F1").pack(anchor="w", pady=(0, 20))
        
        # Task Title
        Label(left_panel, text="Title:", bg="#34495E", fg="#ECF0F1").pack(anchor="w")
        self.title_entry = Entry(left_panel, width=30, bg="#ECF0F1", fg="#2C3E50", relief=FLAT)
        self.title_entry.pack(anchor="w", pady=(0, 10), fill=X)

        # Description
        Label(left_panel, text="Description:", bg="#34495E", fg="#ECF0F1").pack(anchor="w")
        self.desc_entry = Text(left_panel, width=30, height=5, bg="#ECF0F1", fg="#2C3E50")
        self.desc_entry.pack(anchor="w", pady=(0, 10), fill=X)

        # Due Date
        Label(left_panel, text="Due Date:", bg="#34495E", fg="#ECF0F1").pack(anchor="w")
        self.due_date_entry = Entry(left_panel, width=30, bg="#ECF0F1", fg="#2C3E50")
        self.due_date_entry.insert(0, 'YYYY-MM-DD')
        self.due_date_entry.bind('<FocusIn>', lambda e: self.due_date_entry.delete(0, END) if self.due_date_entry.get() == 'YYYY-MM-DD' else None)
        self.due_date_entry.pack(anchor="w", pady=(0, 10), fill=X)

        # Status
        Label(left_panel, text="Status:", bg="#34495E", fg="#ECF0F1").pack(anchor="w")
        self.status_var = StringVar(value="pending")
        status_frame = Frame(left_panel, bg="#34495E")
        status_frame.pack(anchor="w", pady=(0, 20), fill=X)
        
        Radiobutton(status_frame, text="Pending", variable=self.status_var, value="pending", bg="#34495E", fg="#ECF0F1", selectcolor="#2C3E50").pack(side=LEFT)
        Radiobutton(status_frame, text="Completed", variable=self.status_var, value="completed", bg="#34495E", fg="#ECF0F1", selectcolor="#2C3E50").pack(side=LEFT)

        # Add Button
        add_button = Button(left_panel, text="Add Task", 
                            bg="#1ABC9C", fg="#ECF0F1",
                            activebackground="#16A085",  
                            activeforeground="#ffffff",
                            font=("Helvetica", 10, "bold"),
                            pady=5,
                            command=self.add_task)
        add_button.pack(fill=X, pady=(0, 10))

        # Edit Button
        edit_button = Button(left_panel, text="Edit Task",
                            bg="#F39C12", fg="#ECF0F1",
                            activebackground="#D68910",  
                            activeforeground="#ffffff",
                            font=("Helvetica", 10, "bold"),
                            pady=5,
                            command=self.edit_task)
        edit_button.pack(fill=X, pady=(0, 10))

        # Delete Button
        delete_button = Button(left_panel, text="Delete Task",
                                bg="#E74C3C", fg="#ECF0F1",
                                activebackground="#CB4335",  
                                activeforeground="#ffffff",
                                font=("Helvetica", 10, "bold"),
                                pady=5,
                                command=self.delete_task)
        delete_button.pack(fill=X, pady=(0, 10))

        # Mark as Complete/Incomplete Button
        toggle_button = Button(left_panel, text="Toggle Complete",
                                bg="#3498DB", fg="#ECF0F1",
                                activebackground="#2E86C1",  
                                activeforeground="#ffffff",
                                font=("Helvetica", 10, "bold"),
                                pady=5,
                                command=self.toggle_complete)
        toggle_button.pack(fill=X, pady=(0, 10))

        # Right Panel - Task List
        right_panel = Frame(self.root, bg="#2C3E50")
        right_panel.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        # Search and Filter Frame
        control_frame = Frame(right_panel, bg="#34495E")
        control_frame.pack(fill=X, pady=(0, 10))

        # Search
        self.search_var = StringVar()
        search_entry = Entry(control_frame, textvariable=self.search_var, width=30, bg="#ECF0F1", fg="#2C3E50")
        search_entry.pack(side=LEFT, padx=5)
        search_entry.insert(0, "Search tasks...")
        search_entry.bind('<FocusIn>', lambda e: search_entry.delete(0, END) if search_entry.get() == "Search tasks..." else None)

        # Search Button
        search_button = Button(control_frame, text="Search",
                                bg="#1ABC9C", fg="#ECF0F1",
                                activebackground="#16A085",  
                                activeforeground="#ffffff",
                                font=("Helvetica", 10, "bold"),
                                command=self.search_task)
        search_button.pack(side=LEFT, padx=5)

        # Filter
        self.filter_var = StringVar(value="all")
        filter_frame = Frame(control_frame, bg="#34495E")
        filter_frame.pack(side=RIGHT)
        
        Label(filter_frame, text="Filter by Status:", bg="#34495E", fg="#ECF0F1").pack(side=LEFT, padx=5)
        Radiobutton(filter_frame, text="All", variable=self.filter_var, value="all", bg="#34495E", fg="#ECF0F1", selectcolor="#2C3E50", command=self.filter_status).pack(side=LEFT)
        Radiobutton(filter_frame, text="Pending", variable=self.filter_var, value="pending", bg="#34495E", fg="#ECF0F1", selectcolor="#2C3E50", command=self.filter_status).pack(side=LEFT)
        Radiobutton(filter_frame, text="Completed", variable=self.filter_var, value="completed", bg="#34495E", fg="#ECF0F1", selectcolor="#2C3E50", command=self.filter_status).pack(side=LEFT)

        # Task List with updated style
        columns = ('id', 'title', 'description', 'due_date', 'status')
        self.tree = ttk.Treeview(right_panel, columns=columns, show='headings', style="Treeview")
        
        # Define column headings with updated style
        for col in columns:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, anchor='center')
        
        # Adjust column widths
        self.tree.column('id', width=50, minwidth=50)
        self.tree.column('title', width=150, minwidth=150)
        self.tree.column('description', width=250, minwidth=200)
        self.tree.column('due_date', width=100, minwidth=100)
        self.tree.column('status', width=100, minwidth=100)
                    
        # Scrollbar with updated custom style
        scrollbar = ttk.Scrollbar(right_panel, orient=VERTICAL, command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.tag_configure('evenrow', background="#ffffff")
        self.tree.tag_configure('oddrow', background="#ebf5fb")
        
        # Pack the treeview and scrollbar
        self.tree.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        scrollbar.pack(side=RIGHT, fill=Y)

        # Sort column function
        self.last_clicked = None
        self.click_count = 0

        def sort_column(clicked):
            if self.last_clicked != clicked:
                self.click_count = 0
                self.last_clicked = clicked
            self.click_count += 1
            order = "DESC" if self.click_count % 2 == 0 else "ASC"

            # Clear the current task list
            self.tree.delete(*self.tree.get_children())

            # Fetch sorted tasks from the database
            tasks = db.sort_tasks(clicked, order)

            # Populate the treeview with sorted tasks
            for index, task in enumerate(tasks):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=task, tags=(tag,))

            self.last_clicked = clicked

        # Bind the sort_column function to column headers
        for column_name in ('id', 'title', 'description', 'due_date', 'status'):
            self.tree.heading(column_name, text=column_name.title(), command=lambda c=column_name: sort_column(c))

    def load_task_list(self):
        #Clear the exeisting task list
        self.tree.delete(*self.tree.get_children())
        tasks = db.get_all_tasks()
        for index, task in enumerate(tasks):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=task, tags=(tag,))

    def get_selected_task(self):
        selected = self.tree.focus()  # Get selected item ID
        if selected:
            return self.tree.item(selected)['values']  # returns [id, title, description, due_date, status]
        return None

    def add_task(self):
        # Implementation for adding a task
        title = self.title_entry.get()
        description = self.desc_entry.get("1.0", "end-1c")
        due_date = self.due_date_entry.get()
        status = self.status_var.get()
        if not title or not description or not due_date:
            messagebox.showerror("Error", "All fields are required!")
            return
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Due date must be in YYYY-MM-DD format!")
            return
        db.add_task(title, description, due_date, status)
        self.title_entry.delete(0, END)
        self.desc_entry.delete("1.0", "end")
        self.due_date_entry.delete(0, END)
        messagebox.showinfo("Success", "Task added successfully!")
        self.load_task_list()

    def edit_task(self):
        task = self.get_selected_task()
        if not task:
            messagebox.showerror("Error", "No task selected!")
            return
        else:
            new_window = Toplevel(self.root)
            new_window.title("Edit Task")
            new_window.geometry("400x500+750+400")
            new_window.resizable(False, False)
            new_window.configure(bg="#34495E")  # Darker blue-gray background

            # Title Label
            tk.Label(new_window, text="Edit Task", font=("Helvetica", 16, "bold"), bg="#34495E", fg="#ECF0F1").pack(pady=10)

            # Title Entry
            tk.Label(new_window, text="Title:", font=("Helvetica", 12), bg="#34495E", fg="#ECF0F1").pack(anchor="w", padx=10)
            title_entry = Entry(new_window, font=("Helvetica", 12), bg="#ECF0F1", fg="#2C3E50", relief=FLAT)
            title_entry.insert(0, task[1])  # Pre-fill with current title
            title_entry.pack(fill="x", pady=5, padx=10)

            # Description Entry
            tk.Label(new_window, text="Description:", font=("Helvetica", 12), bg="#34495E", fg="#ECF0F1").pack(anchor="w", padx=10)
            desc_entry = Text(new_window, font=("Helvetica", 12), height=5, bg="#ECF0F1", fg="#2C3E50", relief=FLAT)
            desc_entry.insert("1.0", task[2])  # Pre-fill with current description
            desc_entry.pack(fill="x", pady=5, padx=10)

            # Due Date Entry
            tk.Label(new_window, text="Due Date (YYYY-MM-DD):", font=("Helvetica", 12), bg="#34495E", fg="#ECF0F1").pack(anchor="w", padx=10)
            due_date_entry = Entry(new_window, font=("Helvetica", 12), bg="#ECF0F1", fg="#2C3E50", relief=FLAT)
            due_date_entry.insert(0, task[3])  # Pre-fill with current due date
            due_date_entry.pack(fill="x", pady=5, padx=10)

            # Status Radio Buttons
            tk.Label(new_window, text="Status:", font=("Helvetica", 12), bg="#34495E", fg="#ECF0F1").pack(anchor="w", padx=10)
            status_var = StringVar(value=task[4])  # Pre-fill with current status
            status_frame = Frame(new_window, bg="#34495E")
            status_frame.pack(fill="x", pady=5, padx=10)
            Radiobutton(status_frame, text="Pending", variable=status_var, value="pending", bg="#34495E", fg="#ECF0F1", selectcolor="#2C3E50").pack(side=LEFT, padx=5)
            Radiobutton(status_frame, text="Completed", variable=status_var, value="completed", bg="#34495E", fg="#ECF0F1", selectcolor="#2C3E50").pack(side=LEFT, padx=5)

            def save_changes():
                new_title = title_entry.get()
                new_description = desc_entry.get("1.0", "end-1c")
                new_due_date = due_date_entry.get()
                new_status = status_var.get()
                if not new_title or not new_description or not new_due_date:
                    messagebox.showerror("Error", "All fields are required!")
                    return
                try:
                    datetime.strptime(new_due_date, '%Y-%m-%d')
                except ValueError:
                    messagebox.showerror("Error", "Due date must be in YYYY-MM-DD format!")
                    return
                db.update_task(task[0], new_title, new_description, new_due_date, new_status)
                self.load_task_list()
                new_window.destroy()
                messagebox.showinfo("Success", "Task updated successfully!")

            def undo_changes():
                new_window.destroy()

            Button(new_window, text="Save Changes", bg="#4CAF50", fg="white", 
                    font=("Helvetica", 10, "bold"), command=save_changes).pack(pady=20, fill=X, padx=10)
            
            Button(new_window, text="Undo Changes", bg="#F44336", fg="white", 
                    font=("Helvetica", 10, "bold"), command=undo_changes).pack(pady=20, fill=X, padx=10)


    def delete_task(self):
        # Delete the selected task
        task = self.get_selected_task()
        if not task:
            messagebox.showerror("Error", "No task selected!")
            return
        
        def valider():
            task_id = task[0]
            db.delete_task(task_id)
            self.load_task_list()
            new_window.destroy()
            messagebox.showinfo("Succès", "Produit supprimé avec succès")

        def annuler():
            new_window.destroy()
            messagebox.showinfo("Succès", "Produit n'est pas supprimé")

        new_window = Toplevel(self.root)
        new_window.title("Supprimer un produit")
        new_window.geometry("300x80+800+550")
        new_window.resizable(False, False)
        button_valider = tk.Button(new_window, text="Valider", command=valider, bg="#2ecc71", fg="white", activebackground="#27ae60", activeforeground="white")
        button_valider.grid(row=0, column=0, pady=20, padx=50)
        button_annuler = tk.Button(new_window, text="Annuler", command=annuler, bg="#e74c3c", fg="white", activebackground="#c0392b", activeforeground="white")
        button_annuler.grid(row=0, column=1)

    def toggle_complete(self):
        task = self.get_selected_task()
        if not task: 
            messagebox.showerror('Error', "No Task Selected!")
            return
        
        task_id = task[0]
        task_status = task[4]
        if task_status == "pending":
            task_status = "completed"
            db.update_task_status(task_id, task_status)
        else:
            task_status = "pending"
            db.update_task_status(task_id, task_status)
        self.load_task_list()
        messagebox.showinfo("Success", f"Task status updated to {task_status}.")

    def search_task(self):
        # Search for tasks
        keyword = self.search_var.get().strip()
        if not keyword:
            messagebox.showerror("Error", "Please enter a keyword to search!")
            return
        # Fetch tasks matching the keyword
        tasks = db.search_tasks(keyword)
        if not tasks:
            messagebox.showinfo("Info", "No tasks found matching the keyword.")
            return
        
        # Clear the current task list
        self.tree.delete(*self.tree.get_children())
        
        # Populate the treeview with the search results
        for task in tasks:
            self.tree.insert('', 'end', values=task)

    def filter_status(self):
        # Filter tasks by status
        status = self.filter_var.get()
        
        # Clear the current task list while preserving the scrollbar style
        self.tree.delete(*self.tree.get_children())
        
        # Get filtered tasks
        tasks = db.filter_tasks_by_status(status)
        
        # Reinsert tasks with preserved styling
        for index, task in enumerate(tasks):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=task, tags=(tag,))

    def run(self):
        # Run the main loop from the class
        self.root.mainloop()