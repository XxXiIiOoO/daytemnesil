import sqlite3
import hashlib
from datetime import datetime

class Веломагазин:
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
            print("Авторизация успешна")
        else:
            print("Неверное имя пользователя или пароль")

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
if __name__ == "__main__":
    веломагазин = Веломагазин()

    while True:
        print("\n--- Меню веломагазина ---")
        print("1. Регистрация пользователя")
        print("2. Авторизация")
        print("3. Добавить велосипед в инвентарь")
        print("4. Добавить запчасть в инвентарь")
        print("5. Оформить заказ")
        print("0. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            веломагазин.register_user(username, password)

        elif choice == "2":
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            веломагазин.login_user(username, password)

        elif choice == "3":
            model = input("Введите модель велосипеда: ")
            brand = input("Введите бренд велосипеда: ")
            price = float(input("Введите цену велосипеда: "))
            quantity = int(input("Введите количество: "))
            веломагазин.add_bike(model, brand, price, quantity)

        elif choice == "4":
            name = input("Введите название запчасти: ")
            category = input("Введите категорию: ")
            price = float(input("Введите цену запчасти: "))
            quantity = int(input("Введите количество: "))
            веломагазин.add_bike_part(name, category, price, quantity)

        elif choice == "5":
            user_id = int(input("Введите ID пользователя: "))
            items = []
            while True:
                item_type = input("Введите тип товара (Велосипед/Запчасть) или 'done' для завершения: ").capitalize()
                if item_type == 'Done':
                    break
                item_id = int(input("Введите ID товара: "))
                quantity = int(input("Введите количество: "))
                items.append((item_id, item_type, quantity))
            веломагазин.place_order(user_id, items)

        elif choice == "0":
            веломагазин.close_connection()
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите существующий пункт меню.")
    def save_to_json(self, data, filename):
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    def load_from_json(self, filename):
        try:
            with open(filename, 'r') as json_file:
                data = json.load(json_file)
                return data
        except FileNotFoundError:
            return {}

    def manage_users(self):
        users = self.load_from_json('users.json')
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
                for user_id, user_data in users.items():
                    print(f"{user_id}. {user_data['username']}")
                input("Нажмите Enter для продолжения...")

            elif choice == "2":
                username = input("Введите имя пользователя: ")
                password = input("Введите пароль: ")
                user_id = max(map(int, users.keys()), default=0) + 1
                users[user_id] = {'username': username, 'password': password}
                self.save_to_json(users, 'users.json')
                print("Пользователь успешно добавлен")

            elif choice == "3":
                user_id = input("Введите ID пользователя для изменения: ")
                if user_id in users:
                    username = input("Введите новое имя пользователя: ")
                    password = input("Введите новый пароль: ")
                    users[user_id] = {'username': username, 'password': password}
                    self.save_to_json(users, 'users.json')
                    print("Пользователь успешно изменен")
                else:
                    print("Пользователь с указанным ID не найден")

            elif choice == "4":
                user_id = input("Введите ID пользователя для удаления: ")
                if user_id in users:
                    del users[user_id]
                    self.save_to_json(users, 'users.json')
                    print("Пользователь успешно удален")
                else:
                    print("Пользователь с указанным ID не найден")

            elif choice == "5":
                search_attribute = input("Выберите атрибут для поиска (username, password): ")
                search_value = input(f"Введите значение {search_attribute} для поиска: ")
                found_users = {user_id: user_data for user_id, user_data in users.items() if user_data[search_attribute] == search_value}
                if found_users:
                    print("Найденные пользователи:")
                    for user_id, user_data in found_users.items():
                        print(f"{user_id}. {user_data['username']}")
                else:
                    print("Пользователи по указанным критериям не найдены")

            elif choice == "0":
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите существующий пункт меню.")

    def manage_staff(self):
        staff = self.load_from_json('staff.json')
        while True:
            print("\n--- Меню менеджера персонала ---")
            print("1. Просмотреть всех сотрудников")
            print("2. Добавить сотрудника")
            print("3. Изменить сотрудника")
            print("4. Удалить сотрудника")
            print("5. Поиск сотрудника")
            print("0. Вернуться в главное меню")

            choice = input("Выберите действие: ")

            if choice == "1":
                print("Список сотрудников:")
                for staff_id, staff_data in staff.items():
                    print(f"{staff_id}. {staff_data['name']}")
                input("Нажмите Enter для продолжения...")

            elif choice == "2":
                name = input("Введите имя сотрудника: ")
                position = input("Введите должность сотрудника: ")
                staff_id = max(map(int, staff.keys()), default=0) + 1
                staff[staff_id] = {'name': name, 'position': position, 'user_id': None}
                self.save_to_json(staff, 'staff.json')
                print("Сотрудник успешно добавлен")

            elif choice == "3":
                staff_id = input("Введите ID сотрудника для изменения: ")
                if staff_id in staff:
                    name = input("Введите новое имя сотрудника: ")
                    position = input("Введите новую должность сотрудника: ")
                    staff[staff_id] = {'name': name, 'position': position, 'user_id': staff[staff_id]['user_id']}
                    self.save_to_json(staff, 'staff.json')
                    print("Сотрудник успешно изменен")
                else:
                    print("Сотрудник с указанным ID не найден")

            elif choice == "4":
                staff_id = input("Введите ID сотрудника для удаления: ")
                if staff_id in staff:
                    del staff[staff_id]
                    self.save_to_json(staff, 'staff.json')
                    print("Сотрудник успешно удален")
                else:
                    print("Сотрудник с указанным ID не найден")

            elif choice == "5":
                search_attribute = input("Выберите атрибут для поиска (name, position): ")
                search_value = input(f"Введите значение {search_attribute} для поиска: ")
                found_staff = {staff_id: staff_data for staff_id, staff_data in staff.items() if staff_data[search_attribute] == search_value}
                if found_staff:
                    print("Найденные сотрудники:")
                    for staff_id, staff_data in found_staff.items():
                        print(f"{staff_id}. {staff_data['name']} ({staff_data['position']})")
                else:
                    print("Сотрудники по указанным критериям не найдены")

            elif choice == "0":
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите существующий пункт меню.")
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
                bikes = self.load_from_json('bikes.json')
                print("Список велосипедов:")
                for bike_id, bike_data in bikes.items():
                    print(f"{bike_id}. {bike_data['brand']} {bike_data['model']} ({bike_data['price']} руб.) - В наличии: {bike_data['quantity']} шт.")
                input("Нажмите Enter для продолжения...")

            elif choice == "2":
                parts = self.load_from_json('parts.json')
                print("Список запчастей:")
                for part_id, part_data in parts.items():
                    print(f"{part_id}. {part_data['name']} ({part_data['category']}) - В наличии: {part_data['quantity']} шт.")
                input("Нажмите Enter для продолжения...")

            elif choice == "3":
                model = input("Введите модель велосипеда: ")
                brand = input("Введите бренд велосипеда: ")
                price = float(input("Введите цену велосипеда: "))
                quantity = int(input("Введите количество: "))
                bikes = self.load_from_json('bikes.json')
                bike_id = max(map(int, bikes.keys()), default=0) + 1
                bikes[bike_id] = {'model': model, 'brand': brand, 'price': price, 'quantity': quantity}
                self.save_to_json(bikes, 'bikes.json')
                print("Велосипед успешно добавлен")

            elif choice == "4":
                name = input("Введите название запчасти: ")
                category = input("Введите категорию: ")
                price = float(input("Введите цену запчасти: "))
                quantity = int(input("Введите количество: "))
                parts = self.load_from_json('parts.json')
                part_id = max(map(int, parts.keys()), default=0) + 1
                parts[part_id] = {'name': name, 'category': category, 'price': price, 'quantity': quantity}
                self.save_to_json(parts, 'parts.json')
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

    def modify_item(self):
        item_id = input("Введите ID товара для изменения: ")
        item_type = input("Введите тип товара (Велосипед/Запчасть): ").capitalize()
        if item_type == "Велосипед":
            bikes = self.load_from_json('bikes.json')
            if item_id in bikes:
                self.modify_bike(bikes, item_id)
            else:
                print("Велосипед с указанным ID не найден")
        elif item_type == "Запчасть":
            parts = self.load_from_json('parts.json')
            if item_id in parts:
                self.modify_part(parts, item_id)
            else:
                print("Запчасть с указанным ID не найдена")
        else:
            print("Неверный тип товара. Допустимые значения: 'Велосипед' или 'Запчасть'.")

    def modify_bike(self, bikes, bike_id):
        model = input("Введите новую модель велосипеда: ")
        brand = input("Введите новый бренд велосипеда: ")
        price = float(input("Введите новую цену велосипеда: "))
        quantity = int(input("Введите новое количество: "))
        bikes[bike_id] = {'model': model, 'brand': brand, 'price': price, 'quantity': quantity}
        self.save_to_json(bikes, 'bikes.json')
        print("Велосипед успешно изменен")

    def modify_part(self, parts, part_id):
        name = input("Введите новое название запчасти: ")
        category = input("Введите новую категорию: ")
        price = float(input("Введите новую цену запчасти: "))
        quantity = int(input("Введите новое количество: "))
        parts[part_id] = {'name': name, 'category': category, 'price': price, 'quantity': quantity}
        self.save_to_json(parts, 'parts.json')
        print("Запчасть успешно изменена")

    def delete_item(self):
        item_id = input("Введите ID товара для удаления: ")
        item_type = input("Введите тип товара (Велосипед/Запчасть): ").capitalize()
        if item_type == "Велосипед":
            bikes = self.load_from_json('bikes.json')
            if item_id in bikes:
                del bikes[item_id]
                self.save_to_json(bikes, 'bikes.json')
                print("Велосипед успешно удален")
            else:
                print("Велосипед с указанным ID не найден")
        elif item_type == "Запчасть":
            parts = self.load_from_json('parts.json')
            if item_id in parts:
                del parts[item_id]
                self.save_to_json(parts, 'parts.json')
                print("Запчасть успешно удалена")
            else:
                print("Запчасть с указанным ID не найдена")
        else:
            print("Неверный тип товара. Допустимые значения: 'Велосипед' или 'Запчасть'.")

    def search_item(self):
        search_attribute = input("Выберите атрибут для поиска (model, brand, name): ")
        search_value = input(f"Введите значение {search_attribute} для поиска: ")
        item_type = input("Введите тип товара (Велосипед/Запчасть): ").capitalize()
        if item_type == "Велосипед":
            bikes = self.load_from_json('bikes.json')
            found_items = {item_id: item_data for item_id, item_data in bikes.items() if item_data[search_attribute] == search_value}
        elif item_type == "Запчасть":
            parts = self.load_from_json('parts.json')
            found_items = {item_id: item_data for item_id, item_data in parts.items() if item_data[search_attribute] == search_value}
        else:
            print("Неверный тип товара. Допустимые значения: 'Велосипед' или 'Запчасть'.")
            return

        if found_items:
            print(f"Найденные товары ({item_type}):")
            for item_id, item_data in found_items.items():
                print(f"{item_id}. {item_data['brand']} {item_data['model']} ({item_data['name']}) - В наличии: {item_data['quantity']} шт.")
        else:
            print(f"Товары ({item_type}) по указанным критериям не найдены")
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
        bikes = self.load_from_json('bikes.json')
        parts = self.load_from_json('parts.json')

        print("\n--- Велосипеды на складе ---")
        for bike_id, bike_data in bikes.items():
            print(f"{bike_id}. {bike_data['brand']} {bike_data['model']} ({bike_data['price']} руб.) - В наличии: {bike_data['quantity']} шт.")

        print("\n--- Запчасти на складе ---")
        for part_id, part_data in parts.items():
            print(f"{part_id}. {part_data['name']} ({part_data['category']}) - В наличии: {part_data['quantity']} шт.")

    def process_order(self):
        user_id = int(input("Введите ID пользователя: "))
        items = []
        
        while True:
            item_type = input("Введите тип товара (Велосипед/Запчасть) или 'done' для завершения: ").capitalize()
            if item_type == 'Done':
                break
            
            inventory_type = 'bikes' if item_type == 'Велосипед' else 'parts'
            self.view_items(inventory_type)

            item_id = int(input("Введите ID товара: "))
            quantity = int(input("Введите количество: "))

            if self.check_availability(item_id, item_type, quantity):
                items.append((item_id, item_type, quantity))
            else:
                print("Выбранного товара в указанном количестве нет на складе. Попробуйте снова.")

        self.complete_order(user_id, items)

    def view_items(self, inventory_type):
        items = self.load_from_json(f'{inventory_type}.json')
        print(f"\n--- {inventory_type.capitalize()} на складе ---")
        for item_id, item_data in items.items():
            print(f"{item_id}. {item_data['brand']} {item_data['model'] if inventory_type == 'bikes' else item_data['name']} - В наличии: {item_data['quantity']} шт.")

    def check_availability(self, item_id, item_type, quantity):
        inventory_type = 'bikes' if item_type == 'Велосипед' else 'parts'
        items = self.load_from_json(f'{inventory_type}.json')

        if item_id in items and items[item_id]['quantity'] >= quantity:
            return True
        else:
            return False

    def complete_order(self, user_id, items):
        bikes = self.load_from_json('bikes.json')
        parts = self.load_from_json('parts.json')

        order_total = 0

        for item_id, item_type, quantity in items:
            inventory_type = 'bikes' if item_type == 'Велосипед' else 'parts'
            item_data = locals()[inventory_type][item_id]

            item_total = item_data['price'] * quantity
            order_total += item_total

            locals()[inventory_type][item_id]['quantity'] -= quantity

        order_record = {'user_id': user_id, 'items': items, 'total': order_total}
        orders = self.load_from_json('orders.json')
        order_id = max(map(int, orders.keys()), default=0) + 1
        orders[order_id] = order_record
        self.save_to_json(orders, 'orders.json')

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
        transactions = self.load_from_json('transactions.json')

        print("\n--- Все транзакции ---")
        for transaction_id, transaction_data in transactions.items():
            print(f"{transaction_id}. Дата: {transaction_data['date']}, Сумма: {transaction_data['amount']} руб., Описание: {transaction_data['description']}")

        input("Нажмите Enter для продолжения...")

    def add_transaction(self):
        date = input("Введите дату транзакции (гггг-мм-дд): ")
        amount = float(input("Введите сумму транзакции: "))
        description = input("Введите описание транзакции: ")

        transactions = self.load_from_json('transactions.json')
        transaction_id = max(map(int, transactions.keys()), default=0) + 1
        transactions[transaction_id] = {'date': date, 'amount': amount, 'description': description}
        self.save_to_json(transactions, 'transactions.json')
        print("Транзакция успешно добавлена")

    def update_transaction(self):
        transaction_id = input("Введите ID транзакции для изменения: ")
        transactions = self.load_from_json('transactions.json')

        if transaction_id in transactions:
            date = input("Введите новую дату транзакции (гггг-мм-дд): ")
            amount = float(input("Введите новую сумму транзакции: "))
            description = input("Введите новое описание транзакции: ")

            transactions[transaction_id] = {'date': date, 'amount': amount, 'description': description}
            self.save_to_json(transactions, 'transactions.json')
            print("Транзакция успешно изменена")
        else:
            print("Транзакция с указанным ID не найдена")

    def delete_transaction(self):
        transaction_id = input("Введите ID транзакции для удаления: ")
        transactions = self.load_from_json('transactions.json')

        if transaction_id in transactions:
            del transactions[transaction_id]
            self.save_to_json(transactions, 'transactions.json')
            print("Транзакция успешно удалена")
        else:
            print("Транзакция с указанным ID не найдена")

    def search_transaction(self):
        search_attribute = input("Выберите атрибут для поиска (date, amount, description): ")
        search_value = input(f"Введите значение {search_attribute} для поиска: ")
        transactions = self.load_from_json('transactions.json')

        found_transactions = {transaction_id: transaction_data for transaction_id, transaction_data in transactions.items() if str(transaction_data[search_attribute]) == search_value}
        if found_transactions:
            print("Найденные транзакции:")
            for transaction_id, transaction_data in found_transactions.items():
                print(f"{transaction_id}. Дата: {transaction_data['date']}, Сумма: {transaction_data['amount']} руб., Описание: {transaction_data['description']}")
        else:
            print("Транзакции по указанным критериям не найдены")

