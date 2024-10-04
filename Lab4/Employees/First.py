import csv
from faker import Faker
import random

# Ініціалізація Faker з українською локалізацією
fake = Faker('uk_UA')

# Кількість записів
num_records = 2000
male_ratio = 0.6
female_ratio = 0.4


# Функція для генерування даних про працівників
def generate_employee(gender):
    if gender == 'M':  # Чоловік
        first_name = fake.first_name_male()
        middle_name = fake.middle_name_male()
    else:  # Жінка
        first_name = fake.first_name_female()
        middle_name = fake.middle_name_female()

    return {
        'Прізвище': fake.last_name(),
        'Ім’я': first_name,
        'По батькові': middle_name,
        'Стать': 'Чоловіча' if gender == 'M' else 'Жіноча',
        'Дата народження': fake.date_of_birth(minimum_age=16, maximum_age=85).strftime('%d-%m-%Y'),
        'Посада': fake.job(),
        'Місто проживання': fake.city(),
        'Адреса проживання': fake.address().replace('\n', ', '),
        'Телефон': fake.phone_number(),
        'Email': fake.email()
    }


# Створення і запис у CSV файл
with open('employees.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Прізвище', 'Ім’я', 'По батькові', 'Стать', 'Дата народження', 'Посада',
                                              'Місто проживання', 'Адреса проживання', 'Телефон', 'Email'])
    writer.writeheader()

    # Генерування записів
    male_count = int(num_records * male_ratio)
    female_count = num_records - male_count

    # Додаємо чоловіків
    for _ in range(male_count):
        writer.writerow(generate_employee('M'))

    # Додаємо жінок
    for _ in range(female_count):
        writer.writerow(generate_employee('F'))

print(f"Згенеровано {num_records} записів у файл employees.csv.")
