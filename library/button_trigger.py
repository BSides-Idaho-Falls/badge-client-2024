"""
This is where buttons get translated into actions.

* action_forward()
    - In menus, moves cursor down one item
    - When in a house, moves player in the direction they're facing
* action_backward()
    - In menus, moves cursor up one item
    - When in a house, changes the direction a player is facing
* primary_select()
    - In menus, enters or selects selected item
    - When in a house, performs the selected action
* secondary_select()
    - When in a menu, goes back to parent menu.
    - When in a house, leaves house
* primary_modify()
    - When in a house, changes selected action
* secondary_modify()
    - noop
* hybrid_action_move(direction: str)  # left, right, up, down
    - Combination of action_backward() and action_forward().
    - When in a house, moves player <direction>
"""
from display_helper import KONAMI_LOGO
from library import atomics
from library.action_class import ButtonAction
from library.actions_animation_menu import AnimationMenuActions
from library.actions_game import GameActions
from library.actions_game_menu import GameMenuActions
from library.actions_info_menu import InfoMenuActions
from library.actions_light_menu import LightMenuActions
from library.actions_main_menu import MainMenuActions
from library.actions_offline_menu import OfflineMenuActions
from library.actions_shop_menu import ShopMenuActions
from library.display import QueueItem

BUTTON_ACTION_MAPPER: dict = {
    "game": GameActions,
    "game_menu": GameMenuActions,
    "main_menu": MainMenuActions,
    "info_menu": InfoMenuActions,
    "light_menu": LightMenuActions,
    "animate_menu": AnimationMenuActions,
    "offline_menu": OfflineMenuActions,
    "shop_menu": ShopMenuActions
}


def _is_konami_complete() -> bool:
    return atomics.KONAMI_PRESSES == atomics.EXPECTED_KONAMI


def _correct_konami_sequence() -> bool:
    return "".join(atomics.EXPECTED_KONAMI).startswith("".join(atomics.KONAMI_PRESSES))


def _konami_complete():
    atomics.KONAMI_PRESSES = []
    print("You did the konami code!")
    atomics.DISPLAY.queue_item(QueueItem("animation", KONAMI_LOGO, 150))


def process_konami(btn_pressed):
    if not atomics.most_recent():
        return
    atomics.KONAMI_PRESSES.append(btn_pressed)
    if _is_konami_complete():
        return _konami_complete()
    if not _correct_konami_sequence():
        atomics.KONAMI_PRESSES = []


def create_instance(class_name):
    instance = BUTTON_ACTION_MAPPER.get(class_name)
    return instance() if class_name in BUTTON_ACTION_MAPPER else None


def action_forward():
    if atomics.FREEZE_BUTTONS:
        return

    action: ButtonAction = create_instance(atomics.STATE)
    if not action:
        print(f"action_forward no function for this state | {atomics.STATE}")
        return
    try:
        action.action_forward()
    except NotImplementedError:
        print(f"Extra action being attempted - {atomics.STATE}")


def action_backward():
    if atomics.FREEZE_BUTTONS:
        return

    action: ButtonAction = create_instance(atomics.STATE)
    if not action:
        print("action_backward has no function for this state")
        return
    try:
        action.action_backward()
    except NotImplementedError:
        print(f"Extra action being attempted - {atomics.STATE}")


def primary_select(konami_override=False):
    if atomics.FREEZE_BUTTONS:
        return

    is_menu: bool = "_menu" in atomics.STATE
    if is_menu and not konami_override:
        process_konami("b")

    action: ButtonAction = create_instance(atomics.STATE)
    if not action:
        print("primary_select has no function for this state")
        return
    try:
        action.primary_select()
    except NotImplementedError:
        print(f"Extra action being attempted - {atomics.STATE}")


def secondary_select():
    if atomics.FREEZE_BUTTONS:
        return

    action: ButtonAction = create_instance(atomics.STATE)
    if not action:
        print("secondary_select has no function for this state")
        return
    try:
        action.secondary_select()
    except NotImplementedError:
        print(f"Extra action being attempted - {atomics.STATE}")


def secondary_modify():
    if atomics.FREEZE_BUTTONS:
        return

    action: ButtonAction = create_instance(atomics.STATE)
    if not action:
        print("secondary_modify has no function for this state")
        return
    try:
        action.secondary_modify()
    except NotImplementedError:
        print(f"Extra action being attempted - {atomics.STATE}")


def primary_modify():
    if atomics.FREEZE_BUTTONS:
        return

    is_menu: bool = "_menu" in atomics.STATE
    if is_menu:
        process_konami("a")

    action: ButtonAction = create_instance(atomics.STATE)
    if not action:
        print("primary_modify has no function for this state")
        return
    try:
        action.primary_modify()
    except NotImplementedError:
        print(f"Extra action being attempted - {atomics.STATE}")


def hybrid_action_move(direction):
    """This combines actions. It will change the direction the player looks, then move the player."""
    if atomics.FREEZE_BUTTONS:
        return

    action: ButtonAction = create_instance(atomics.STATE)
    if not action:
        print("hybrid_action_move has no function for this state.")
        return
    try:
        action.hybrid_action_move(direction)
    except NotImplementedError:
        print(f"Extra action being attempted - {atomics.STATE}")


def dpad_action(direction):
    """This is an attempt for a dpad action being mapped to multiple things."""
    if atomics.FREEZE_BUTTONS:
        return

    is_menu: bool = "_menu" in atomics.STATE

    if is_menu:
        process_konami(direction)
        if direction == "right":
            return primary_select(konami_override=True)
        if direction == "left":
            return secondary_select()
        if direction == "down":
            return action_forward()
        if direction == "up":
            return action_backward()
        print("darn im returning!")
        return  # Shouldn't happen but who knows
    return hybrid_action_move(direction)


def dpad_action_left():
    return dpad_action("left")


def dpad_action_right():
    return dpad_action("right")


def dpad_action_up():
    return dpad_action("up")


def dpad_action_down():
    return dpad_action("down")


def double_up():
    """Better konami code detection"""
    if atomics.FREEZE_BUTTONS:
        return
    is_menu: bool = "_menu" in atomics.STATE
    if not is_menu:
        return
    process_konami("up")
    process_konami("up")


def double_down():
    """Better konami code detection"""
    if atomics.FREEZE_BUTTONS:
        return
    is_menu: bool = "_menu" in atomics.STATE
    if not is_menu:
        return
    process_konami("down")
    process_konami("down")