from inspect import signature
from colorama import Back

class UI(object):
    def __init__(self, help, mapping):
        self.help = {**{'q': 'Quit the program (q <exit-code>)'}, **help}
        self.mapping = {**{'q': exit}, **mapping}

    def print_menu(self):
        print(Back.BLUE + '====== PTC CLIENT MENU ======')
        for cmd, helptext in self.help.items():
            print(cmd, ':', helptext)
        print(Back.BLUE + '====== PTC CLIENT MENU ======')

    def prompt(self):
        user_input = input('Select an option: ')
        tokens = user_input.split(' ')
        option = tokens[0]

        if option not in self.mapping or len(signature(self.mapping[option]).parameters) != len(tokens) - 1:
            print(Back.RED + 'Invalid option!')
            return

        resp_template = 'Server Response: {}'
        resp = ''

        print(Back.GREEN + '====== PTC CLIENT OUTPUT ======')
        if len(tokens) == 1:
            resp = resp_template.format(self.mapping[option]())
        else:
            resp = resp_template.format(self.mapping[option](*tokens[1:]))

        print(resp)
        print(Back.GREEN + '====== PTC CLIENT OUTPUT ======')

    def print_and_prompt(self):
        self.print_menu()
        self.prompt()