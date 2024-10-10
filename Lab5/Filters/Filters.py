import string


# Функція для читання тексту з файлу та обробки помилок
def read_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"Помилка: файл {file_name} не знайдено.")
        return None
    except Exception as e:
        print(f"Сталася помилка при читанні файлу: {e}")
        return None


# Функція для отримання першого речення
def get_first_sentence(text):
    sentences = text.split('.')
    if sentences:
        return sentences[0]
    return ""


# Функція для сортування слів по алфавіту з урахуванням українських та англійських слів
def sort_words(text):
    # Видалення пунктуації
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)

    # Отримання списку слів
    words = text.split()

    # Розподіл на українські та англійські слова
    uk_words = [word for word in words if word[0].lower() in 'абвгґдежзийклмнопрстуфхцчшщьюяєії']
    en_words = [word for word in words if word[0].lower() in 'abcdefghijklmnopqrstuvwxyz']

    # Сортування
    uk_words.sort()
    en_words.sort()

    return uk_words + en_words


# Основна частина програми
def main():
    file_name = 'text.txt'
    text = read_file(file_name)

    if text is None:
        return

    # Виведення першого речення
    first_sentence = get_first_sentence(text)
    print(f"Перше речення: {first_sentence}\n")

    # Отримання та сортування слів
    sorted_words = sort_words(text)

    print("Відсортовані слова:")
    print(sorted_words)
    print(f"Кількість слів: {len(sorted_words)}")


if __name__ == "__main__":
    main()
