import pandas as pd
from datetime import datetime
import os


def calculate_age(birth_date):
    """Обчислює вік на основі дати народження"""
    today = datetime.now()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def categorize_by_age(df):
    """Розподіляє працівників по вікових категоріях"""
    younger_18 = df[df['Вік'] < 18]
    between_18_45 = df[(df['Вік'] >= 18) & (df['Вік'] <= 45)]
    between_45_70 = df[(df['Вік'] > 45) & (df['Вік'] <= 70)]
    older_70 = df[df['Вік'] > 70]

    return younger_18, between_18_45, between_45_70, older_70


def main():
    try:
        # Перевіряємо наявність CSV файлу
        csv_file = 'employees.csv'
        if not os.path.exists(csv_file):
            print("Помилка: CSV файл не знайдено.")
            return

        # Читання CSV файлу
        df = pd.read_csv(csv_file)

        # Перетворюємо дату народження у формат datetime і додаємо стовпець з віком
        df['Дата народження'] = pd.to_datetime(df['Дата народження'], format='%d-%m-%Y')
        df['Вік'] = df['Дата народження'].apply(calculate_age)

        # Створення Excel файлу з 5 аркушами
        xlsx_file = 'employees.xlsx'

        # Розподіл по віковим групам
        younger_18, between_18_45, between_45_70, older_70 = categorize_by_age(df)

        # Збереження у Excel файл
        with pd.ExcelWriter(xlsx_file, engine='openpyxl') as writer:
            df[['Прізвище', 'Ім’я', 'По батькові', 'Дата народження', 'Вік']].to_excel(writer, sheet_name='all',
                                                                                       index_label='№')
            younger_18[['Прізвище', 'Ім’я', 'По батькові', 'Дата народження', 'Вік']].to_excel(writer,
                                                                                               sheet_name='younger_18',
                                                                                               index_label='№')
            between_18_45[['Прізвище', 'Ім’я', 'По батькові', 'Дата народження', 'Вік']].to_excel(writer,
                                                                                                  sheet_name='18-45',
                                                                                                  index_label='№')
            between_45_70[['Прізвище', 'Ім’я', 'По батькові', 'Дата народження', 'Вік']].to_excel(writer,
                                                                                                  sheet_name='45-70',
                                                                                                  index_label='№')
            older_70[['Прізвище', 'Ім’я', 'По батькові', 'Дата народження', 'Вік']].to_excel(writer,
                                                                                             sheet_name='older_70',
                                                                                             index_label='№')

        print("Ok")

    except FileNotFoundError:
        print("Помилка: не вдалося знайти або відкрити CSV файл.")
    except PermissionError:
        print("Помилка: неможливо створити XLSX файл.")
    except Exception as e:
        print(f"Сталася непередбачена помилка: {e}")


if __name__ == "__main__":
    main()
