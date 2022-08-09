from termcolor import colored
from rich.console import Console
from torch_backend import filter_words


def main():
    console = Console()

    with open('data/allowed.txt', 'r') as f:
        words = [i.strip() for i in f.readlines()]

    colors = {'0': 'white', '1': 'green', '2': 'yellow'}

    title = """
         _       ______  ____  ____  __    ______   ____  ____  ______
        | |     / / __ \/ __ \/ __ \/ /   / ____/  / __ )/ __ \/_  __/
     | | /| / / / / / /_/ / / / / /   / __/    / __  / / / / / /
    | |/ |/ / /_/ / _, _/ /_/ / /___/ /___   / /_/ / /_/ / / /
    |__/|__/\____/_/ |_/_____/_____/_____/  /_____/\____/ /_/
    """

    instructions = """
    +-----------------------------------------+
    | Please enter hints like this:           |
    | 0: [bold white]white[/bold white]                                |
    | 1: [bold green]green[/bold green]                                |
    | 2: [bold yellow]yellow[/bold yellow]                               |
    |                                         |
    | When you solve the puzzle, type [white]"[bold white]solved[/bold white]"|
    +-----------------------------------------+"""
    console.print(title, justify='center', style='bold magenta')
    console.print(instructions, justify='center')
    print()
    print()

    def print_puzzle(words, hints):
        console.print('    -----------------------', justify='center')
        for ind, word in enumerate(words):
            my_string = ''
            for ind2, letter in enumerate(word):
                my_string += f'[bold {colors[hints[ind][ind2]]}]{letter}[/bold {colors[hints[ind][ind2]]}] '
            my_string = '    ' + my_string[:-1]
            console.print(my_string, justify='center')
        console.print('    -----------------------', justify='center')

    print(f'{len(words)} words left')
    console.print('Try word: [bold magenta]PIOUS[/bold magenta]')

    words_list = ['PIOUS']
    hints_list = []
    while True:
        c_code = input('Enter hints or type \"solved\": ')
        print("\033[A                                              \033[A")
        print("\033[A                                              \033[A")
        print("\033[A                                              \033[A")

        if c_code == 'solved':
            hints_list.append('11111')
            print()
            print_puzzle(words_list, hints_list)
            print()
            console.print(
                '    ', ':party_popper:', '[bold magenta]CONGRATULATIONS![/bold magenta]', ':party_popper:', justify='center')
            print()
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

        print_puzzle(words_list, hints_list)
        print('\n\n')

        words, new_word = filter_words(words_list[-1].lower(), words, c_code)
        words_list.append(new_word.upper())
        console.print(f'Try: [bold magenta]{new_word.upper()}[/bold magenta]')


if __name__ == '__main__':
    main()
