import numpy as np
import urllib.request


def tokenize(lines):
    words = []
    
    for line in lines:
        start = 0
        line = line.lower()
        word = ""
    
        while start < len(line):
            if line[start].isspace():
                if len(word) > 0:
                    words.append(word)
                    word = ""
            else:
                if len(word) > 0:
                    last_word = word[-1:]
                    
                    if not last_word.isdigit() == line[start].isdigit(): #123A
                        words.append(word)
                        word = ""
                    elif not last_word.isalpha() == line[start].isalpha(): #ABC1
                        words.append(word)
                        word = ""
                    else:
                        if not (line[start].isdigit() or line[start].isalpha()):
                            words.append(word)
                            word = ""

                    word += line[start]
                            
                else:
                    if line[start].isdigit():
                        word += line[start]
                    elif line[start].isalpha():
                        word += line[start]
                    else:
                        words.append(line[start]) 
                        
            start += 1
        if len(word) > 0:
            words.append(word)
            
    return words

def countWords(output, badElements=[]):

    numbers = dict()
    for word in output:
        if word in numbers: 
            numbers[word] += 1
        else:
            if not word in badElements:
                numbers[word] = 1 

    return numbers

def fileOpener(fileName):
    f = open(fileName)
    text = f.read()
    f.close()

    array = text.split("\n")
    return tokenize(array)
    
def printTopMost(frequencies,n):
    array = map(lambda lg: [lg, frequencies[lg]], frequencies)

    for word, freq in sorted(array, key=lambda x: -x[1])[:n]:
        print(word.ljust(20) + str(freq).rjust(5))

