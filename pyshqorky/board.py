"""
Původní návrh:
class Board
- grid
* reset
* draw
* score - z pohledu hráče
* score_wnd5
* wintie - globálně, 0 = jedeme dál, 1/-1 win hráč, jinak = tie
* wintie_wnd5
"""

import pygame
import random
import math
from pyshqorky.players import *

class Board:
    """ Třída pro práci s herní deskou. Jsou zde informace o rozmístění kamenů na desce, vyhodnocení stavu desky a její vykreslování."""

    #: Obsah prázdného pole na desce.
    CELL_EMPTY = 0

    #: Vítězství nebo remíza? Nic, nejde určit.
    WT_NONE = 0
    #: Vítězství nebo remíza? Jsem vítěz.
    WT_WINNER = 1
    #: Vítězství nebo remíza? Nejsem vítěz.
    WT_LOSER = 2
    #: Vítězství nebo remíza? Je to remíza.
    WT_TIE = 3

    def __init__(self, rows, cols, width, height, x_offset, y_offset) -> None:
        #: Počet řádků.
        self.rows = rows
        #: Počet sloupců.
        self.cols = cols
        #: Velikost na ose x v px.
        self.width = width
        #: Velikost na ose y v px.
        self.height = height
        #: Velikost strany jednoho hracího pole.
        self.sqsize = width // cols
        #: Posun na ose x, kam se bude deska vykreslovat.
        self.x_offset = x_offset
        #: Posun na ose y, kam se bude deska vykreslovat.
        self.y_offset = y_offset
        #: Seznam seznamů (2D pole), kde je umístění kamenů na desce.
        self.grid = [[0 for col in range(self.cols)] for row in range(self.rows)]
        #: Seznam seznamů (2D pole), kde je info o hracích polích, které použijeme pro vyhodnocení interakce s hráčem.
        self.btns = [[pygame.Rect for col in range(self.cols)] for row in range(self.rows)]

    def draw(self, screen, players: Players = None) -> None: # type: ignore
        """
        Vykreslení herní plochy. Nejdřív nakreslíme pole `pygame.Rect`. Každý v poli o velikosti o jedna menší, než velikost `pyshqorky.board.Board.sqsize`. To pro zobrazení mřížky.
        Potom, pokud jsme dostali v parametru i seznam hráčů, nakreslíme jejich kameny na každé pole, kde se nacházejí.
        """
        # vykreslení herní plochy
        for r in range (self.rows):
            for c in range(self.cols):
                self.btns[r][c] = pygame.draw.rect(screen, (0x40,0x40,0x40), pygame.Rect(self.sqsize*r+self.x_offset, # type: ignore
                                                                                         self.sqsize*c+self.y_offset,
                                                                                         self.sqsize-1, self.sqsize-1))
                if players is not None:
                    for id, pl in players.items():
                        if self.grid[r][c] == pl.id:
                            match pl.shape:
                                case Player.SHAPE_SQUARE:
                                    pygame.draw.rect(screen, pl.color, pygame.Rect(self.sqsize*r+self.x_offset+(self.sqsize/8),
                                                                                    self.sqsize*c+self.y_offset+(self.sqsize/8),
                                                                                    self.sqsize-(self.sqsize/4),
                                                                                    self.sqsize-(self.sqsize/4)))
                                case Player.SHAPE_CIRCLE:
                                    pygame.draw.circle(screen, pl.color, (self.sqsize*r+self.x_offset+(self.sqsize/2),
                                                                        self.sqsize*c+self.y_offset+(self.sqsize/2)),
                                                                        self.sqsize*0.45)
                                case Player.SHAPE_SYMBOL:
                                    #ToDo
                                    pass

    def score_wnd5(self, window: list, player: Player) -> int:
        """
        Ohodnocení výseku 1x5 z hrací desky z pohledu hráče (počítačového). Jestliže je tu prázdno nebo jsou tu oba protivníci, skóre je nula.
        Jestli je tu hráč sám, skóre se přičítá a pokud pouze protihráč, skóre se odečítá.
        Kolik se toho přičte nebo odečte, záleží na úrovni hry počítače, jestli jsou to kameny hráče nebo protivníka a počtu kamenů v této pětici.
        Hodnota se vezme ze slovníku `pyshqorky.player.Player.AI_VALUES`
        """
        score = 0

        # jestliže je tu prázdno
        if window.count(Board.CELL_EMPTY) == 5:
            return 0
        # jestliže v této pětici jsme
        if window.count(player.id) != 0:
            # a nejsme tu sami
            if window.count(player.oponent_id) != 0:
                return 0
            # pokud jsme tu sami
            else:
                # tak přičteme hodnotu odpovídající počtu našich značek
                score += Player.AI_VALUES[player.ai_level][Player.AI_SCORE_MY][window.count(player.id)]
        else:
            # je tu pouze protivník, takže odečteme hodnotu odpovídající počtu jeho značek
            score -= Player.AI_VALUES[player.ai_level][Player.AI_SCORE_OPONENT][window.count(player.oponent_id)]

        return score

    def score_board(self, player: Player) -> int:
        """
        Projedeme na hrací desce všechna pole 1x5. Pro každé takové pole voláme `pyshqorky.board.Board.score_wnd5`.
        Nasčítáme všechna skóre, která se nám vrátila a vracíme to jako ohodnocení celé desky.
        """
        score = 0

        # ohodnocení řádků
        for r in range(self.rows):
            row_array = [int(i) for i in list(self.grid[r][:])]
            for c in range(self.cols-4):
                window = row_array[c:c+5]
                score += self.score_wnd5(window, player)

        # ohodnocení sloupců
        for c in range(self.cols):
            col_array = [i[:][c] for i in self.grid]
            for r in range(self.rows-4):
                window = col_array[r:r+5]
                score += self.score_wnd5(window, player)

        # ohodnocení diagonál (\ i /)
        for r in range(self.rows-4):
            for c in range(self.cols-4):
                # to je \
                window = [self.grid[r+i][c+i] for i in range(5)]
                score += self.score_wnd5(window, player)
                # a tohle /
                window = [self.grid[r+4-i][c+i] for i in range(5)]
                score += self.score_wnd5(window, player)

        return score

    # vracíme WT_NONE, když je možné hrát dál
    # WT_WINNER, pokud je vítězem player
    # WT_LOSER, pokud je vítězem oponent
    # WT_TIE, pokud v této pětici nejde dosáhnout vítězství
    def win_tie_wnd5(self, window: list, player: Player) -> int:
        """
        Zde hodnotíme z pohledu výhra / prohra /remíza výsek z boardu o velikosti 1 x 5.
        Pokud je tam pouze player, vyhrál. Pokud je tam pouze oponent, player prohrál.
        Pokud jsou tam oba, tak zde již nikdo pětku neudělá.
        Pokud neplatí nic z toho, je možné hrát dál.
        :param window: Výsek z boardu 1 x 5.
        :type window: list
        :param player: Hodnotíme z pohledu tohoto hráče
        :type player: Player
        :return: Vrací možné hodnoty WT_WINNER, pokud player zvítězil, WT_LOSER pokud prohrál, WT_TIE pokud zde již není možné vyhrát nebo WT_NONE, pokud je možné zde ještě vyhrát.
        :rtype: int
        """
        # jestliže máme pět
        if window.count(player.id) == 5:
            return self.WT_WINNER

        # jestli má pět oponent
        if window.count(player.oponent_id) == 5:
            return self.WT_LOSER
        
        # zde již není možné vyhrát
        if window.count(player.id) != 0 and window.count(player.oponent_id) != 0:
            return self.WT_TIE
        
        # jinak je možné pořád hrát dál
        return self.WT_NONE

    def win_tie(self, player: Player) -> int:
        """
        Zde projedeme celý board a z pohledu hráče zhodnotíme, jestli jsme vyhráli nebo prohráli, jestli je remíza nebo hrajeme dál.
        Technicky je to provedeno tak, že projedeme všechna okna 1 x 5, co jsou na desce a zhodnotíme je ve vlastní funkci win_tie_wnd5.
        Podle toho odsud vracíme hodnoty dál.
        :param player: Hodnotíme z pohledu tohoto hráče
        :type player: Player
        :return: Vrací možné hodnoty WT_WINNER, pokud player zvítězil, WT_LOSER pokud prohrál, WT_TIE pokud je remíza nebo WT_NONE, pokud je možné hrát dál.
        :rtype: int
        """
        wt5 = None
        tie = self.WT_TIE

        # ohodnocení řádků
        for r in range(self.rows):
            row_array = [int(i) for i in list(self.grid[r][:])]
            for c in range(self.cols-4):
                window = row_array[c:c+5]
                wt5 = self.win_tie_wnd5(window, player)
                if (wt5 in (self.WT_WINNER, self.WT_LOSER)):
                    return wt5
                elif wt5 == self.WT_NONE:
                    tie = wt5

        # ohodnocení sloupců
        for c in range(self.cols):
            col_array = [i[:][c] for i in self.grid]
            for r in range(self.rows-4):
                window = col_array[r:r+5]
                wt5 = self.win_tie_wnd5(window, player)
                if (wt5 in (self.WT_WINNER, self.WT_LOSER)):
                    return wt5
                elif wt5 == self.WT_NONE:
                    tie = wt5

        # ohodnocení diagonál (\ i /)
        for r in range(self.rows-4):
            for c in range(self.cols-4):
                # to je \
                window = [self.grid[r+i][c+i] for i in range(5)]
                wt5 = self.win_tie_wnd5(window, player)
                if (wt5 in (self.WT_WINNER, self.WT_LOSER)):
                    return wt5
                elif wt5 == self.WT_NONE:
                    tie = wt5
                # a tohle /
                window = [self.grid[r+4-i][c+i] for i in range(5)]
                wt5 = self.win_tie_wnd5(window, player)
                if (wt5 in (self.WT_WINNER, self.WT_LOSER)):
                    return wt5
                elif wt5 == self.WT_NONE:
                    tie = wt5
        
        # nikdo ještě nevyhrál, tak vracíme, jestli byla remíza nebo ne
        return tie

    def best_move(self, player: Player) -> tuple:
        avail_moves = []
        # spočítáme ohodnocení každého možného tahu a potom se rozhodneme
        best_score = -math.inf
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == Board.CELL_EMPTY:
                    self.grid[r][c] = player.id
                    score = self.score_board(player)
                    self.grid[r][c] = Board.CELL_EMPTY
                    if (score > best_score):
                        avail_moves = []
                        avail_moves.append((r,c))
                        best_score = score
                    elif (score == best_score):
                        avail_moves.append((r,c))
        return random.choice(avail_moves)

    def make_move(self, player: Player, coord: tuple):
        self.grid[coord[0]][coord[1]] = player.id

    def reset(self):
        self.grid = [[0 for col in range(self.cols)] for row in range(self.rows)]
        self.btns = [[pygame.Rect for col in range(self.cols)] for row in range(self.rows)]
        pass
