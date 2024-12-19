import tkinter as tk
from tkinter import messagebox
import sqlite3



def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()



def register_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Регистрация", "Пользователь успешно зарегистрирован!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует.")
    finally:
        conn.close()



def login_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None



def open_registration_window():
    registration_window = tk.Toplevel(root)
    registration_window.title("Регистрация")

    tk.Label(registration_window, text="Логин:").pack()
    username_entry = tk.Entry(registration_window)
    username_entry.pack()

    tk.Label(registration_window, text="Пароль:").pack()
    password_entry = tk.Entry(registration_window, show="*")
    password_entry.pack()

    def register():
        username = username_entry.get()
        password = password_entry.get()
        register_user(username, password)

    tk.Button(registration_window, text="Зарегистрироваться", command=register).pack()



def login():
    username = username_entry.get()
    password = password_entry.get()

    if login_user(username, password):
        messagebox.showinfo("Успех", "Авторизация успешна!")
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль.")



root = tk.Tk()
root.title("Авторизация")

create_db()  # Создаем базу данных

tk.Label(root, text="Логин:").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Пароль:").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Button(root, text="Войти", command=login).pack()
tk.Button(root, text="Регистрация", command=open_registration_window).pack()

root.mainloop()
