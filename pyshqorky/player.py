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

    AI_LVL_AGRESSIVE = 0
    AI_LVL_BALANCED = 1
    AI_LVL_DEFENSIVE = 2
    AI_LVL_ULTRADEFENS = 3
    
    AI_SCORE_MY = 0
    AI_SCORE_OPONENT = 1
    
    # LVL: SCORE SELF, SCORE OPONENT
    AI_VALUES = {0: ([0, 10, 100, 1000, 10000, 100000], [0, 20, 200, 2000, 20000, 200000]),
                 1: ([0, 10, 100, 1000, 10000, 100000], [0, 50, 500, 5000, 50000, 500000]),
                 2: ([0, 10, 100, 1000, 10000, 100000], [0, 100, 1000, 10000, 100000, 1000000]),
                 3: ([0, 10, 100, 1000, 2000, 100000], [0, 100, 1000, 10000, 20000, 1000000])}

    
    type_list = ("Human", "AI")
    shape_list = ("Square", "Circle", "Symbol")
    ai_level_list = ("Agressive", "Balanced", "Defensive", "Ultra defensive")
    
    def __init__(self, id: int, name: str, color: tuple, shape: int = SHAPE_SQUARE, ai_level:int = AI_LVL_BALANCED, type: int = TYPE_HUMAN):
        self._id = id
        self.name = name
        self.color = color
        self.shape = shape
        self.type = type
        self.ai_level = ai_level

    @property
    def id(self) -> int:
        return self._id

    @property
    def oponent_id(self) -> int:
        return -self.id
    

    

