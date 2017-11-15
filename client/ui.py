from inspect import signature

class UI(object):
    def __init__(self, help, mapping):
        self.help = {**{'q': 'Quit the program'}, **help}
        self.mapping = {**{'q': exit}, **mapping}

    def print_menu(self):
        print('====== PTC CLIENT MENU ======')
        for cmd, helptext in self.help.items():
            print(cmd, ':', helptext)
        print('====== PTC CLIENT MENU ======')

    def prompt(self):
        user_input = input('Select an option: ')
        tokens = user_input.split(' ')
        option = tokens[0]

        if option not in self.mapping or len(signature(self.mapping[option]).parameters) != len(tokens) - 1:
            print('Invalid option!')

        print('====== PTC CLIENT OUTPUT ======')
        if len(tokens) == 1:
            self.mapping[option]()
        else:
            self.mapping[option](*tokens[1:])
        print('====== PTC CLIENT OUTPUT ======')

    def print_and_prompt(self):
        self.print_menu()
        self.prompt()