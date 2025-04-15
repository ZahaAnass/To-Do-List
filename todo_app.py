from tkinter import *
from interface import TodoList
import database as db

# Initialize the database
db.connect_db()

if __name__ == "__main__":
    # Create the main application window
    root = Tk()
    
    # Initialize the TodoList interface
    todo_list = TodoList(root)
    
    # Run the application
    todo_list.run()