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
        if selected_item not in display_helper.ANIMATION_MAPPER:
            # This could happen when we have not locally stored animations in
            # the menu. Add code to pull data from server then display it :)
            AnimationMenuActions.display_remote_animation(selected_item)
            return
        AnimationMenuActions.display_local_animation(selected_item)

    @staticmethod
    def display_remote_animation(name):
        atomics.DISPLAY.queue_item(
            QueueItem(
                "text",
                data={
                    "message": [
                        "Remote",
                        "animations",
                        "not yet",
                        "supported"
                    ],
                    "delay": 2000
                }
            )
        )
        atomics.ANIMATE_MENU.modified = True

    @staticmethod
    def display_local_animation(name):
        item = display_helper.ANIMATION_MAPPER[name]
        contents = item["contents"]
        iterations = item.get("iterations", 1)
        frame_time = item.get("frame_time_ms", 50)
        for i in range(0, iterations):
            atomics.DISPLAY.queue_item(
                QueueItem(
                    "animation",
                    data=contents,
                    ms_between_frames=frame_time
                )
            )
        atomics.ANIMATE_MENU.modified = True
