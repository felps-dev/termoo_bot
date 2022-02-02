from distutils.sysconfig import PREFIX
from PIL import ImageGrab
import pyautogui
import time
import random

coordinates = [
    [(110, 91), (195, 81), (278, 81), (366, 80), (449, 79)],
    [(62, 140), (147, 139), (232, 139), (315, 137), (398, 137)],
    [(61, 223), (144, 219), (227, 221), (313, 221), (395, 218)],
    [(60, 306), (145, 306), (230, 306), (315, 306), (397, 306)],
    [(62, 388), (145, 388), (229, 388), (312, 388), (397, 388)],
    [(60, 471), (174, 471), (230, 471), (313, 471), (395, 471)],
]

word_list = []

with open("palavras_filtradas.txt", "r", encoding="UTF-8") as a_file:
    for line in a_file:
        word_list.append(line.strip())


def update_status():
    width, height = pyautogui.size()
    box = (width / 2 - 250, height / 2 - 330,
           width / 2 + 250,  height / 2 + 260)
    image = ImageGrab.grab(box)
    resultado = []
    for x in coordinates:
        temp = []
        for y in x:
            pix = image.getpixel(y)
            if(pix == (58, 163, 148)):
                temp.append(1)  # Certo
            elif(pix == (49, 42, 44)):
                temp.append(0)  # Errado
            elif(pix == (211, 173, 105)):
                temp.append(2)  # Quase
            else:
                temp.append(3)  # Indefinido
        resultado.append(temp)
    return resultado


def get_words(word, status, allowed_words, negated_words):
    for index, letter in enumerate(word):
        if(status[index] in [0]):
            negated_words.append(letter)
        elif(status[index] in [1, 2]):
            allowed_words.append(letter)
    return allowed_words, negated_words


def get_chances(last_line, word, list, allowed_words, negated_words, has_green):
    # Primeiro filtra todas as palavras que podem
    # ser possíveis, ou seja, possuem
    almost = []
    for g_word in list:
        allow = False
        for cha in g_word:
            if(cha in negated_words):
                if(cha not in allowed_words):
                    allow = False
                    break
            allow = True
        if(allow):
            almost.append(g_word)
    certain = []
    if(not has_green):
        certain = almost
    else:
        for g_word in almost:
            allow = False
            for index, cha in enumerate(g_word):
                if(last_line[index] == 1):
                    if(cha == word[index]):
                        allow = True
                    else:
                        allow = False
                        break
            if(allow):
                certain.append(g_word)
    return certain


# O jogo consiste em 6 jogadas, a cada jogada ele verifica a
# linha para descobrir se está ou não próximo
time.sleep(4)
resultado = update_status()
# Pega uma palavra aleatória.
filtered_list = word_list
allowed_words = []
negated_words = []
has_green = False
great_words = ['BOMBA', 'FOLHA', 'PILHA',
               'DACIO',
               'BROCA',
               'HIATO',
               'SINTO',
               'TIGRE',
               'CESTA']
i_win = False
for tries in [0, 1, 2, 3, 4, 5]:
    result_ok = False
    print('Tentativa ' + str(tries))
    while not result_ok:
        pyautogui.press(['backspace', 'backspace',
                        'backspace', 'backspace', 'backspace'], interval=0.08)
        if(tries == 0):
            test_word = random.choice(great_words)
        else:
            test_word = random.choice(filtered_list)
        pyautogui.write(test_word, interval=0.08)
        pyautogui.press('enter')
        time.sleep(3)
        resultado = update_status()
        result_ok = 3 not in resultado[tries] or tries == 5
        has_green = 1 in resultado[tries]
        i_win = resultado[tries] == [1, 1, 1, 1, 1]
    allowed_words, negated_words = get_words(
        test_word, resultado[tries], allowed_words, negated_words)
    filtered_list = get_chances(
        resultado[tries], test_word, filtered_list, allowed_words, negated_words, has_green)
    print('Possibilidades: ' + str(len(filtered_list)))
    if(i_win):
        print('Consegui!')
        break
