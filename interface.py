from tkinter import *
from tkinter import ttk, messagebox
import database as db

class TodoList:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List")
        self.root.geometry("600x400")