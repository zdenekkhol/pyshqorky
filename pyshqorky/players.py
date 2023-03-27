from player import *

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

    actint = 1

    def active(self):
        return self.items[self.actint]
    
    def nonactive(self):
        return self.item[-self.actint]
    
    def switch_active(self):
        self.actint = -self.actint