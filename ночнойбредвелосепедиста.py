import sqlite3
import hashlib
from datetime import datetime

class velomagazin:
    def __init__(self):
        # Подключение к базе данных
        self.conn = sqlite3.connect('bikeshop.db')
        self.cursor = self.conn.cursor()
        # Создание таблиц при инициализации
        self.create_tables()

    def create_tables(self):
        # Создание таблиц, если они не существуют
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Пользователи (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Велосипеды (
                bike_id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT,
                brand TEXT,
                price REAL,
                quantity INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Запчасти (
                part_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                category TEXT,
                price REAL,
                quantity INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Заказы (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                order_date TEXT,
                FOREIGN KEY (user_id) REFERENCES Пользователи(user_id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ДеталиЗаказа (
                order_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                item_id INTEGER,
                item_type TEXT,  -- 'Велосипед' или 'Запчасть'
                quantity INTEGER,
                FOREIGN KEY (order_id) REFERENCES Заказы(order_id)
            )
        ''')

        self.conn.commit()

    def register_user(self, username, password):
        # Регистрация пользователя
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute('INSERT INTO Пользователи (username, password) VALUES (?, ?)', (username, hashed_password))
            self.conn.commit()
            print("Регистрация успешна")
        except sqlite3.IntegrityError:
            print("Пользователь с таким именем уже существует")

    def login_user(self, username, password):
        # Авторизация пользователя
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute('SELECT * FROM Пользователи WHERE username=? AND password=?', (username, hashed_password))
        user = self.cursor.fetchone()
        if user:
            print("Вход выполнен успешно.")
            self.current_user_id = user[0]
        else:
            print("Неверное имя пользователя или пароль.")

    def add_bike(self, model, brand, price, quantity):
        # Добавление велосипеда в инвентарь
        try:
            self.cursor.execute('INSERT INTO Велосипеды (model, brand, price, quantity) VALUES (?, ?, ?, ?)',
                                (model, brand, price, quantity))
            self.conn.commit()
            print("Велосипед успешно добавлен")
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении велосипеда: {e}")

    def add_bike_part(self, name, category, price, quantity):
        # Добавление запчасти в инвентарь
        try:
            self.cursor.execute('INSERT INTO Запчасти (name, category, price, quantity) VALUES (?, ?, ?, ?)',
                                (name, category, price, quantity))
            self.conn.commit()
            print("Запчасть успешно добавлена")
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении запчасти: {e}")

    def place_order(self, user_id, items):
        # Оформление заказа
        try:
            order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute('INSERT INTO Заказы (user_id, order_date) VALUES (?, ?)', (user_id, order_date))
            order_id = self.cursor.lastrowid

            for item_id, item_type, quantity in items:
                self.cursor.execute('INSERT INTO ДеталиЗаказа (order_id, item_id, item_type, quantity) VALUES (?, ?, ?, ?)',
                                    (order_id, item_id, item_type, quantity))
            
            self.conn.commit()
            print("Заказ успешно оформлен")
        except sqlite3.Error as e:
            print(f"Ошибка при оформлении заказа: {e}")

    def close_connection(self):
        # Закрытие соединения с базой данных
        self.conn.close()

# Пример использования
# if __name__ == "__main__":
#     velomagazin = velomagazin()
#     while True:
#         print("\nВыберите роль:")
#         print("1. Администратор")
#         print("2. Менеджер персонала")
#         print("3. Складской менеджер")
#         print("4. Кассир")
#         print("5. Бухгалтер")
#         print("0. Выход")

#         role_choice = input("Введите номер роли: ")

#         if role_choice == "1":
#             self.manage_users()
#         elif role_choice == "2":
#             self.manager_personnel_menu()
#         elif role_choice == "3":
#             self.warehouse_manager_menu()
#         elif role_choice == "4":
#             self.cashier_menu()
#         elif role_choice == "5":
#             self.accountant_menu()
#         elif role_choice == "0":
#             self.close_connection()
#             print("Выход из программы.")
#             break
#         else:
#             print("Некорректный выбор. Пожалуйста, введите корректный номер роли.")
# if __name__ == "__main__":
#     velomagazin = velomagazin()

#     while True:
#         print("\n--- Меню velomagazinа ---")
#         print("1. Регистрация пользователя")
#         print("2. Авторизация")
#         print("3. Добавить велосипед в инвентарь")
#         print("4. Добавить запчасть в инвентарь")
#         print("5. Оформить заказ")
#         print("0. Выйти")

#         choice = input("Выберите действие: ")
#         if choice == "1":
#             username = input("Введите имя пользователя: ")
#             password = input("Введите пароль: ")
#             velomagazin.register_user(username, password)

#         elif choice == "2":
#             username = input("Введите имя пользователя: ")
#             password = input("Введите пароль: ")
#             velomagazin.login_user(username, password)

#         elif choice == "3":
#             model = input("Введите модель велосипеда: ")
#             brand = input("Введите бренд велосипеда: ")
#             price = float(input("Введите цену велосипеда: "))
#             quantity = int(input("Введите количество: "))
#             velomagazin.add_bike(model, brand, price, quantity)

#         elif choice == "4":
#             name = input("Введите название запчасти: ")
#             category = input("Введите категорию: ")
#             price = float(input("Введите цену запчасти: "))
#             quantity = int(input("Введите количество: "))
#             velomagazin.add_bike_part(name, category, price, quantity)

#         elif choice == "5":
#             user_id = int(input("Введите ID пользователя: "))
#             items = []
#             while True:
#                 item_type = input("Введите тип товара (Велосипед/Запчасть) или 'done' для завершения: ").capitalize()
#                 if item_type == 'Done':
#                     break
#                 item_id = int(input("Введите ID товара: "))
#                 quantity = int(input("Введите количество: "))
#                 items.append((item_id, item_type, quantity))
#             velomagazin.place_order(user_id, items)

#         elif choice == "0":
#             velomagazin.close_connection()
#             print("До свидания!")
#             break

#         else:
#             print("Неверный выбор. Пожалуйста, выберите существующий пункт меню.")


    def manage_users(self):
        while True:
            print("\n--- Меню администратора ---")
            print("1. Просмотреть всех пользователей")
            print("2. Добавить пользователя")
            print("3. Изменить пользователя")
            print("4. Удалить пользователя")
            print("5. Поиск пользователя")
            print("0. Вернуться в главное меню")

            choice = input("Выберите действие: ")

            if choice == "1":
                print("Список пользователей:")
                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute("SELECT * FROM Пользователи")
                    users = cursor.fetchall()

                    for user_id, username, password in users:
                        print(f"{user_id}. {username}")

                input("Нажмите Enter для продолжения...")

            elif choice == "2":
                username = input("Введите имя пользователя: ")
                password = input("Введите пароль: ")

                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute("SELECT MAX(user_id) FROM Пользователи")
                    max_user_id = cursor.fetchone()[0]
                    user_id = max_user_id + 1 if max_user_id is not None else 1

                    # Вставка данных в таблицу Пользователи
                    cursor.execute("INSERT INTO Пользователи (user_id, username, password) VALUES (?, ?, ?)", (user_id, username, password))

                print("Пользователь успешно добавлен")

            elif choice == "3":
                user_id = input("Введите ID пользователя для изменения: ")
                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute("SELECT * FROM Пользователи WHERE user_id=?", (user_id,))
                    existing_user = cursor.fetchone()

                if existing_user:
                    new_username = input("Введите новое имя пользователя: ")
                    new_password = input("Введите новый пароль: ")

                    # Изменение данных пользователя
                    with self.conn:
                        cursor = self.conn.cursor()
                        cursor.execute("UPDATE Пользователи SET username=?, password=? WHERE user_id=?", (new_username, new_password, user_id))

                    print("Пользователь успешно изменен")
                else:
                    print("Пользователь с указанным ID не найден")

            elif choice == "4":
                user_id = input("Введите ID пользователя для удаления: ")

                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute("SELECT * FROM Пользователи WHERE user_id=?", (user_id,))
                    existing_user = cursor.fetchone()

                if existing_user:
                    # Удаление пользователя
                    with self.conn:
                        cursor = self.conn.cursor()
                        cursor.execute("DELETE FROM Пользователи WHERE user_id=?", (user_id,))

                    print("Пользователь успешно удален")
                else:
                    print("Пользователь с указанным ID не найден")

            elif choice == "5":
                search_attribute = input("Выберите атрибут для поиска (username, password): ")
                search_value = input(f"Введите значение {search_attribute} для поиска: ")

                # Поиск пользователя
                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute(f"SELECT * FROM Пользователи WHERE {search_attribute} LIKE ?", ('%' + search_value + '%',))
                    found_users = cursor.fetchall()

                if found_users:
                    print("Найденные пользователи:")
                    for user_id, username, password in found_users:
                        print(f"{user_id}. {username}")
                else:
                    print("Пользователи по указанным критериям не найдены")

            elif choice == "0":
                break

            else:
                print("Неверный выбор. Пожалуйста, выберите существующий пункт меню.")
    def save_to_database(self, data, table_name):
        # Общий метод для сохранения данных в базу данных
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' for _ in data.values())
        values = tuple(data.values())

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, values)
    def manage_staff(self):
            while True:
                print("\n--- Меню менеджера персонала ---")
                print("1. Просмотреть всех сотрудников")
                print("2. Добавить сотрудника")
                print("3. Изменить данные сотрудника")
                print("4. Удалить сотрудника")
                print("0. Вернуться в главное меню")

                choice = input("Выберите действие: ")

                if choice == "1":
                    self.view_all_staff()
                elif choice == "2":
                    self.add_staff()
                elif choice == "3":
                    self.modify_staff()
                elif choice == "4":
                    self.delete_staff()
                elif choice == "0":
                    break
                else:
                    print("Неверный выбор. Пожалуйста, выберите существующий пункт меню.")

    def view_all_staff(self):
            print("Список сотрудников:")
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM Сотрудники")
                staff = cursor.fetchall()

                for staff_id, staff_name in staff:
                    print(f"{staff_id}. {staff_name}")

            input("Нажмите Enter для продолжения...")

    def add_staff(self):
            staff_name = input("Введите имя сотрудника: ")

            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("SELECT MAX(staff_id) FROM Сотрудники")
                max_staff_id = cursor.fetchone()[0]
                staff_id = max_staff_id + 1 if max_staff_id is not None else 1

                # Вставка данных в таблицу Сотрудники
                cursor.execute("INSERT INTO Сотрудники (staff_id, staff_name) VALUES (?, ?)", (staff_id, staff_name))

            print("Сотрудник успешно добавлен")

    def modify_staff(self):
            staff_id = input("Введите ID сотрудника для изменения: ")
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM Сотрудники WHERE staff_id=?", (staff_id,))
                existing_staff = cursor.fetchone()

            if existing_staff:
                new_staff_name = input("Введите новое имя сотрудника: ")

                # Изменение данных сотрудника
                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute("UPDATE Сотрудники SET staff_name=? WHERE staff_id=?", (new_staff_name, staff_id))

                print("Сотрудник успешно изменен")
            else:
                print("Сотрудник с указанным ID не найден")
    def delete_staff(self):
            staff_id = input("Введите ID сотрудника для удаления: ")

            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM Сотрудники WHERE staff_id=?", (staff_id,))
                existing_staff = cursor.fetchone()

            if existing_staff:
                # Удаление сотрудника
                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute("DELETE FROM Сотрудники WHERE staff_id=?", (staff_id,))

                print("Сотрудник успешно удален")
            else:
                print("Сотрудник с указанным ID не найден")

    def manage_inventory(self):
        while True:
            print("\n--- Меню инвентаря ---")
            print("1. Просмотреть велосипеды")
            print("2. Просмотреть запчасти")
            print("3. Добавить велосипед")
            print("4. Добавить запчасть")
            print("5. Изменить товар")
            print("6. Удалить товар")
            print("7. Поиск товара")
            print("0. Вернуться в главное меню")

            choice = input("Выберите действие: ")

            if choice == "1":
                bikes = self.load_from_database('Велосипеды')
                print("Список велосипедов:")
                for bike_id, bike_data in bikes:
                    print(f"{bike_id}. {bike_data['brand']} {bike_data['model']} ({bike_data['price']} руб.) - В наличии: {bike_data['quantity']} шт.")
                input("Нажмите Enter для продолжения...")

            elif choice == "2":
                parts = self.load_from_database('Запчасти')
                print("Список запчастей:")
                for part_id, part_data in parts:
                    print(f"{part_id}. {part_data['name']} ({part_data['category']}) - В наличии: {part_data['quantity']} шт.")
                input("Нажмите Enter для продолжения...")

            elif choice == "3":
                model = input("Введите модель велосипеда: ")
                brand = input("Введите бренд велосипеда: ")
                price = float(input("Введите цену велосипеда: "))
                quantity = int(input("Введите количество: "))
                self.save_bike_to_database(model, brand, price, quantity)
                print("Велосипед успешно добавлен")

            elif choice == "4":
                name = input("Введите название запчасти: ")
                category = input("Введите категорию: ")
                price = float(input("Введите цену запчасти: "))
                quantity = int(input("Введите количество: "))
                self.save_part_to_database(name, category, price, quantity)
                print("Запчасть успешно добавлена")

            elif choice == "5":
                self.modify_item()

            elif choice == "6":
                self.delete_item()

            elif choice == "7":
                self.search_item()

            elif choice == "0":
                break

            else:
                print("Неверный выбор. Пожалуйста, выберите существующий пункт меню.")

    def save_bike_to_database(self, model, brand, price, quantity):
        # Метод для сохранения данных о велосипеде в базу данных
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Велосипеды (model, brand, price, quantity)
                VALUES (?, ?, ?, ?)
            """, (model, brand, price, quantity))

    def save_part_to_database(self, name, category, price, quantity):
        # Метод для сохранения данных о запчасти в базу данных
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Запчасти (name, category, price, quantity)
                VALUES (?, ?, ?, ?)
            """, (name, category, price, quantity))

        def modify_item(self):
            item_id = input("Введите ID товара для изменения: ")
            item_type = input("Введите тип товара (Велосипед/Запчасть): ").capitalize()
            
            if item_type == "Велосипед":
                bikes = self.load_from_database('Велосипеды')
                if any(item[0] == item_id for item in bikes):
                    self.modify_bike_in_database(item_id)
                else:
                    print("Велосипед с указанным ID не найден")
            elif item_type == "Запчасть":
                parts = self.load_from_database('Запчасти')
                if any(item[0] == item_id for item in parts):
                    self.modify_part_in_database(item_id)
                else:
                    print("Запчасть с указанным ID не найдена")
            else:
                print("Неверный тип товара. Допустимые значения: 'Велосипед' или 'Запчасть'.")

    def modify_bike_in_database(self, bike_id):
        # Метод для изменения данных о велосипеде в базе данных
        with self.conn:
            cursor = self.conn.cursor()
            new_model = input("Введите новую модель велосипеда: ")
            new_brand = input("Введите новый бренд велосипеда: ")
            new_price = float(input("Введите новую цену велосипеда: "))
            new_quantity = int(input("Введите новое количество: "))
            cursor.execute("""
                UPDATE Велосипеды
                SET model=?, brand=?, price=?, quantity=?
                WHERE bike_id=?
            """, (new_model, new_brand, new_price, new_quantity, bike_id))
        print("Велосипед успешно изменен")

    def modify_part_in_database(self, part_id):
        # Метод для изменения данных о запчасти в базе данных
        with self.conn:
            cursor = self.conn.cursor()
            new_name = input("Введите новое название запчасти: ")
            new_category = input("Введите новую категорию: ")
            new_price = float(input("Введите новую цену запчасти: "))
            new_quantity = int(input("Введите новое количество: "))
            cursor.execute("""
                UPDATE Запчасти
                SET name=?, category=?, price=?, quantity=?
                WHERE part_id=?
            """, (new_name, new_category, new_price, new_quantity, part_id))
        print("Запчасть успешно изменена")

    def delete_item(self):
        item_id = input("Введите ID товара для удаления: ")
        item_type = input("Введите тип товара (Велосипед/Запчасть): ").capitalize()

        if item_type == "Велосипед":
            bikes = self.load_from_database('Велосипеды')
            if any(item[0] == item_id for item in bikes):
                self.delete_bike_from_database(item_id)
                print("Велосипед успешно удален")
            else:
                print("Велосипед с указанным ID не найден")
        elif item_type == "Запчасть":
            parts = self.load_from_database('Запчасти')
            if any(item[0] == item_id for item in parts):
                self.delete_part_from_database(item_id)
                print("Запчасть успешно удалена")
            else:
                print("Запчасть с указанным ID не найдена")
        else:
            print("Неверный тип товара. Допустимые значения: 'Велосипед' или 'Запчасть'.")

    def delete_bike_from_database(self, bike_id):
        # Метод для удаления данных о велосипеде из базы данных
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Велосипеды WHERE bike_id=?", (bike_id,))

    def delete_part_from_database(self, part_id):
        # Метод для удаления данных о запчасти из базы данных
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Запчасти WHERE part_id=?", (part_id,))

    def search_item(self):
        search_attribute = input("Выберите атрибут для поиска (model, brand, name): ")
        search_value = input(f"Введите значение {search_attribute} для поиска: ")
        item_type = input("Введите тип товара (Велосипед/Запчасть): ").capitalize()

        if item_type == "Велосипед":
            found_items = self.search_bikes_in_database(search_attribute, search_value)
        elif item_type == "Запчасть":
            found_items = self.search_parts_in_database(search_attribute, search_value)
        else:
            print("Неверный тип товара. Допустимые значения: 'Велосипед' или 'Запчасть'.")
            return

        if found_items:
            print(f"Найденные товары ({item_type}):")
            for item_id, item_data in found_items:
                print(f"{item_id}. {item_data['brand']} {item_data['model']} ({item_data['name']}) - В наличии: {item_data['quantity']} шт.")
        else:
            print(f"Товары ({item_type}) по указанным критериям не найдены")

    def search_bikes_in_database(self, search_attribute, search_value):
        # Метод для поиска велосипедов в базе данных
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM Велосипеды WHERE {search_attribute}=?", (search_value,))
            return cursor.fetchall()

    def search_parts_in_database(self, search_attribute, search_value):
        # Метод для поиска запчастей в базе данных
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM Запчасти WHERE {search_attribute}=?", (search_value,))
            return cursor.fetchall()
        
    def cashier_operations(self):
        while True:
            print("\n--- Меню кассира ---")
            print("1. Просмотреть товары на складе")
            print("2. Оформить заказ")
            print("0. Вернуться в главное меню")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.view_inventory()

            elif choice == "2":
                self.process_order()

            elif choice == "0":
                break

            else:
                print("Неверный выбор. Пожалуйста, выберите существующий пункт меню.")

    def view_inventory(self):
            with self.conn:
                cursor = self.conn.cursor()

                # Получаем список велосипедов на складе
                cursor.execute("SELECT * FROM Велосипеды")
                bikes = cursor.fetchall()

                print("Список велосипедов на складе:")
                for bike_id, brand, model, price, quantity in bikes:
                    print(f"{bike_id}. {brand} {model} ({price} руб.) - В наличии: {quantity} шт.")

                # Получаем список запчастей на складе
                cursor.execute("SELECT * FROM Запчасти")
                parts = cursor.fetchall()

                print("\nСписок запчастей на складе:")
                for part_id, name, category, price, quantity in parts:
                    print(f"{part_id}. {name} ({category}) - В наличии: {quantity} шт.")

    def process_order(self):
        user_id = int(input("Введите ID пользователя: "))
        items = []

        while True:
            item_type = input("Введите тип товара (Велосипед/Запчасть) или 'done' для завершения: ").capitalize()
            if item_type == 'Done':
                break

            inventory_type = 'Велосипеды' if item_type == 'Велосипед' else 'Запчасти'
            self.view_inventory()

            item_id = int(input("Введите ID товара: "))
            quantity = int(input("Введите количество: "))

            if self.check_availability_in_database(item_id, item_type, quantity):
                items.append((item_id, item_type, quantity))
            else:
                print("Выбранного товара в указанном количестве нет на складе. Попробуйте снова.")

            # Оформление заказа с использованием данных из базы данных
            self.complete_order(user_id, items)
        # Можете вызвать соответствующий метод для сохранения заказа в базе данных

    def check_availability_in_database(self, item_id, item_type, quantity):
        # Метод для проверки наличия выбранного товара в указанном количестве в базе данных
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT quantity FROM {item_type} WHERE {item_type[:-1]}_id=?", (item_id,))
            available_quantity = cursor.fetchone()[0]
            return available_quantity >= quantity
            self.complete_order(user_id, items)

    def view_items(self, inventory_type):
        # Метод для просмотра товаров на складе из базы данных
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM {inventory_type}")
            items = cursor.fetchall()

        print(f"\n--- {inventory_type.capitalize()} на складе ---")
        for item_id, item_data in items:
            if inventory_type == 'Велосипеды':
                print(f"{item_id}. {item_data['brand']} {item_data['model']} - В наличии: {item_data['quantity']} шт.")
            elif inventory_type == 'Запчасти':
                print(f"{item_id}. {item_data['name']} - В наличии: {item_data['quantity']} шт.")

        def check_availability(self, item_id, item_type, quantity):
            inventory_type = 'Велосипеды' if item_type == 'Велосипед' else 'Запчасти'

            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(f"SELECT quantity FROM {inventory_type} WHERE {inventory_type[:-1]}_id=?", (item_id,))
                result = cursor.fetchone()

            if result and result[0] >= quantity:
                return True
            else:
                return False

    def complete_order(self, user_id, items):
        order_total = 0

        for item_id, item_type, quantity in items:
            inventory_type = 'Велосипеды' if item_type == 'Велосипед' else 'Запчасти'

            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(f"SELECT price, quantity FROM {inventory_type} WHERE {inventory_type[:-1]}_id=?", (item_id,))
                result = cursor.fetchone()

            if result:
                item_price, available_quantity = result
                item_total = item_price * quantity
                order_total += item_total

                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute(f"UPDATE {inventory_type} SET quantity=? WHERE {inventory_type[:-1]}_id=?", (available_quantity - quantity, item_id))

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Заказы (user_id, order_date) VALUES (?, ?)", (user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            order_id = cursor.lastrowid

            for item_id, item_type, quantity in items:
                inventory_type = 'Велосипеды' if item_type == 'Велосипед' else 'Запчасти'
                cursor.execute("INSERT INTO ДеталиЗаказа (order_id, item_id, item_type, quantity) VALUES (?, ?, ?, ?)", (order_id, item_id, item_type, quantity))

        print("Заказ успешно оформлен")
        print(f"Общая сумма заказа: {order_total} руб.")
    def accountant_operations(self):
        while True:
            print("\n--- Меню бухгалтера ---")
            print("1. Просмотреть все транзакции")
            print("2. Добавить транзакцию")
            print("3. Изменить транзакцию")
            print("4. Удалить транзакцию")
            print("5. Поиск транзакции")
            print("0. Вернуться в главное меню")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.view_transactions()

            elif choice == "2":
                self.add_transaction()

            elif choice == "3":
                self.update_transaction()

            elif choice == "4":
                self.delete_transaction()

            elif choice == "5":
                self.search_transaction()

            elif choice == "0":
                break

            else:
                print("Неверный выбор. Пожалуйста, выберите существующий пункт меню.")

    def view_transactions(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Транзакции")
            transactions = cursor.fetchall()

        print("\n--- Все транзакции ---")
        for transaction_id, user_id, amount, transaction_date in transactions:
            print(f"{transaction_id}. Пользователь {user_id}, Сумма: {amount} руб., Дата: {transaction_date}")

    def add_transaction(self):
        user_id = int(input("Введите ID пользователя: "))
        amount = float(input("Введите сумму транзакции: "))

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Транзакции (user_id, amount, transaction_date) VALUES (?, ?, ?)",
                        (user_id, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            print("Транзакция успешно добавлена")

    def update_transaction(self):
        transaction_id = int(input("Введите ID транзакции для изменения: "))
        new_amount = float(input("Введите новую сумму транзакции: "))

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE Транзакции SET amount=? WHERE transaction_id=?", (new_amount, transaction_id))
            print("Транзакция успешно изменена")

    def delete_transaction(self):
        transaction_id = int(input("Введите ID транзакции для удаления: "))

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Транзакции WHERE transaction_id=?", (transaction_id,))
            print("Транзакция успешно удалена")

    def search_transaction(self):
        search_user_id = int(input("Введите ID пользователя для поиска транзакции: "))

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Транзакции WHERE user_id=?", (search_user_id,))
            transactions = cursor.fetchall()

        if transactions:
            print(f"\n--- Транзакции пользователя {search_user_id} ---")
            for transaction_id, user_id, amount, transaction_date in transactions:
                print(f"{transaction_id}. Сумма: {amount} руб., Дата: {transaction_date}")
        else:
            print(f"Транзакции пользователя {search_user_id} не найдены")
    def user_menu(self):
        while True:
            print("\n--- Меню пользователя ---")
            print("1. Просмотреть велосипеды в наличии")
            print("2. Просмотреть запчасти в наличии")
            print("3. Просмотреть свои заказы")
            print("4. Поиск товара")
            print("0. Вернуться в главное меню")

            choice = input("Выберите действие: ")

            if choice == "1":
                self.view_bikes()
            elif choice == "2":
                self.view_parts()
            elif choice == "3":
                self.view_orders()
            elif choice == "4":
                self.search_items()
            elif choice == "0":
                break
            else:
                print("Некорректный выбор. Пожалуйста, введите корректный номер действия.")

    def view_bikes(self):
        print("\n--- Просмотр велосипедов в наличии ---")
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Велосипеды WHERE quantity > 0")
            available_bikes = cursor.fetchall()

            if available_bikes:
                print("Велосипеды в наличии:")
                for bike_id, model, brand, price, quantity in available_bikes:
                    print(f"{bike_id}. Модель: {model}, Бренд: {brand}, Цена: {price}, Количество: {quantity}")
            else:
                print("Велосипедов в наличии нет.")

        input("Нажмите Enter для продолжения...")
        pass

    def view_parts(self):
        print("\n--- Просмотр запчастей в наличии ---")
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Запчасти WHERE quantity > 0")
            available_parts = cursor.fetchall()

            if available_parts:
                print("Запчасти в наличии:")
                for part_id, name, category, price, quantity in available_parts:
                    print(f"{part_id}. Название: {name}, Категория: {category}, Цена: {price}, Количество: {quantity}")
            else:
                print("Запчастей в наличии нет.")

        input("Нажмите Enter для продолжения...")
        pass

    def view_orders(self):
        if not self.current_user_id:
            print("Пользователь не авторизован.")
            return

        print("\n--- Просмотр своих заказов ---")
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Заказы WHERE user_id=?", (self.current_user_id,))
            user_orders = cursor.fetchall()

            if user_orders:
                print("Ваши заказы:")
                for order_id, _, order_date in user_orders:
                    print(f"{order_id}. Дата заказа: {order_date}")
            else:
                print("У вас пока нет заказов.")

        input("Нажмите Enter для продолжения...")


    def search_items(self):
        search_term = input("Введите ключевое слово для поиска товара: ")

        print("\n--- Поиск товара ---")
        with self.conn:
            cursor = self.conn.cursor()

            # Поиск велосипедов
            cursor.execute("SELECT * FROM Велосипеды WHERE model LIKE ? OR brand LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
            bikes = cursor.fetchall()

            if bikes:
                print("Найденные велосипеды:")
                for bike_id, model, brand, price, quantity in bikes:
                    print(f"{bike_id}. Модель: {model}, Бренд: {brand}, Цена: {price}, Количество: {quantity}")
            else:
                print("Велосипеды не найдены.")

            # Поиск запчастей
            cursor.execute("SELECT * FROM Запчасти WHERE name LIKE ? OR category LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
            parts = cursor.fetchall()

            if parts:
                print("Найденные запчасти:")
                for part_id, name, category, price, quantity in parts:
                    print(f"{part_id}. Название: {name}, Категория: {category}, Цена: {price}, Количество: {quantity}")
            else:
                print("Запчасти не найдены.")

        input("Нажмите Enter для продолжения...")
        pass

if __name__ == "__main__":
    velomagazin = velomagazin()
    while True:
        print("\nВыберите роль:")
        print("1. Администратор")
        print("2. Менеджер персонала")
        print("3. Складской менеджер")
        print("4. Кассир")
        print("5. Бухгалтер")
        print("6. Клиент")  
        print("0. Выход")

        role_choice = input("Введите номер роли: ")

        if role_choice == "1":
            velomagazin.manage_users()
        elif role_choice == "2":
            velomagazin.manage_staff()
        elif role_choice == "3":
            velomagazin.manage_inventory()
        elif role_choice == "4":
            velomagazin.cashier_operations()
        elif role_choice == "5":
            velomagazin.accountant_operations()
        elif role_choice == "6":
            velomagazin.user_menu()  
        elif role_choice == "0":
            velomagazin.close_connection()
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Пожалуйста, введите корректный номер роли.")
