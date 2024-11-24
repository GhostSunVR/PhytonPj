from faker import Faker
import random
import psycopg2

fake = Faker("uk_UA")

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="db",
        user="user",
        password="password"
    )


def populate_data():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Заповнення таблиці Errors (Помилки)
    for _ in range(20):
        description = fake.sentence()
        date_received = fake.date_this_year()
        severity_level = random.choice(["Critical", "Important", "Minor"])
        functionality_category = random.choice(["Interface", "Data", "Algorithm", "Other", "Unknown"])
        source = random.choice(["User", "Tester"])
        cursor.execute("""
            INSERT INTO Errors (description, date_received, severity_level, functionality_category, source)
            VALUES (%s, %s, %s, %s, %s)
        """, (description, date_received, severity_level, functionality_category, source))

    # Заповнення таблиці Programmers (Програмісти)
    for _ in range(4):
        last_name = fake.last_name()
        first_name = fake.first_name()
        phone_number = f"+38067{random.randint(1000000, 9999999)}"  # телефон у форматі +38067XXXXXXX
        cursor.execute("""
            INSERT INTO Programmers (last_name, first_name, phone_number)
            VALUES (%s, %s, %s)
        """, (last_name, first_name, phone_number))

    # Заповнення таблиці Fixes (Виправлення помилок)
    for _ in range(20):
        error_id = random.randint(1, 20)  # посилання на існуючі помилки
        programmer_id = random.randint(1, 4)  # посилання на існуючих програмістів
        start_date = fake.date_this_year()
        duration_days = random.choice([1, 2, 3])  # тривалість виправлення (1, 2 або 3 дні)
        daily_rate = random.randint(300, 1000)  # вартість роботи за день
        cursor.execute("""
            INSERT INTO Fixes (error_id, programmer_id, start_date, duration_days, daily_rate)
            VALUES (%s, %s, %s, %s, %s)
        """, (error_id, programmer_id, start_date, duration_days, daily_rate))

    # Застосування змін до бази даних
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    populate_data()
