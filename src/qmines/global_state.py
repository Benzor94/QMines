from typing import NoReturn


class StateTracker:
    game_is_active = False

    def __init__(self) -> NoReturn:
        raise NotImplementedError('This class cannot be instantiated.')

