import sqlite3
import re


# Авторизация
def auth(login:str, password:str):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    current_user: str = 'none'
    sql.execute(f"SELECT Login FROM users WHERE Login = '{login}'")
    if sql.fetchone() is None:
       return 1
       db.close()
       sql.close()
    else:
         sql.execute(f"SELECT Password FROM users WHERE Password = '{password}'")
         if sql.fetchone() is None:
            return 2
            db.close()
            sql.close()
         else:
            current_user = login
            return 3
            db.close()
            sql.close()


# Регистрация
def register(login:str, password:str, first_name:str, last_name:str):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT * FROM users WHERE Login = '{login}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users (Login, Password, FirstName, LastName) "
                    f"VALUES ('{login}', '{password}', '{first_name}', '{last_name}')")
        db.commit()
        return True
        db.close()
        sql.close()
    else:
        return False
        db.close()
        sql.close()


# Проверка баланса
def balance_check(login:str):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT Balance FROM users WHERE Login = '{login}'")
    balance = sql.fetchone()
    return balance[0]
    db.close()
    sql.close()


# Депозит денег на счёт
def deposit(login:str, amount:float):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE users SET Balance = Balance + {amount} WHERE Login = '{login}'")
    db.commit()
    return True
    db.close()
    sql.close()


# Снятие денег со счёта
def withdraw(login:str, password:str, amount:float):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT Balance FROM users WHERE Login = '{login}' AND Password = '{password}'")
    if sql.fetchone() is None:
        return 1
    else:
        sql.execute(f"SELECT Balance FROM users WHERE Login = '{login}' AND Password = '{password}'")
        current_balance = sql.fetchone()
        if current_balance[0] >= amount:
            sql.execute(f"UPDATE users SET Balance = Balance - {amount} "
                        f"WHERE Login = '{login}' AND Password = '{password}'")
            db.commit()
            return 3
        else:
            return 2
    db.close()
    sql.close()


# Перевод денег пользователю
def send_money(login, recipient, amount):
    try:
        db = sqlite3.connect('server.db')
        sql = db.cursor()
        sql.execute(f"UPDATE users SET Balance = Balance - {amount} WHERE Login = '{login}'")
        db.commit()
        sql.execute(f"UPDATE users SET Balance = Balance + {amount} WHERE Login = '{recipient}'")
        db.commit()
        return True
    except Exception:
        return False
    db.close()
    sql.close()


# Проверка логина на корректность
def login_difficulty(login):
    if len(login) <= 6:
        return "Длина логина должна быть не менее 6 символов."
    words = all(ord('а') > ord(char) or ord(char) > ord('я') for char in login.lower())
    if words == False:
        return "Логин должен быть написан на латиннице"
    allowed_characters = {'-', '_'}
    spec_symbols = all(char.isalnum() or char in allowed_characters for char in login)
    if spec_symbols == False:
        return "В логине может использоваться только '-' или '_'."
    return True
    

# Проверка пароля на сложность
def password_difficulty(password):
    if len(password) < 8:
        return "Длина пароля должна быть не менее 8 символов."
    if not re.search(r"[A-Z]", password):
        return "Пароль должен содержать хотя бы одну букву в верхнем регистре."
    if not re.search(r"[a-z]", password):
        return "Пароль должен содержать хотя бы одну букву в нижнем регистре."
    if not re.search(r"\d", password):
        return "Пароль должен содержать хотя бы одну цифру."
    if not re.search(r"\W", password):
        return "Пароль должен содержать хотя бы один специальный символ."
    return True


# Проверка имени и фамилии на корректность
def check_name(name):
    if len(name) == 0:
        return "Имя и фамилия не должны быть пустыми."
    if len(name) > 50:
        return "Имя и фамилия не должны превышать 50 символов в длину."
    if not name.isalpha():
        return "Имя и фамилия должны содержать только буквы."
    return True


# Проверка логина по базе данных
def login_check(login):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT Login FROM users WHERE Login = '{login}'")
    if sql.fetchone() is None:
        return False
    else:
        return True
    db.close()
    sql.close()


# Проверка пароля по базе данных
def password_check(login, password):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT Password FROM users WHERE Login = '{login}'"
                f"AND Password = '{password}'")
    if sql.fetchone() is None:
        return False
    else:
        return True
    db.close()
    sql.close()


# Функция которая возвращает имя
def get_name(login):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT FirstName, LastName FROM users WHERE Login = '{login}'")
    name, *names = (sql.fetchall())
    if name is None:
        return False
    else:
        return name
    db.close()
    sql.close()