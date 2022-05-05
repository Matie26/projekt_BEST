from kamene.all import *
import argparse

from kamene.layers.inet import TCP


def check(file_name):
    file = file_name
    a = rdpcap(file)

    for i in range(len(a)):
        try:
            if a[i][TCP].dport == 5000:
                pkt = a[i][0][Raw]
                txt = pkt.load
                pkt2 = a[i][0]
                txt2 = pkt2.load
                cookie_index = txt2.find(b"Cookie")
                cookie = txt2[cookie_index:cookie_index + 49]
                best = 'b3st'
                letter_index = txt.find(b"User-Agent")
                letter = txt[letter_index:letter_index + 83]
                letter = letter.decode('ascii')
                c = 0
                for l in letter:
                    if l == "l":
                        c = c + 1
                if c > 2:
                    return 'Plik zawiera ukryty tekst'
        except:
            continue
    return "Plik nie zawiera ukrytego tekstu "

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Path to file to be checked")
    parser.parse_args()
    args = parser.parse_args()
    file = args.file
    print(check(file))
    #check(file)

if __name__ == "__main__":
    main()
