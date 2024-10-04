from googletrans import Translator

def TransLate(text: str, scr: str, dest: str) -> str:
    """Переклад тексту"""
    translator = Translator()
    try:
        translated = translator.translate(text, src=scr, dest=dest)
        return translated.text
    except Exception as e:
        return f"Помилка: {str(e)}"

def LangDetect(text: str, set: str = "all") -> str:
    """Визначає мову тексту та коефіцієнт довіри"""
    translator = Translator()
    try:
        detection = translator.detect(text)
        if set == "lang":
            return detection.lang
        elif set == "confidence":
            return str(detection.confidence)
        else:
            return f"Мова: {detection.lang}, Коефіцієнт довіри: {detection.confidence}"
    except Exception as e:
        return f"Помилка: {str(e)}"

def CodeLang(lang: str) -> str:
    """Повертає код або назву мови"""
    languages = {'uk': 'Ukrainian', 'en': 'English', 'fr': 'French', 'de': 'German'}  # додай більше мов
    try:
        if lang in languages:
            return languages[lang]
        else:
            for code, name in languages.items():
                if lang.lower() == name.lower():
                    return code
        return "Мова або код не знайдені"
    except Exception as e:
        return f"Помилка: {str(e)}"


def LanguageList(out: str = "screen", text: str = "") -> str:
    """Виводить таблицю мов і переклад тексту"""
    translator = Translator()
    languages = {
        'uk': 'Ukrainian', 'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic',
        'hy': 'Armenian'
    }  # додай більше мов
    try:
        result = []
        if text:
            for idx, (code, lang) in enumerate(languages.items(), 1):
                translated_text = translator.translate(text, dest=code).text
                result.append(f"{idx} {lang:<15} {code:<10} {translated_text}")
        else:
            for idx, (code, lang) in enumerate(languages.items(), 1):
                result.append(f"{idx} {lang:<15} {code:<10}")

        output = "N  Language       ISO-639 code  Text\n" + "-" * 50 + "\n" + "\n".join(result)

        if out == "screen":
            print(output)
        elif out == "file":
            with open("languages.txt", "w", encoding="utf-8") as f:
                f.write(output)
        return "Ok"
    except Exception as e:
        return f"Помилка: {str(e)}"
