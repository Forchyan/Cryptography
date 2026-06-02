import nltk
nltk.download('words')
from nltk.corpus import words


ALF = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ENGLISH_WORDS = set(words.words())



def guide():
    print('''
1 - Зашифровать\n
2 - Расшифровать\n
3 - Атака по известному тексту\n
4 - Атака по шифрованному тексту\n
5 - Атака по шифрованному тексту со "словарем"\n
----------------------------------------
0 - Выход\n
    ''')

def key_input():
    return int(input('Введите ключ (0-25):'))

def main():
    menu_input = ''
    while menu_input != '0':
        guide()
        menu_input = input('Введите № команды:').strip()

        if menu_input == '1':
            text = input('Введите слово для шифрования:').strip().upper()
            while key := key_input():
                if 0 <= key <= 25:
                    break
                print(f'Ключ неверный, попробуйте снова!')
            print(f'Зашифрованное слово: {''.join([ALF[(ALF.find(i) + key) % 26] for i in text]).lower()}')

        if menu_input == '2':
            text = input('Введите слово для расшифрования:').strip().upper()
            while key := key_input():
                if 0 <= key <= 25:
                    break
                print(f'Ключ неверный, попробуйте снова!')
            print(f'Расшифрованное слово: {''.join([ALF[(ALF.find(i) - key) % 26] for i in text]).lower()}')

        if menu_input == '3':
            text_1 = input('Введите открытое слово:').strip().upper()
            text_2 = input('Введите зашифрованное слово:').strip().upper()
            if 0 < len(text_1) == len(text_2) > 0:
                answer = set([(ALF.find(symb_2) - ALF.find(symb_1)) % 26 for symb_1,symb_2 in zip(text_1, text_2)])
                if len(answer) == 1:
                    print(f"Вероятный ключ:{answer.pop()}")
                else:
                    print(f'Это не шифр Цезаря')
            else:
                print('Слова не равны, возвращаюсь в меню')

        if menu_input == '4':
            text = input('Введите зашифрованное слово:').strip().upper()
            if not text:
                print('Слово не должно быть пустым!')
            else:
                for i in range(26):
                    answer = ''.join([ALF[(ALF.find(symb) - i) % 26] for symb in text]).lower()  # добавил % 26
                    print(f'Вариант №{i + 1}: {answer}')

        if menu_input == '5':
            text = input('Введите зашифрованное слово:').strip().upper()

            best_key, best_score, best_text = 0, 0, ""

            for key in range(26):
                decrypted = ''.join([ALF[(ALF.find(symb) - key) % 26] for symb in text]).lower()  # добавил % 26

                score = 1 if decrypted in ENGLISH_WORDS else 0

                if score > best_score:
                    best_score, best_key, best_text = score, key, decrypted

            if best_score > 0:
                print(f'Найденный ключ: {best_key}')
                print(f'Расшифрованное слово: {best_text}')
            else:
                print('Слово не найдено в словаре. Попробуйте пункт 4.')



if __name__ == '__main__':
    main()



