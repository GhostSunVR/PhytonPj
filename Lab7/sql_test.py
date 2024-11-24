import psycopg2
from prettytable import PrettyTable

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="db",
        user="user",
        password="password"
    )

def execute_queries():
    connection = get_db_connection()
    cursor = connection.cursor()

    # 1. Відобразити всі критичні помилки, відсортовані за кодом помилки
    cursor.execute("""
        SELECT error_id, description, date_received FROM Errors
        WHERE severity_level = 'Critical'
        ORDER BY error_id;
    """)
    table = PrettyTable(["Код помилки", "Опис", "Дата надходження"])
    for row in cursor.fetchall():
        table.add_row(row)
    print("Критичні помилки:\n", table)

    # 2. Порахувати кількість помилок кожного рівня
    cursor.execute("""
        SELECT severity_level, COUNT(*) AS error_count FROM Errors
        GROUP BY severity_level;
    """)
    table = PrettyTable(["Рівень помилки", "Кількість"])
    for row in cursor.fetchall():
        table.add_row(row)
    print("\nКількість помилок кожного рівня:\n", table)

    # 3. Порахувати вартість роботи програміста при виправленні кожної помилки
    cursor.execute("""
        SELECT f.fix_id, f.error_id, p.last_name, p.first_name, 
               (f.duration_days * f.daily_rate) AS total_cost
        FROM Fixes f
        JOIN Programmers p ON f.programmer_id = p.programmer_id;
    """)
    table = PrettyTable(["Код виправлення", "Код помилки", "Прізвище", "Ім'я", "Загальна вартість"])
    for row in cursor.fetchall():
        table.add_row(row)
    print("\nВартість роботи програміста при виправленні кожної помилки:\n", table)

    # 4. Відобразити всі помилки, які надійшли із заданого джерела
    source = input("Введіть джерело помилки (User або Tester): ")
    cursor.execute("""
        SELECT error_id, description, date_received FROM Errors
        WHERE source = %s;
    """, (source,))
    table = PrettyTable(["Код помилки", "Опис", "Дата надходження"])
    for row in cursor.fetchall():
        table.add_row(row)
    print(f"\nПомилки, які надійшли від {source}:\n", table)

    # 5. Порахувати кількість помилок, які надійшли від користувачів та тестувальників
    cursor.execute("""
        SELECT source, COUNT(*) AS error_count FROM Errors
        GROUP BY source;
    """)
    table = PrettyTable(["Джерело", "Кількість"])
    for row in cursor.fetchall():
        table.add_row(row)
    print("\nКількість помилок за джерелом:\n", table)

    # 6. Порахувати кількість критичних, важливих, незначних помилок, виправлених кожним програмістом
    cursor.execute("""
        SELECT p.last_name, p.first_name,
               SUM(CASE WHEN e.severity_level = 'Critical' THEN 1 ELSE 0 END) AS critical_errors,
               SUM(CASE WHEN e.severity_level = 'Important' THEN 1 ELSE 0 END) AS important_errors,
               SUM(CASE WHEN e.severity_level = 'Minor' THEN 1 ELSE 0 END) AS minor_errors
        FROM Fixes f
        JOIN Programmers p ON f.programmer_id = p.programmer_id
        JOIN Errors e ON f.error_id = e.error_id
        GROUP BY p.last_name, p.first_name;
    """)
    table = PrettyTable(["Прізвище", "Ім'я", "Критичні", "Важливі", "Незначні"])
    for row in cursor.fetchall():
        table.add_row(row)
    print("\nКількість виправлених помилок за рівнем кожним програмістом:\n", table)

    # Закриваємо з'єднання
    cursor.close()
    connection.close()

if __name__ == "__main__":
    execute_queries()
