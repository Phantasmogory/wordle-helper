import re
import sys
from collections import Counter
from itertools import chain
import operator


word_dict = []
letters = {}
letters_freqs = {}
WORD_LENGTH = 5
solutions = []


def load_dict(dict_name=r'dictionary\rus.txt'):
    global word_dict
    global letters
    global letters_freqs
    with open(dict_name, "r", encoding='utf-8') as word_list:
        word_dict = word_list.read().split('\n')

    #for word in word_dict:
    #    for letter in word:
    #        letters[letter] = letters.get(letter, 0) + 1
    # replaced with
    letters = Counter(chain.from_iterable(word_dict))

    total = sum(letters.values())
    letters_freqs = {character: value / total for character, value in letters.items()}


def calculate_word_commonality(word):
    score = 0.0
    for char in word:
        score += letters_freqs[char]
    return score / (WORD_LENGTH - len(set(word)) + 1)


def sort_by_word_commonality(words):
    sort_by = operator.itemgetter(1)
    return sorted([(word, calculate_word_commonality(word)) for word in words], key=sort_by, reverse=True)


def display_word_table(word_commonalities):
    for (word, freq) in word_commonalities:
        print(f"{word:<10} | {freq:<5.2}")


def solver(present, absent, placement='.'*WORD_LENGTH):
    global solutions
    if present != '?':
        solutions = [word for word in solutions if all(letter in word for letter in present)]

    if absent != '?':
        solutions = [word for word in solutions if all(letter not in word for letter in absent)]
    pattern = re.compile(placement)
    solutions = [word for word in solutions if pattern.match(word)]


def main():
    global solutions
    load_dict()
    solutions = word_dict.copy()
    if len(sys.argv) == 4:
        present = sys.argv[1]
        absent = sys.argv[2]
        teplate = sys.argv[3]
        print('Total word count:', len(solutions))
        solver(present, absent, teplate)
        print('Word count after apply rules:', len(solutions))
        display_word_table(sort_by_word_commonality(solutions)[:5])
    else:
        print("Usage: ./main.py <letters in word|?> <letters not in word|?> <placement|.....>")
        print("Examples: ./main.py ? ? .....")
        print("Examples: ./main.py орма иктпен .орма")
        exit()

if __name__ == '__main__':
    main()
