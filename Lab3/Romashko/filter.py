import os
from Packeges.modul1 import TransLate
from langdetect import detect
from configparser import ConfigParser


def file_statistics(filename):
    """Повертає статистику файлу"""
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        char_count = len(content)
        word_count = len(content.split())
        sentence_count = content.count('.') + content.count('!') + content.count('?')
        language = detect(content)
    return char_count, word_count, sentence_count, language


def main():
    config = ConfigParser()
    config.read('config.ini')

    text_file = config['Settings']['text_file']
    target_language = config['Settings']['target_language']
    output = config['Settings']['output']
    max_chars = int(config['Settings']['max_chars'])
    max_words = int(config['Settings']['max_words'])
    max_sentences = int(config['Settings']['max_sentences'])

    if not os.path.exists(text_file):
        print("Файл не знайдено")
        return

    char_count, word_count, sentence_count, language = file_statistics(text_file)

    print(f"Файл: {text_file}")
    print(f"Кількість символів: {char_count}")
    print(f"Кількість слів: {word_count}")
    print(f"Кількість речень: {sentence_count}")
    print(f"Мова: {language}")

    if char_count > max_chars or word_count > max_words or sentence_count > max_sentences:
        print("Перевищено ліміти конфігураційного файлу")
        return

    with open(text_file, 'r', encoding='utf-8') as file:
        content = file.read()

    translated_text = TransLate(content, language, target_language)

    if output == "screen":
        print(f"Переклад на {target_language}:")
        print(translated_text)
    elif output == "file":
        output_file = f"{os.path.splitext(text_file)[0]}_{target_language}.txt"
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(translated_text)
        print("Ok")


if __name__ == "__main__":
    main()
