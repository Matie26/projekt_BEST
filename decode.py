import binascii

from kamene.all import *
import argparse

from kamene.layers.inet import TCP


def check(file_name):
    file = file_name
    file2 = open("zakodowanie.txt", 'w+')
    a = rdpcap(file)
    for i in range(len(a)):
        try:
            if a[i][TCP].dport == 5000:
                pkt = a[i][0][Raw]
                txt = pkt.load
                letter_index = txt.find(b"User-Agent")
                letter = ""
                for j in 22,26,48,59,62,65,68,79:
                    letter += str(txt[letter_index+j:letter_index + j + 1])[2]
                letter = letter.replace("l","0")
                #print(letter)
                letter = int(letter, 2)
                letter = letter.to_bytes(1, "big")
                letter = letter.decode()
                file2.write(letter)

        except:
            continue
    file2.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Path to file to be checked")
    parser.parse_args()
    args = parser.parse_args()
    file = args.file
    print(check(file))
    #check(file)


if __name__ == "__main__":
    print(check("sekret.pcap"))
    text = '00110000'
    binary_int = int(text, 2)

    # Getting the byte number
    byte_number = binary_int.bit_length() + 7 // 8

    # Getting an array of bytes
    binary_array = binary_int.to_bytes(1, "big")

    # Converting the array into ASCII text
    ascii_text = binary_array.decode()

    # Getting the ASCII value

