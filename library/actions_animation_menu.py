import display_helper
from library import atomics
from library.action_class import ButtonAction
from library.display import QueueItem
from library.navigation import MainMenu


class AnimationMenuActions(ButtonAction):

    def __init__(self):
        super().__init__()

    def short_press0(self):
        atomics.ANIMATE_MENU.increment_state()

    def short_press1(self):
        atomics.ANIMATE_MENU.decrement_state()

    def long_press1(self):
        atomics.MAIN_MENU = MainMenu()
        atomics.STATE = "main_menu"
        atomics.ANIMATE_MENU = None

    def long_press0(self):
        selected_item = atomics.ANIMATE_MENU.selected_item
        if selected_item == "potato":
            for i in range(0, 3):
                atomics.DISPLAY.queue_item(
                    QueueItem(
                        "animation",
                        data=display_helper.WINKING_POTATO,
                        ms_between_frames=50
                    )
                )
            atomics.ANIMATE_MENU.modified = True
