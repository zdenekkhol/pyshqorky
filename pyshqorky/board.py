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

    def __init__(self, rows: int, cols: int, width: int, height: int, x_offset: int, y_offset: int) -> None:
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
        self.tiles = [[pygame.Rect for col in range(self.cols)] for row in range(self.rows)]

    def draw(self, screen, players: Players | None = None, mark_coords: list[tuple[int, int]] | None = None) -> None:
        """
        Vykreslení herní plochy. Nejdřív nakreslíme pole `pygame.Rect`. Každý v poli o velikosti o jedna menší, než velikost `pyshqorky.board.Board.sqsize`. To pro zobrazení mřížky.
        Potom, pokud jsme dostali v parametru i seznam hráčů, nakreslíme jejich kameny na každé pole, kde se nacházejí.
        Nakonec nakreslíme zvýraznění, pokud je máme.
        """
        # vykreslení herní plochy
        for r in range (self.rows):
            for c in range(self.cols):
                # Vykreslení jednoho herního pole
                self.tiles[r][c] = pygame.draw.rect(screen, (0x40,0x40,0x40), #type: ignore
                    pygame.Rect(self.sqsize*r+self.x_offset, self.sqsize*c+self.y_offset, self.sqsize-1, self.sqsize-1))
                # Pokud jsme dostali i seznam hráčů
                if players is not None:
                    # projedem oba
                    for id, pl in players.items():
                        # a pokud je tenhle na tomto poli
                        if self.grid[r][c] == pl.id:
                            # tak ho nakreslíme
                            pl.draw(screen, r, c, self.x_offset, self.y_offset, self.sqsize)
        # nakonec vykreslení zvýraznění, pokud je přítomno
        if mark_coords is not None:
            # pro každé pole k zvýraznění
            for (r, c) in mark_coords:
                # pokud máme hráče 
                if players is not None:
                    # projedem oba
                    for id, pl in players.items():
                        # a pokud je tenhle na tomto poli
                        if self.grid[r][c] == pl.id:
                            # tak ho obtáhneme
                            pl.draw(screen, r, c, self.x_offset, self.y_offset, self.sqsize, True)
                # jinak uděláme pro zvýraznění tečku uprostřed
                else:
                    pygame.draw.circle(screen, (255, 255, 0), (self.sqsize*r+self.x_offset+(self.sqsize/2),
                                                    self.sqsize*c+self.y_offset+(self.sqsize/2)),
                                                    self.sqsize*0.15)

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
        Inspirace zde: http://blog.trixi.cz/2013/02/popis-piskvorkoveho-algoritmu/
        """
        score = 0
        #"""
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
        """
        # optimalizovaný algoritmus, jenom nefunguje stejně
        for r in range(2, self.rows-2):
            for c in range(2, self.cols-2):
                # ohodnotíme řádky
                window = [self.grid[r-2+i][c] for i in range(5)]
                # budeme hodnotit pouze pokud tu není prázdno
                if window.count(Board.CELL_EMPTY != 5):
                    score += self.score_wnd5(window, player)
                # sloupce
                window = [self.grid[r][c-2+i] for i in range(5)]
                # budeme hodnotit pouze pokud tu není prázdno
                if window.count(Board.CELL_EMPTY != 5):
                    score += self.score_wnd5(window, player)
                # diagonála \
                window = [self.grid[r-2+i][c-2+i] for i in range(5)]
                # budeme hodnotit pouze pokud tu není prázdno
                if window.count(Board.CELL_EMPTY != 5):
                    score += self.score_wnd5(window, player)
                # diagonála /
                window = [self.grid[r+2-i][c-2+i] for i in range(5)]
                # budeme hodnotit pouze pokud tu není prázdno
                if window.count(Board.CELL_EMPTY != 5):
                    score += self.score_wnd5(window, player)
        """
        return score
            
    # vracíme WT_NONE, když je možné hrát dál
    # WT_WINNER, pokud je vítězem player
    # WT_LOSER, pokud je vítězem oponent
    # WT_TIE, pokud v této pětici nejde dosáhnout vítězství
    def win_tie_wnd5(self, window: list[int], player: Player) -> int:
        """
        Zde hodnotíme z pohledu hráče výsek z boardu o velikosti 1 x 5 na možnou výhru, prohru nebo remízu.
        Pokud je tam pouze player, vyhrál. Pokud je tam pouze oponent, player prohrál.
        Pokud jsou tam oba, tak zde již nikdo pětku neudělá. Pokud neplatí nic z toho, je možné hrát dál.
        Vrací možné hodnoty WT_WINNER, pokud player zvítězil, WT_LOSER pokud prohrál, WT_TIE pokud zde již není možné vyhrát nebo WT_NONE, pokud je možné zde ještě vyhrát.
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

    def win_tie(self, player: Player) -> tuple[int, list[tuple[int, int]]]:
        """
        Zde projedeme celý board a z pohledu hráče zhodnotíme, jestli jsme vyhráli nebo prohráli, jestli je remíza nebo hrajeme dál.
        Technicky je to provedeno tak, že projedeme všechna okna 1 x 5, co jsou na desce a zhodnotíme je ve vlastní funkci win_tie_wnd5.
        Podle toho odsud vracíme hodnoty dál. Pro vítězství i kde bylo zvítězeno pro označení dané pětky.
        Jako hlavní integer vracíme WT_WINNER, pokud player zvítězil, WT_LOSER pokud prohrál, WT_TIE pokud je remíza nebo WT_NONE, pokud je možné hrát dál.
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
                    return (wt5, [(r, c+i) for i in range(5)])
                elif wt5 == self.WT_NONE:
                    tie = wt5

        # ohodnocení sloupců
        for c in range(self.cols):
            col_array = [i[:][c] for i in self.grid]
            for r in range(self.rows-4):
                window = col_array[r:r+5]
                wt5 = self.win_tie_wnd5(window, player)
                if (wt5 in (self.WT_WINNER, self.WT_LOSER)):
                    return (wt5, [(r+i,c) for i in range(5)])
                elif wt5 == self.WT_NONE:
                    tie = wt5

        # ohodnocení diagonál (\ i /)
        for r in range(self.rows-4):
            for c in range(self.cols-4):
                # to je \
                window = [self.grid[r+i][c+i] for i in range(5)]
                wt5 = self.win_tie_wnd5(window, player)
                if (wt5 in (self.WT_WINNER, self.WT_LOSER)):
                    return (wt5, [(r+i, c+i) for i in range(5)])
                elif wt5 == self.WT_NONE:
                    tie = wt5
                # a tohle /
                window = [self.grid[r+4-i][c+i] for i in range(5)]
                wt5 = self.win_tie_wnd5(window, player)
                if (wt5 in (self.WT_WINNER, self.WT_LOSER)):
                    return (wt5, [(r+4-i, c+i) for i in range(5)])
                elif wt5 == self.WT_NONE:
                    tie = wt5
        
        # nikdo ještě nevyhrál, tak vracíme, jestli byla remíza nebo ne
        return (tie, list())

    def best_move(self, player: Player) -> tuple:
        """
        Najdeme, který tah hráče z možných bude ohodnocen nejvyšším skóre. Všechny s tímto skóre si dáme do seznamu a z něho jeden náhodně vybereme.
        """
        # možné tahy
        avail_moves = []
        # na začátek je nejlepší skóre dostatečně malé, třeba mínus nekonečno
        best_score = -math.inf
        # projedeme všechny pole na hrací desce
        for r in range(self.rows):
            for c in range(self.cols):
                # pokud je prázdné
                if self.grid[r][c] == Board.CELL_EMPTY:
                    # tak si ho pro teď obsadíme
                    self.grid[r][c] = player.id
                    # a spočítáme jeho skóre
                    score = self.score_board(player)
                    # pole vrátíme zase zpět na prázdné
                    self.grid[r][c] = Board.CELL_EMPTY
                    # pokud je skóre vyšši než předchozí nejvyšší
                    if (score > best_score):
                        # vynulujeme seznam s možnými předchozími tahy
                        avail_moves = []
                        # a přidáme tam tento
                        avail_moves.append((r,c))
                        # nejlepší skóre je tedy toto naše nové
                        best_score = score
                    # jinak, pokud je zjištěné skóre shodné s nejvyššim
                    elif (score == best_score):
                        # tak přidáme tento tah mezi nejlepší
                        avail_moves.append((r,c))
        # vrátíme náhodně vybraný tah z těch nejlepších
        return random.choice(avail_moves)

    def make_move(self, player: Player, coord: tuple) -> None:
        """
        Položíme značku hráče `pyshqorky.player.Player` na pole o souřadnicích coord.
        """
        self.grid[coord[0]][coord[1]] = player.id

    def reset(self) -> None:
        """
        Inicializujeme hrací desku - odebereme všechny značky hráčů.
        """
        self.grid = [[0 for col in range(self.cols)] for row in range(self.rows)]
