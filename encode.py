from unidecode import unidecode

def part_of_Antygona(file_name = 'Antygona.txt', n=0 ):
    file = open(file_name, "r")
    text = file.read()
    lenght = len(text)/5  # 20% Antygony
    # pierwsza część Antygony z 5
    start = int(lenght*n)
    stop = int(start + lenght)
    text = text[start:stop]
    text = unidecode(text)
    return text

def list_of_bits(text, i ):
    list = []
    print(f'DEBUG: text[{i}] = {text[i]}')
    b = bin(int.from_bytes(text[i].encode(), 'big'))
    for j in range(len(b)):
        if (j != 1):
            list.append(b[j])
    if len(list) <8:
        x = 8 - len(list)
        for i in range(x):
            list.insert(0,'0')
    return list

if __name__ == '__main__':
    n =0 # pierwsza część Antygony z 5
    text = part_of_Antygona("Antygona.txt", n)
    for i in range(len(text)):
        print(list_of_bits(text,i))