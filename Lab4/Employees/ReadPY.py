import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os


def calculate_age(birth_date):
    """Обчислює вік на основі дати народження"""
    today = datetime.now()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def categorize_by_age(df):
    """Додає до DataFrame вікову категорію"""
    df['Вікова категорія'] = pd.cut(df['Вік'],
                                    bins=[0, 18, 45, 70, 100],
                                    labels=['younger_18', '18-45', '45-70', 'older_70'],
                                    right=False)
    return df


def plot_pie_chart(labels, sizes, title):
    """Будує кругову діаграму"""
    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140,
            colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
    plt.title(title)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()


def plot_bar_chart(x, y, title, xlabel, ylabel):
    """Будує стовпчасту діаграму"""
    plt.figure(figsize=(8, 6))
    plt.bar(x, y, color=['#ff9999', '#66b3ff'])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def main():
    try:
        # Перевірка наявності CSV файлу
        csv_file = 'employees.csv'
        if not os.path.exists(csv_file):
            print("Помилка: CSV файл не знайдено.")
            return

        # Читання CSV файлу
        df = pd.read_csv(csv_file)

        # Перетворення дати народження у формат datetime і обчислення віку
        df['Дата народження'] = pd.to_datetime(df['Дата народження'], format='%d-%m-%Y')
        df['Вік'] = df['Дата народження'].apply(calculate_age)

        # Додавання вікової категорії
        df = categorize_by_age(df)

        # Підрахунок кількості чоловіків і жінок
        gender_count = df['Стать'].value_counts()
        print("Кількість чоловіків:", gender_count.get('Чоловіча', 0))
        print("Кількість жінок:", gender_count.get('Жіноча', 0))

        # Побудова діаграми за статтю
        plot_pie_chart(gender_count.index, gender_count.values, "Розподіл за статтю")

        # Підрахунок кількості співробітників у вікових категоріях
        age_category_count = df['Вікова категорія'].value_counts()
        print("Кількість у вікових категоріях:")
        print(age_category_count)

        # Побудова діаграми за віковими категоріями
        plot_bar_chart(age_category_count.index, age_category_count.values, "Розподіл за віковими категоріями",
                       "Вікові категорії", "Кількість співробітників")

        # Підрахунок кількості чоловіків і жінок у кожній віковій категорії
        gender_age_count = df.groupby(['Вікова категорія', 'Стать']).size().unstack(fill_value=0)
        print("Кількість чоловіків і жінок у кожній віковій категорії:")
        print(gender_age_count)

        # Побудова діаграм за статтю для кожної вікової категорії
        for category in gender_age_count.index:
            plot_bar_chart(gender_age_count.columns, gender_age_count.loc[category],
                           f"Розподіл за статтю у категорії {category}", "Стать", "Кількість співробітників")

        print("Ok")

    except FileNotFoundError:
        print("Помилка: не вдалося знайти або відкрити CSV файл.")
    except PermissionError:
        print("Помилка: неможливо відкрити або створити файл.")
    except Exception as e:
        print(f"Сталася непередбачена помилка: {e}")


if __name__ == "__main__":
    main()
