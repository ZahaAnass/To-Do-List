# Modern Todo List Application

A feature-rich Todo List application built with Python and Tkinter.

## Features

- Add tasks with title, description, due date, and status.
- Edit existing tasks.
- Delete tasks.
- Mark tasks as completed or pending.
- Search tasks by keyword.
- Filter tasks by status (All, Pending, Completed).
- Modern and user-friendly interface.
- SQLite database for persistent storage.
- Simple date input (YYYY-MM-DD format).

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- SQLite3 (built into Python)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ZahaAnass/To-Do-List.git
   cd To-Do-List
   ```

2. Run the application:
   ```bash
   python3 todo_app.py
   ```

## Usage

1. **Add a New Task**  
   Use the left panel to add a new task. Provide the title, description, due date (in `YYYY-MM-DD` format), and set the status.

2. **Edit a Task**
   Right-click on a task and select the "Edit" option to modify its details.

3. **Delete a Task**
   Right-click on a task and select the "Delete" option to remove it.

4. **Mark Task as Complete or Pending**  
   Right-click on a task and choose "Mark Complete" or "Mark Pending" to update its status.

5. **Search for Tasks**  
   Use the search box at the top to find tasks by keywords in their title or description.

6. **Filter Tasks by Status**  
   Use the radio buttons to filter tasks by their status: All, Pending, or Completed.

7. **Persistent Storage**  
   All tasks are saved in an SQLite database, ensuring your data is not lost between sessions.

## File Structure

```
To-Do-List/
├── todo_app.py          # Main application file
├── database.py          # Handles SQLite database operations
├── interface.py     # Contains reusable UI components
├── README.md            # Project documentation
```
