from library import atomics
from library.action_class import ButtonAction
from library.actions_animation_menu import AnimationMenuActions
from library.actions_game import GameActions
from library.actions_game_menu import GameMenuActions
from library.actions_info_menu import InfoMenuActions
from library.actions_main_menu import MainMenuActions
from library.actions_offline_menu import OfflineMenuActions

BUTTON_ACTION_MAPPER: dict = {
    "game": GameActions,
    "game_menu": GameMenuActions,
    "main_menu": MainMenuActions,
    "info_menu": InfoMenuActions,
    "animate_menu": AnimationMenuActions,
    "offline_menu": OfflineMenuActions
}


def create_instance(class_name):
    instance = BUTTON_ACTION_MAPPER.get(class_name)
    return instance() if class_name in BUTTON_ACTION_MAPPER else None


def press0():
    if atomics.FREEZE_BUTTONS:
        return
    action: ButtonAction = create_instance(atomics.STATE)
    if not action:
        print("Short Press 0 has no function for this state")
        return
    try:
        action.short_press0()
    except NotImplementedError:
        print("Short Press 0 has no function for this state")


def press1():
    if atomics.FREEZE_BUTTONS:
        return

    action: ButtonAction = create_instance(atomics.STATE)
    if not action:
        print("Short Press 1 has no function for this state")
        return
    try:
        action.short_press1()
    except NotImplementedError:
        print("Short Press 1 has no function for this state")


def long_press0():
    if atomics.FREEZE_BUTTONS:
        return

    action: ButtonAction = create_instance(atomics.STATE)
    if not action:
        print("Long Press 0 has no function for this state")
        return
    try:
        action.long_press0()
    except NotImplementedError:
        print("Long press 0 has no function for this state")


def long_press1():
    if atomics.FREEZE_BUTTONS:
        return

    action: ButtonAction = create_instance(atomics.STATE)
    if not action:
        print("Long Press 1 has no function for this state")
        return
    try:
        action.long_press1()
    except NotImplementedError:
        print("Long Press 1 has no function for this state")


def double_press0():
    if atomics.FREEZE_BUTTONS:
        return

    action: ButtonAction = create_instance(atomics.STATE)
    if not action:
        print("Double Press 0 has no function for this state")
        return
    try:
        action.double_press0()
    except NotImplementedError:
        print("Double Press 0 has no function for this state")


def double_press1():
    if atomics.FREEZE_BUTTONS:
        return

    action: ButtonAction = create_instance(atomics.STATE)
    if not action:
        print("Double Press 1 has no function for this state")
        return
    try:
        action.double_press1()
    except NotImplementedError:
        print("Double Press 1 has no function for this state")
