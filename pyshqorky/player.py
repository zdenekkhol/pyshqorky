"""
class Player
- id
- name
- color
- type
* oponent_id
"""

class Player:
    TYPE_HUMAN = 0
    TYPE_AI = 1
    SHAPE_SQUARE = 0
    SHAPE_CIRCLE = 1
    SHAPE_SYMBOL = 2
    
    type_list = ("Human", "AI")
    shape_list = ("Square", "Circle", "Symbol")
    
    def __init__(self, id: int, name: str, color: tuple, shape: int = SHAPE_SQUARE, type: int = TYPE_HUMAN):
        self._id = id
        self.name = name
        self.color = color
        self.shape = shape
        self.type = type

    @property
    def id(self) -> int:
        return self._id

    @property
    def oponent_id(self) -> int:
        return -self.id
    

    

