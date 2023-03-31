"""
Původní návrh:
class Players (list)
- actint
* switch_active
* active
* nonactive
"""

from __future__ import annotations
import pickle
from pyshqorky.player import *

class Players(dict[int, Player]):
    """
    Seznam hráčů. Je navržen tak, že hráč jedna má id 1, hráč dva má id -1.
    Object je děděn ze slovníku, kde index je shodný s id hráče, hodnota je objekt `pyshqorky.player.Player`.
    Na začátku naplníme slovník. Očekávám dva hráče s id 1 a -1.
    """
    #: Id prvího hráče
    PLAYER_1 = 1
    #: Id druhého hráče
    PLAYER_2 = -1 

    def __init__(self, new_dict: dict[int, Player]):
        #: Id právě hrajícího hráče.
        self.id_active: int = self.PLAYER_1
        #: Počet kol pro open game, implicitně 5
        self.open_game_turns = 5
        # a voláme konstruktor rodiče
        super().__init__(new_dict)

    @property
    def active(self) -> Player:
        """Vrací hráče, který **je** právě na tahu"""
        return self.__getitem__(self.id_active)
    
    @property
    def oponent(self) -> Player:
        """Vrací hráče, který právě **není** na tahu"""
        return self.__getitem__(-self.id_active)
    
    def next(self) -> None:
        """Přepnutí na dalšího hráče."""
        self.id_active = -self.id_active

    def reset(self) -> None:
        """Nastavení nové hry. Začíná hráč číslo jedna"""
        self.id_active = self.PLAYER_1

    def save(self, filename: str = ".settings.dmp") -> None:
        """
        Uložení konfigurace hry.
        Otevřeme soubor filename (defultně .settings.dmp) pro zápis a dumpneme tam tento objekt. Poté za sebou zavřeme.
        """
        pf = open(filename, "wb")
        pickle.dump(self, pf)
        pf.close()

    @staticmethod
    def load(filename: str = ".settings.dmp") -> Players:
        """
        Načtení konfigurace hry.
        Zkusíme otevřít soubor filename (defaultně .settings.dmp) pro čtení.
        Pokud se povedlo, načteme do proměnné loaded, vynulujeme počet vítězství a vrátíme.
        Očekáváme, že v souboru je instance objektu Players. Na konec po sobě zavřeme.
        Pokud se nepovedlo otevřít soubor, vracíme None.
        """
        try:
            pf = open(filename, "rb")
            loaded: Players = pickle.load(pf)
            pf.close()
            loaded.reset_win_count()
            return loaded
        except FileNotFoundError:
            return None # type: ignore
        
    def score(self) -> str:
        """Vrací skóre vítězství pro zobrazení ve tvaru 0 : 0"""
        return "{} : {}".format(self.__getitem__(Players.PLAYER_1).win_count,
                                self.__getitem__(Players.PLAYER_2).win_count)
    
    def reset_win_count(self) -> None:
        """Vynuluje počet vítězství pro oba hráče"""
        for i, p in self.items():
            p.win_count = 0
