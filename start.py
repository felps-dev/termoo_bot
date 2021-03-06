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

letter_priority = {
    'A': 54.63,
    'B': 1.04,
    'C': 3.88,
    'D': 4.99,
    'E': 52.57,
    'F': 1.02,
    'G': 1.30,
    'H': 1.28,
    'I': 56.18,
    'J': 0.40,
    'K': 0.02,
    'L': 2.78,
    'M': 4.74,
    'N': 5.05,
    'O': 50.73,
    'P': 2.52,
    'Q': 1.20,
    'R': 6.53,
    'S': 7.81,
    'T': 4.34,
    'U': 54.63,
    'V': 30.67,
    'W': 0.01,
    'X': 0.21,
    'Y': 0.01,
    'Z': 0.47,
}

great_words = ['BOMBA', 'FOLHA', 'PILHA',
               'DACIO',
               'BROCA',
               'HIATO',
               'SINTO',
               'TIGRE',
               'CESTA', 'ROSEA', 'MELAO']

consoantes = 'BCÇDFGHJKLMNPQRSTV'

with open("palavras_filtradas.txt", "r", encoding="UTF-8") as a_file:
    for line in a_file:
        word_list.append(line.strip())


def update_status():
    width, height = pyautogui.size()
    box = (width / 2 - 250, height / 2 - 330,
           width / 2 + 250,  height / 2 + 260)
    image = ImageGrab.grab(box)
    if(image.getpixel(coordinates[0][0]) == (49, 43, 45)):
        return None
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
            if(not letter in negated_words):
                negated_words.append(letter)
        elif(status[index] in [1, 2]):
            if(not letter in allowed_words):
                allowed_words.append(letter)
    return allowed_words, negated_words


def get_chances(last_line, word, list, allowed_words, negated_words, has_green, alread_tried):
    # Primeiro filtra todas as palavras que podem
    # ser possíveis, ou seja, possuem
    almost = []
    for g_word in list:
        allow = False
        if(g_word in alread_tried):
            continue
        for cha in g_word:
            if(cha in negated_words):
                if(cha not in allowed_words):
                    allow = False
                    break
            allow = True
        for alw in allowed_words:
            if(alw in g_word):
                continue
            else:
                allow = False
                break
        if(allow):
            almost.append(g_word)
    certain = []
    # Filtra as palavras que possuem as letras exatamente
    # nos espaços verdes
    if(not has_green):
        certain = almost
    else:
        for g_word in almost:
            allow = False
            for index, cha in enumerate(g_word):
                if(last_line[index] == 1):
                    # Letra exatamente no espaço verde.
                    if(cha == word[index]):
                        allow = True
                    else:
                        allow = False
                        break
            if(allow):
                certain.append(g_word)

    # Filtra as palavras por ordem de prioridade das letras.
    def get_sum_qulity(w):
        sum = 0
        for cha in w:
            sum += letter_priority[cha]
            sum += 50 if cha in consoantes else 0
            sum -= 300 if w.count(cha) > 2 else 0
        sum -= 300 if w[3] == 'A' and w[4] == 'O' else 0
        return sum

    certain.sort(reverse=True, key=get_sum_qulity)
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
alread_tried = []
i_win = False
for tries in [0, 1, 2, 3, 4, 5]:
    result_ok = False
    print('Tentativa ' + str(tries))
    while not result_ok:
        if(resultado is None):
            i_win = True
            break
        pyautogui.press(['backspace', 'backspace',
                        'backspace', 'backspace', 'backspace'], interval=0.08)
        if(tries == 0):
            test_word = random.choice(great_words)
        else:
            w_tries = 0
            while(test_word in alread_tried):
                # Pega a primeira da lista filtrada
                test_word = filtered_list[0 + w_tries]
                w_tries += 1

        pyautogui.write(test_word, interval=0.08)
        pyautogui.press('enter')
        time.sleep(2)
        resultado = update_status()
        result_ok = 3 not in resultado[tries] or tries == 5
        has_green = 1 in resultado[tries]
        i_win = resultado[tries] == [1, 1, 1, 1, 1]
        alread_tried.append(test_word)
    if(i_win):
        print('Consegui!')
        break
    else:
        allowed_words, negated_words = get_words(
            test_word, resultado[tries], allowed_words, negated_words)
        filtered_list = get_chances(
            resultado[tries], test_word, filtered_list, allowed_words, negated_words, has_green, alread_tried)
        # print(filtered_list)
        print('Possibilidades: ' + str(len(filtered_list)))
