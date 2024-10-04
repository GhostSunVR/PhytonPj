from Packeges.modul2 import TransLate, LangDetect, CodeLang, LanguageList

def main():
    print(TransLate("Привіт", "uk", "en"))
    print(LangDetect("Hello"))
    print(CodeLang("English"))
    print(LanguageList("screen", "Добрий день"))

if __name__ == "__main__":
    main()
