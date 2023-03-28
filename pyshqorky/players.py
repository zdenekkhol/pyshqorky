from pyshqorky.player import *

"""
class Players (list)
- actint
* switch_active
* active
* nonactive
"""

class Players(dict[int, Player]):
    PLAYER_1 = 1
    PLAYER_2 = -1

    def __init__(self, dict: dict[int, Player]):
        self.reset()
        super().__init__(dict)

    @property
    def active(self) -> Player:
        return self.__getitem__(self._active_id)
    
    @property
    def oponent(self) -> Player:
        return self.__getitem__(-self._active_id)
    
    def next(self) -> None:
        self._active_id = -self._active_id

    def reset(self) -> None:
        self._active_id = self.PLAYER_1