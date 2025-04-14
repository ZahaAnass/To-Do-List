import tkinter as tk
from tkinter import ttk, messagebox

class TodoList:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Modern Todo List")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")
        
        # Create GUI elements
        self.create_gui()

    def create_gui(self):
        # Left Panel - Task Input
        left_panel = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10, pady=10)

        # Title
        tk.Label(left_panel, text="Add New Task", font=("Helvetica", 16, "bold"), bg="#ffffff").pack(anchor="w", pady=(0, 20))
        
        # Task Title
        tk.Label(left_panel, text="Title:", bg="#ffffff").pack(anchor="w")
        self.title_entry = tk.Entry(left_panel, width=30)
        self.title_entry.pack(anchor="w", pady=(0, 10), fill=tk.X)

        # Description
        tk.Label(left_panel, text="Description:", bg="#ffffff").pack(anchor="w")
        self.desc_entry = tk.Text(left_panel, width=30, height=5)
        self.desc_entry.pack(anchor="w", pady=(0, 10), fill=tk.X)

        # Due Date
        tk.Label(left_panel, text="Due Date:", bg="#ffffff").pack(anchor="w")
        self.due_date_entry = tk.Entry(left_panel, width=30)
        self.due_date_entry.insert(0, 'YYYY-MM-DD')
        self.due_date_entry.bind('<FocusIn>', lambda e: self.due_date_entry.delete(0, tk.END) if self.due_date_entry.get() == 'YYYY-MM-DD' else None)
        self.due_date_entry.pack(anchor="w", pady=(0, 10), fill=tk.X)

        # Status
        tk.Label(left_panel, text="Status:", bg="#ffffff").pack(anchor="w")
        self.status_var = tk.StringVar(value="pending")
        status_frame = tk.Frame(left_panel, bg="#ffffff")
        status_frame.pack(anchor="w", pady=(0, 20), fill=tk.X)
        
        tk.Radiobutton(status_frame, text="Pending", variable=self.status_var, value="pending", bg="#ffffff").pack(side=tk.LEFT)
        tk.Radiobutton(status_frame, text="Completed", variable=self.status_var, value="completed", bg="#ffffff").pack(side=tk.LEFT)

        # Add Button
        tk.Button(left_panel, text="Add Task", bg="#4CAF50", fg="white", 
                 font=("Helvetica", 10, "bold"), pady=5).pack(fill=tk.X, pady=(0, 10))

        # Right Panel - Task List
        right_panel = tk.Frame(self.root, bg="#ffffff")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Search and Filter Frame
        control_frame = tk.Frame(right_panel, bg="#ffffff")
        control_frame.pack(fill=tk.X, pady=(0, 10))

        # Search
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(control_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.insert(0, "Search tasks...")
        search_entry.bind('<FocusIn>', lambda e: search_entry.delete(0, tk.END) if search_entry.get() == "Search tasks..." else None)

        # Filter
        self.filter_var = tk.StringVar(value="all")
        filter_frame = tk.Frame(control_frame, bg="#ffffff")
        filter_frame.pack(side=tk.RIGHT)
        
        tk.Radiobutton(filter_frame, text="All", variable=self.filter_var, value="all", bg="#ffffff").pack(side=tk.LEFT)
        tk.Radiobutton(filter_frame, text="Pending", variable=self.filter_var, value="pending", bg="#ffffff").pack(side=tk.LEFT)
        tk.Radiobutton(filter_frame, text="Completed", variable=self.filter_var, value="completed", bg="#ffffff").pack(side=tk.LEFT)

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
        scrollbar = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = TodoList()
    app.run()
