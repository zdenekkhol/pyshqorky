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
    
    def __init__(self, id: int, name: str, color: tuple, type: int = TYPE_HUMAN):
        self._id = id
        self.name = name
        self.color = color
        self.type = type

    @property
    def id(self) -> int:
        return self._id

    @property
    def oponent_id(self) -> int:
        return -self.id
    

    

