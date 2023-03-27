"""
class Player
- id
- name
- color
- type
* oponent_id
"""

class Player:
    TYPE_HUMAN = 1
    TYPE_AI = 2
    
    def __init__(self, id, name, color, player_type = TYPE_HUMAN):
        self.id = id
        self.name = name
        self.color = color
        self.player_type = player_type

    def oponent_id(self):
        return -self.id
