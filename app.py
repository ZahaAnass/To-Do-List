from tkinter import *
from interface import TodoList
import database as db

db.connect_db()

if __name__ == "__main__":
    root = Tk()
    root.title("Todo List")
    root.geometry("600x400")
    todo_list = TodoList(root)
    root.mainloop()