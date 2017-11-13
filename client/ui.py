from inspect import signature

class UI(object):
    def __init__(self, help, mapping):
        self.help = {**{'q': 'Quit the program'}, **help}
        self.mapping = {**{'q': exit}, **mapping}

    def print_menu(self):
        for cmd, helptext in self.help.items():
            print(cmd, ':', helptext)

    def prompt(self):
        user_input = input('Select an option: ')
        tokens = user_input.split(' ')
        option = tokens[0]

        if option not in self.mapping or len(signature(self.mapping[option]).parameters) != len(tokens) - 1:
            print('Invalid option!')
        elif len(tokens) == 1:
            self.mapping[option]()
        else:
            self.mapping[option](*tokens[1:])

    def print_and_prompt(self):
        self.print_menu()
        self.prompt()