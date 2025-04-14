import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import database as db
from datetime import datetime

class TodoList:
    def __init__(self):
        self.root = Tk()
        self.root.title("Modern Todo List")
        self.root.geometry("1000x600")
        self.root.configure(bg="#000000")
        # Create GUI elements
        self.create_gui()
        self.load_task_list()

    def create_gui(self):
        # Left Panel - Task Input
        left_panel = Frame(self.root, bg="#ffffff", padx=20, pady=20)
        left_panel.pack(side=LEFT, fill=BOTH, expand=False, padx=10, pady=10)

        # Title
        Label(left_panel, text="Add New Task", font=("Helvetica", 16, "bold"), bg="#ffffff").pack(anchor="w", pady=(0, 20))
        
        # Task Title
        Label(left_panel, text="Title:", bg="#ffffff").pack(anchor="w")
        self.title_entry = Entry(left_panel, width=30)
        self.title_entry.pack(anchor="w", pady=(0, 10), fill=X)

        # Description
        Label(left_panel, text="Description:", bg="#ffffff").pack(anchor="w")
        self.desc_entry = Text(left_panel, width=30, height=5)
        self.desc_entry.pack(anchor="w", pady=(0, 10), fill=X)

        # Due Date
        Label(left_panel, text="Due Date:", bg="#ffffff").pack(anchor="w")
        self.due_date_entry = Entry(left_panel, width=30)
        self.due_date_entry.insert(0, 'YYYY-MM-DD')
        self.due_date_entry.bind('<FocusIn>', lambda e: self.due_date_entry.delete(0, END) if self.due_date_entry.get() == 'YYYY-MM-DD' else None)
        self.due_date_entry.pack(anchor="w", pady=(0, 10), fill=X)

        # Status
        Label(left_panel, text="Status:", bg="#ffffff").pack(anchor="w")
        self.status_var = StringVar(value="pending")
        status_frame = Frame(left_panel, bg="#ffffff")
        status_frame.pack(anchor="w", pady=(0, 20), fill=X)
        
        Radiobutton(status_frame, text="Pending", variable=self.status_var, value="pending", bg="#ffffff").pack(side=LEFT)
        Radiobutton(status_frame, text="Completed", variable=self.status_var, value="completed", bg="#ffffff").pack(side=LEFT)

        # Add Button
        Button(left_panel, text="Add Task", bg="#4CAF50", fg="white", 
                font=("Helvetica", 10, "bold"), pady=5, command=self.add_task).pack(fill=X, pady=(0, 10))

        # Edit Button
        Button(left_panel, text="Edit Task", bg="#FFC107", fg="white", 
                font=("Helvetica", 10, "bold"), pady=5, command=self.edit_task).pack(fill=X, pady=(0, 10))

        # Delete Button
        Button(left_panel, text="Delete Task", bg="#F44336", fg="white", 
                font=("Helvetica", 10, "bold"), pady=5, command=self.delete_task).pack(fill=X, pady=(0, 10))

        # Mark as Complete/Incomplete Button
        Button(left_panel, text="Toggle Complete", bg="#2196F3", fg="white", 
                font=("Helvetica", 10, "bold"), pady=5, command=self.toggle_complete).pack(fill=X, pady=(0, 10))

        # Right Panel - Task List
        right_panel = Frame(self.root, bg="#ffffff")
        right_panel.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        # Search and Filter Frame
        control_frame = Frame(right_panel, bg="#ffffff")
        control_frame.pack(fill=X, pady=(0, 10))

        # Search
        self.search_var = StringVar()
        search_entry = Entry(control_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=LEFT, padx=5)
        search_entry.insert(0, "Search tasks...")
        search_entry.bind('<FocusIn>', lambda e: search_entry.delete(0, END) if search_entry.get() == "Search tasks..." else None)

        # Search Button
        Button(control_frame, text="Search", bg="#4CAF50", fg="white", 
                font=("Helvetica", 10, "bold"), command=self.search_task).pack(side=LEFT, padx=5)

        # Filter
        self.filter_var = StringVar(value="all")
        filter_frame = Frame(control_frame, bg="#ffffff")
        filter_frame.pack(side=RIGHT)
        
        Label(filter_frame, text="Filter by Status:", bg="#ffffff").pack(side=LEFT, padx=5)
        Radiobutton(filter_frame, text="All", variable=self.filter_var, value="all", bg="#ffffff", command=self.filter_status).pack(side=LEFT)
        Radiobutton(filter_frame, text="Pending", variable=self.filter_var, value="pending", bg="#ffffff", command=self.filter_status).pack(side=LEFT)
        Radiobutton(filter_frame, text="Completed", variable=self.filter_var, value="completed", bg="#ffffff", command=self.filter_status).pack(side=LEFT)

        # Task List
        columns = ('id', 'title', 'description', 'due_date', 'status')
        self.tree = ttk.Treeview(right_panel, columns=columns, show='headings')
        
        # Define column headings
        self.tree.heading('id', text='ID')
        self.tree.heading('title', text='Title')
        self.tree.heading('description', text='Description')
        self.tree.heading('due_date', text='Due Date')
        self.tree.heading('status', text='Status')
        
        # Define column widths
        self.tree.column('id', width=50)
        self.tree.column('title', width=150)
        self.tree.column('description', width=250)
        self.tree.column('due_date', width=100)
        self.tree.column('status', width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(right_panel, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

    def load_task_list(self):
        #Clear the exeisting task list
        self.tree.delete(*self.tree.get_children())
        tasks = db.get_all_tasks()
        for task in tasks:
            self.tree.insert('', 'end', values=task)

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

            tk.Label(new_window, text="Title:").pack()
            title_entry = Entry(new_window, font=("Arial", 12))
            title_entry.insert(0, task[1])  # Pre-fill with current title
            title_entry.pack(fill="x", pady=10, padx=10)

            tk.Label(new_window, text="Description:").pack()
            desc_entry = Text(new_window, font=("Arial", 12), height=5)
            desc_entry.insert("1.0", task[2])  # Pre-fill with current description
            desc_entry.pack(fill="x", pady=10, padx=10)

            tk.Label(new_window, text="Due Date (YYYY-MM-DD):").pack()
            due_date_entry = Entry(new_window, font=("Arial", 12))
            due_date_entry.insert(0, task[3])  # Pre-fill with current due date
            due_date_entry.pack(fill="x", pady=10, padx=10)

            tk.Label(new_window, text="Status:").pack()
            status_var = StringVar(value=task[4])  # Pre-fill with current status
            status_frame = Frame(new_window)
            status_frame.pack(fill="x", pady=10, padx=10)
            Radiobutton(status_frame, text="Pending", variable=status_var, value="pending").pack(side=LEFT)
            Radiobutton(status_frame, text="Completed", variable=status_var, value="completed").pack(side=LEFT)

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
        """Search tasks by keyword."""
        # Implementation for searching tasks
        pass

    def filter_status(self):
        # Filter tasks by status
        status = self.filter_var.get()
        self.tree.delete(*self.tree.get_children())
        tasks = db.filter_tasks_by_status(status)
        for task in tasks:
            self.tree.insert('', 'end', values=task)


    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = TodoList()
    app.run()
