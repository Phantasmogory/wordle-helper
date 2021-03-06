import re
import sys
from collections import Counter
from itertools import chain
import operator
import clipboard

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

    # for word in word_dict:
    #    for letter in word:
    #        letters[letter] = letters.get(letter, 0) + 1
    # replaced with
    letters = Counter(chain.from_iterable(word_dict))

    total = sum(letters.values())
    letters_freqs = {letter: value / total for letter, value in letters.items()}


def calc_word_weight(word):
    score = 0
    for letter in set(word):
        score += letters_freqs[letter]
    return score


def sort_by_word_weight(words):
    sort_by = operator.itemgetter(1)
    return sorted([(word, calc_word_weight(word)) for word in words], key=sort_by, reverse=True)


def display_word_table(word_weights):
    for (word, freq) in word_weights:
        print(f"{word:<10} | {freq:<5.2}")


def solver(present, absent, template='.'*WORD_LENGTH):
    global solutions
    if present != '?':
        solutions = [word for word in solutions if all(letter in word for letter in present)]

    if absent != '?':
        solutions = [word for word in solutions if all(letter not in word for letter in absent)]
    pattern = re.compile(template)
    solutions = [word for word in solutions if pattern.match(word)]


def clipboard_mode():
    global solutions
    text = clipboard.paste()
    present = absent = ''
    template = ['.']*WORD_LENGTH
    for i, match in enumerate(re.findall(r'(bg-present|bg-absent|bg-correct)[^<]*>(.)</div', text)):
        if match[0] == 'bg-present':
            present += match[1]
            if template[i % WORD_LENGTH][0] == '^':
                template[i % WORD_LENGTH] += match[1]
            if template[i % WORD_LENGTH][0] == '.':
                template[i % WORD_LENGTH] = '^' + match[1]
        if match[0] == 'bg-absent':
            absent += match[1]
        if match[0] == 'bg-correct':
            present += match[1]
            template[i % WORD_LENGTH] = match[1]
    teplatestr = ''.join([f'[{t}]' if '^' in t else t for t in template])
    if present or absent:
        print('Found in clipboard:')
        print('python main.py', ''.join(list(set(present))), ''.join(list(set(absent))), teplatestr)
        load_dict()
        solutions = word_dict.copy()
        solver(present, absent, teplatestr)
        print('Word count after apply rules:', len(solutions))
        display_word_table(sort_by_word_weight(solutions)[:5])


def main():
    global solutions
    load_dict()
    solutions = word_dict.copy()
    if len(sys.argv) == 4:
        present = sys.argv[1]
        absent = sys.argv[2]
        template = sys.argv[3]
        print('Total word count:', len(solutions))
        solver(present, absent, template)
        print('Word count after apply rules:', len(solutions))
        display_word_table(sort_by_word_weight(solutions)[:5])
    else:
        print('Usage: python main.py <letters in word|?> <letters not in word|?> <template|.....>')
        print('Examples: python main.py ? ? .....')
        print('Examples: python main.py ???????? ???????????? .????????')
        print('Examples: python main.py ???? ?????? "...??[^??]" ')
        print('Examples: python main.py')
        print('  For Clipboard mode')
        clipboard_mode()



if __name__ == '__main__':
    main()

