from ui import UI
from actions import Actions

actions = Actions()
ui_obj = UI(actions.helptext, actions.actions)

while True:
    ui_obj.print_and_prompt()