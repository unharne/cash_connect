from functions import *


# Стартовое окно
def main():
    while True:
        print("Зарегистрировать новый аккаунт - введите 1\n"
              "Войти в существующий аккаунт - введите 2\n"
              "Выйти из приложения - введите 3\n")
        message = input()
        if message == "1":
            user_reg()
        elif message == "2":
            user_auth()
        else:
            break


# Регистрация
def user_reg():
    while True:
        while True:
            login = input("Придумайте логин: \n")
            result = login_difficulty(login)
            if result == True:
                break
            else:
                print(result)
                continue
            check = login_check(login)
            if check == True:
                print(f"Пользователь {login} уже существует!")
                continue
            else:
                break
        while True:
            password = input("Придумайте пароль: \n")
            result = password_difficulty(password)
            if result == True:
                break
            else:
                print(result)
                continue
        while True:
            first_name = input("Введите имя: \n")
            result = check_name(first_name)
            if result == True:
                pass
            else:
                print(result)
                continue
            last_name = input("Введите фамилию: \n")
            result = check_name(last_name)
            if result == True:
                pass
            else:
                print(result)
                continue
            register(login, password, first_name, last_name)
            print("Успешная регистрация! \n")
            menu(login, password, first_name, last_name)


# Вход в аккаунт
def user_auth():
    while True:
        login = str(input("Введите логин: \n"))
        check = login_check(login)
        if check == False:
            print("Такого пользователя не существует")
            continue
        password = str(input("Введите пароль: \n"))
        check = password_check(login, password)
        if check == False:
            print("Неверный пароль!")
            continue
        result = auth(login, password)
        if result == 1:
            print("Такого пользователя не существует")
        elif result == 2:
            print("Неверный пароль!")
        elif result == 3:
            names = get_name(login)
            first_name, last_name = names[0], names[1]
            menu(login, password, first_name, last_name)


# Главное меню
def menu(login, password, first_name, last_name):
    while True:
        print(f"\nЗдравствуйте {first_name.title()} {last_name.title()}!\n"
              f"Что вы хотите сделать сегодня?\n"
            "Введите '1' чтобы снять деньги\n"
            "Введите '2' чтобы пополнить счёт\n"
            "Введите '3' чтобы узнать баланс счёта\n"
            "Введите '4' чтобы перевести деньги\n"
            "Введите '5' чтобы выйти\n")
        choiсe = input()
        if choiсe == '1':
            while True:
                try:
                    amount = input("Введите 'q' чтобы выйти.\n"
                                         "Введите сумму для снятия: \n")
                except Exception:
                    print("Ошибка ввода.")
                    continue
                if str(amount) == 'q':
                    break
                elif float(amount) < 1:
                    print("Вы можете снять не меньше 1 рубля.")
                    continue
                else:
                    msg = withdraw(login, password, amount)
                    if msg == 1:
                        print("Ошибка!Попробуйте ввести другие даннные\n")
                        continue
                    elif msg == 2:
                        print("Недостаточно средств!\n")
                        continue
                    elif msg == 3:
                        print("\nУспешно снято -", amount, "руб")
                        break
        elif choiсe == '2':
            while True:
                try:
                    amount = input("Введите 'q' чтобы выйти.\n"
                                         "Положите деньги в банкомат: \n")
                except Exception:
                    print("Ошибка ввода.")
                    continue
                if str(amount) == 'q':
                    menu()
                elif float(amount) < 1:
                    print("Вы не можете внести меньше 1 рубля.")
                    continue
                else:
                    deposit(login, amount)
                    print("\nУспешное пополнение -", amount, "руб")
        elif choiсe == '3':
            while True:
                print("\nБаланс -", balance_check(login), "руб")
                break
        elif choiсe == '4':
            while True:
                recipient = str(input("Введите 'q' чтобы выйти.\n"
                                        "Введите логин пользователя которому хотите перевести деньги:\n"))
                if recipient == 'q':
                    break
                elif recipient == login:
                    print("Это ваш логин.")
                    continue
                search_login = login_check(recipient)
                if search_login == False:
                    print("Такого пользователя не существует.")
                    continue
                try:
                    amount = input("Введите 'q' чтобы выйти.\n"
                                         "Введите сумму для перевода:\n")
                except Exception:
                    print("Ошибка ввода.")
                    continue
                if str(amount) == 'q':
                    menu()
                elif float(amount) < 1:
                    print("Вы можете перевести не меньше 1 рубля.")
                    continue
                elif float(amount) > balance_check(login):
                    print("Недостаточно средств.")
                    continue
                else:
                    send_money(login, recipient, amount)
                    print("\nУспешно переведено -", amount, "руб")
                    break
        else:
            main()
            exit()



# Старт программы
main()