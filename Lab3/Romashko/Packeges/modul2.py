from deep_translator import GoogleTranslator

def TransLate(text: str, scr: str, dest: str) -> str:
    """Переклад тексту через deep_translator"""
    try:
        translator = GoogleTranslator(source=scr, target=dest)
        translated_text = translator.translate(text)
        return translated_text
    except Exception as e:
        return f"Помилка: {str(e)}"

from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0

def LangDetect(text: str, set: str = "all") -> str:
    """Визначення мови через langdetect"""
    try:
        language = detect(text)
        if set == "lang":
            return language
        else:
            return f"Мова: {language}"  # Для langdetect немає коефіцієнта довіри
    except Exception as e:
        return f"Помилка: {str(e)}"

def CodeLang(lang: str) -> str:
    """Аналогічна функція з першого модуля"""
    languages = {'uk': 'Ukrainian', 'en': 'English', 'fr': 'French', 'de': 'German'}
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
    """Аналогічна функція з першого модуля"""
    languages = {
        'uk': 'Ukrainian', 'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic', 'hy': 'Armenian'
    }
    result = []
    try:
        for idx, (code, lang) in enumerate(languages.items(), 1):
            translated_text = GoogleTranslator(target=code).translate(text)
            result.append(f"{idx} {lang:<15} {code:<10} {translated_text}")

        output = "N  Language       ISO-639 code  Text\n" + "-" * 50 + "\n" + "\n".join(result)

        if out == "screen":
            print(output)
        elif out == "file":
            with open("languages_deep.txt", "w", encoding="utf-8") as f:
                f.write(output)
        return "Ok"
    except Exception as e:
        return f"Помилка: {str(e)}"
