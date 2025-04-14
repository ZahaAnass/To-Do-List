import sqlite3 as db

def connect_db():
    conn = db.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'pending'
        );
    """)
    conn.commit()
    conn.close()

def add_task(title, description, due_date, status):
    conn = db.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        insert into tasks (title, description, due_date, status)
        values (?, ?, ?, ?);
        """, (title, description, due_date, status))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = db.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks;")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task(task_id, title, description, due_date, status):
    conn = db.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET title = ?, description = ?, due_date = ?, status = ?
        WHERE id = ?;
    """, (title, description, due_date, status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = db.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
    conn.commit()
    conn.close()

def update_task_status(task_id, status):
    conn = db.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET status = ?
        WHERE id = ?;
    """, (status, task_id))
    conn.commit()
    conn.close()

def search_tasks(keyword):
    conn = db.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM tasks
        WHERE title LIKE ? OR description LIKE ?LIKE ?;
    """, (f"%{keyword}%", f"%{keyword}%"))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def filter_tasks_by_status(status):
    conn = db.connect("data.db")
    cursor = conn.cursor()
    if status == "all":
        cursor.execute("SELECT * FROM tasks;")
    else:
        cursor.execute("""
            SELECT * FROM tasks
            WHERE status = ?;
        """, (status,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

