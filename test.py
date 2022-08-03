from termcolor import colored
from main import find_words
from pyfiglet import Figlet
import os


with open('answers.txt', 'r') as f:
    words = [i.strip() for i in f.readlines()]

f = Figlet(font='slant')
colors = {'0': 'white', '1': 'green', '2': 'yellow'}

print()
print(colored(f.renderText(f'WORDLE BOT'), 'cyan'))
print('+--------------------------------------------+')
# print(f"| {colored('WELCOME TO THE WORLDS GREATEST WORDLE BOT!', 'cyan')}".ljust(46), '|')
# print('|'.ljust(44), '|')
print('| Please enter hints like this:'.ljust(44), '|')
print('| 0: white'.ljust(44), '|')
print(f'| 1: {colored("green", "green")}'.ljust(53), '|')
print(f'| 2: {colored("yellow", "yellow")}'.ljust(53), '|')
print('|'.ljust(44), '|')
print('| When you solve the puzzle, type "solved"'.ljust(44), '|')
print('+--------------------------------------------+')
print()


def print_puzzle(words, hints):
    for ind, word in enumerate(words):
        for ind2, letter in enumerate(word):
            print(colored(letter, colors[hints[ind][ind2]]), end=' ')
        print()


print(f'Try word: {colored("PIOUS", "magenta")}')

words_list = ['PIOUS']
hints_list = []
while True:
    c_code = input('Enter hints or type \"solved\": ')
    # os.system('cls' if os.name == 'nt' else 'clear')

    if c_code == 'solved':
        hints_list.append('11111')
        print()
        print_puzzle(words_list, hints_list)
        print(colored(
            f'\n {chr(0x1f389)} CONGRATULATIONS!{chr(0x1f389)} \n', 'green'))
        break

    try:
        if any(int(i) > 2 for i in c_code) or len(c_code) != 5:
            print(colored('Wrong input, try again', 'red'))
            continue
    except:
        print(colored('Wrong input, try again', 'red'))
        continue

    print()
    hints_list.append(c_code)

    print('\n\n')
    print(colored('Thinking...', 'cyan'))

    words, new_word = find_words(words_list[-1].lower(), words, c_code)
    # new_word = 'CRANE'  # plugin the actual program here!
    words_list.append(new_word.upper())

    print(f'now_try: {colored(new_word.upper(),  "magenta")}')
