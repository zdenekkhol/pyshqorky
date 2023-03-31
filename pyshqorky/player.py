"""
Původní návrh:
class Player
- id
- name
- color
- type
* oponent_id
"""

class Player:
    """ Třída, kde se bude držet info o jednom hráči."""

    #: Typ hráče: Člověk
    TYPE_HUMAN = 0
    #: Typ hráče: Počítač
    TYPE_AI = 1
    
    #: Tvar hracího kamene: čtverec
    SHAPE_SQUARE = 0
    #: Tvar hracího kamene: kruh
    SHAPE_CIRCLE = 1
    #: Tvar hracího kamene: křížky a kolečka
    SHAPE_SYMBOL = 2

    #: Úroveň hry počítače: agresivní
    AI_LVL_AGRESSIVE = 0
    #: Úroveň hry počítače: normální
    AI_LVL_BALANCED = 1
    #: Úroveň hry počítače: defenzivní
    AI_LVL_DEFENSIVE = 2
    #: Úroveň hry počítače: ještě defenzivnější
    AI_LVL_ULTRADEFENS = 3
    #: Úroveň hry počítače: skrytá, pouze pro mód open game
    AI_LVL_OPEN_GAME = 4
    
    #: Číslo seznamu pro úroveň hry počítače: moje
    AI_SCORE_MY = 0
    #: Číslo seznamu pro úroveň hry počítače: protivníkovo
    AI_SCORE_OPONENT = 1
    
    #: Hodnoty pro hru počítače jako slovník se seznamy. Index je Úroveň hry počítače, první level seznamu znamená moje nebo protivníkovo, další level je počet kamenů v posuzované pětici.
    #: Příklad: `AI_VALUES[AI_LVL_DEFENSIVE][AI_SCORE_MY][počet kamenů v pětici]`.
    #: Jeden řádek definice slovníku je `AI_LVL: ([moje skóre], [protivníkovo skóre])`.
    #: Více v `pyshqorky.board.Board.score_board`
    AI_VALUES = {0: ([0, 10, 100, 1000, 10000, 100000], [0, 20, 200, 2000, 20000, 200000]),
                 1: ([0, 10, 100, 1000, 10000, 100000], [0, 50, 500, 5000, 50000, 500000]),
                 2: ([0, 10, 100, 1000, 10000, 100000], [0, 100, 1000, 10000, 100000, 1000000]),
                 3: ([0, 10, 100, 1000, 2000, 100000], [0, 100, 1000, 10000, 20000, 1000000]),
                 4: ([0, 10, 100, 1000, 0, 0], [0, 100, 1000, 10000, 20000, 1000000])
                }

    #: Seznam hodnot typu hráče
    type_list = ("Human", "AI")
    #: Seznam hodnot tvaru kamene
    shape_list = ("Square", "Circle", "Symbol")
    #: Seznam hodnot úrovně hry počítače
    ai_level_list = ("Agressive", "Balanced", "Defensive", "Ultra defensive")
    #: Seznam hodnot tahů pro open game
    open_game_turns_list = {str(i+3) for i in range(8)}
    open_game_turns_list = {"3", "4", "5", "6", "8", "10"}
    def __init__(self, id: int, name: str, color: tuple, shape: int = SHAPE_SQUARE, ai_level:int = AI_LVL_BALANCED, type: int = TYPE_HUMAN) -> None:
        #: id hráče (navrženo tak, že bude nabývat pouze hodnot 1 a -1)
        self.id = id
        #: Jméno hráče
        self.name = name
        #: Barva kamenů hráče
        self.color = color
        #: Tvar kamenů hráče
        self.shape = shape
        #: Typ hráče
        self.type = type
        #: Úroveň hry počítače
        self.ai_level = ai_level
        #: Počet vítězných her od začátku
        self.win_count: int = 0

    @property
    def oponent_id(self) -> int:
        """Vrací id protihráče."""
        return -self.id
    
    def wins(self) -> None:
        """Tento hráč tuto hru vyhrál, přičteme mu to do počtu vítězství"""
        self.win_count += 1
    

    

