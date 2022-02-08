from unidecode import unidecode

with open("palavrasnovas.txt", "r", encoding="UTF-8") as a_file:
    final_file = []
    for line in a_file:
        stripped_line = line.strip().replace('.', '').replace("'", '').replace("-", '')
        if(len(stripped_line) == 5):
            final_file.append(unidecode(stripped_line.upper()))

    with open('palavras_filtradas.txt', 'w') as f:
        for item in final_file:
            f.write("%s\n" % item)
