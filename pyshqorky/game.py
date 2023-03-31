"""
Původní návrh:
class Game
- running
- mode - menumain, menusettings, run
- active_player
* menu_main
* menu_settings
* main
"""

import pygame
import pygame_gui
import copy
from pyshqorky.players import *
from pyshqorky.board import *
from pyshqorky.gui import *

class Game:
    """
    Třída pro ovládání hry a jejích událostí.
    Pokud z nějakého neznámého důvodu padá hra na chybu 'Player' nebo 'Players 'object has no attribute 'cokoliv',
    je třeba vymazat soubor .settings.dmp.
    """
    #: Stav hry: Konec
    STATE_QUIT = 0
    #: Stav hry: Hlavní menu
    STATE_MENU_MAIN = 1
    #: Stav hry: Běh hry (tahu)
    STATE_GAME_RUN = 2
    #: Stav hry: Konec tahu
    STATE_GAME_END_MOVE = 3
    #: Stav hry: Konec kola
    STATE_GAME_END_ROUND = 4
    #: Stav hry: Inicializace open game
    STATE_OPEN_GAME_INIT = 5
    #: Stav hry: Zahájení open game
    STATE_OPEN_GAME_OPEN = 6

    #: Mód hry: normální
    MODE_STANDARD = 0
    # Mód hry: hra k dokončení
    MODE_OPEN_GAME = 1

    def __init__(self):
        #: Stav hry. Na začátku se spouští do hlavního menu.
        self.state: int = Game.STATE_MENU_MAIN
        #: Mód hry.
        self.mode: int = Game.MODE_STANDARD
        #: Seznam polí, která budou zvýrazněna (další tah počítače nebo výhra)
        self.mark_coords: list[tuple[int, int]] | None = None
        #: Vytvoříme GUI pro menu a vykreslování
        self.gui = GUI()
        # A jmenuju se Pyshqorky
        pygame.display.set_caption("Pyshqorky")
        #: Hrací deska o velikosti 15x15 polí, 525x525 px, offset pro vykreslení do okna je 235x35 px
        self.board: Board = Board(15, 15, 525, 525, 235, 35)
        #: Seznam hráčů s implicitním nastavením.
        self.players: Players = Players({
            Players.PLAYER_1: Player(id=Players.PLAYER_1, name="Human", color=(255, 64, 64), shape=Player.SHAPE_SQUARE, type=Player.TYPE_HUMAN, ai_level=Player.AI_LVL_BALANCED), 
            Players.PLAYER_2: Player(id=Players.PLAYER_2, name="Computer", color=(64, 64, 255), shape=Player.SHAPE_CIRCLE, type=Player.TYPE_AI, ai_level=Player.AI_LVL_BALANCED)
            })
        # Pokud jsme nedokázali nahrát uložené nastavení
        if Players.load() == None:
            # tak uložíme to aktuální jako základ
            self.players.save()
        else:
            # jinak hráče nastavíme podle uloženého souboru
            self.players = self.players.load()

    def main(self):
        """
        Vstupní bod po spuštění hry. Hlavní smyčka hry.
        """
        msg: str = ""
        og_moves: int = 20
        players_backup: Players = Players({})
        # hlavní smyčka hry
        while self.state > Game.STATE_QUIT:
            # nastavení FPS + časová delta (dle dokumentace důležité pro GUI)
            time_delta = self.gui.clock.tick(self.gui.fps)/1000.0
            
            # je stav konec kola?
            if self.state == Game.STATE_GAME_END_ROUND:
                # zeptáme se, jestli pokračovat
                # správnou otázku jsme si připravili předem
                if self.gui.message_box(msg + " Do you want to play next round?"):
                    # pokud ano, jedem dál
                    self.run_new_round()
                else:
                    # jinak menu
                    self.state = Game.STATE_MENU_MAIN

            # je stav konec tahu? vyhodnocení a přepnutí
            if self.state == Game.STATE_GAME_END_MOVE:
                # co nám vrátí wintie?
                wt_state, to_mark = self.board.win_tie(self.players.active)
                # Není výhra, prohra ani remíza
                if wt_state == Board.WT_NONE:
                    # přepneme hráče
                    self.players.next()
                    # a hra jede dál
                    self.state = Game.STATE_GAME_RUN
                else:
                    msg = ""
                    # A hle něco se děje, ale co?
                    match wt_state:
                        # Hráč zvítězil
                        case Board.WT_WINNER:
                            print("And The Winner is : " + self.players.active.name)
                            self.mark_coords = to_mark
                            self.players.active.wins()
                            msg = "Winner is {}.".format(self.players.active.name)
                        # Hráč prohrál
                        case Board.WT_LOSER:
                            print("And The Winner is : " + self.players.oponent.name)
                            self.mark_coords = to_mark
                            self.players.oponent.wins()
                            msg = "Winner is {}.".format(self.players.oponent.name)
                        # Remíza - ani jeden jedokáže udělat na tomto boardu žádnou pětku
                        case Board.WT_TIE:
                            print("Remíza hoši")
                            msg = "Game is tie."
                    # Aktualizace skóre
                    self.gui.lbl_score.set_text(self.players.score())
                    self.state = Game.STATE_GAME_END_ROUND
            
            # je stav inicializace open game?
            if self.state == Game.STATE_OPEN_GAME_INIT:
                og_moves = 20
                # zazálohujeme si players
                players_backup = copy.deepcopy(self.players)
                # nastavíme typ hráče na AI 
                self.players.active.type = Player.TYPE_AI
                self.players.oponent.type = Player.TYPE_AI
                # nastavíme ai level open game
                self.players.active.ai_level = Player.AI_LVL_OPEN_GAME
                self.players.oponent.ai_level = Player.AI_LVL_OPEN_GAME
                # jdeme zahajovat
                self.state = Game.STATE_OPEN_GAME_OPEN
            # je stav zahájení open game?
            if self.state == Game.STATE_OPEN_GAME_OPEN:
                # další tah je právě sem
                next_move = self.board.best_move(self.players.active)
                # proveď ten tah
                self.board.make_move(self.players.active, next_move)
                # přepneme hráče
                self.players.next()
                og_moves -= 1
                if og_moves == 0:
                    self.state = Game.STATE_GAME_RUN
                    # vrátíme tam původní hodnoty
                    self.players = copy.deepcopy(players_backup)
            # zpracujeme eventy
            for event in pygame.event.get():
                # křížkem nebo zmáčknutím q je konec
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_q):
                    self.state = Game.STATE_QUIT
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    if self.gui.message_box(message = "Are you sure?") == True:
                        self.state = Game.STATE_QUIT
                # event GUI - zmáčkli jsme tlačítko myši
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    # pokud je to nová hra
                    if event.ui_element == self.gui.btn_new_game:
                        # a jsme v menu
                        if self.state == Game.STATE_MENU_MAIN:
                            # pustíme ji rovnou
                            self.run_new_game(Game.MODE_STANDARD)
                        else:
                            # jinak se zeptáme, jestli chce hru od začátku
                            if self.gui.message_box("Abandon this game and start again?") == True:
                                # Pokud ano, tak jedeme
                                self.run_new_game(Game.MODE_STANDARD)
                    # a je to open game
                    if event.ui_element == self.gui.btn_open_game:
                        # a jsme v menu
                        if self.state == Game.STATE_MENU_MAIN:
                            # pustíme ji rovnou
                            self.run_new_game(Game.MODE_OPEN_GAME)
                        else:
                            # jinak se zeptáme, jestli chce hru od začátku
                            if self.gui.message_box("Abandon this game and start again?") == True:
                                # Pokud ano, tak jedeme
                                self.run_new_game(Game.MODE_OPEN_GAME)
                    # a je to nastaveni
                    if event.ui_element == self.gui.btn_settings:
                        # lze pouze v menu nebo v game run
                        if self.state in (Game.STATE_MENU_MAIN, Game.STATE_GAME_RUN):
                            print("Settings")
                            # zakážeme hlavní menu
                            self.gui.ui_menu.disable()
                            # spustíme okno nastavení
                            if self.gui.menu_settings(self.players) == True:
                                # pokud vrátilo True, uložíme
                                self.players.save()
                            # povolíme hlavní menu
                            self.gui.ui_menu.enable()
                    # končíme?
                    if event.ui_element == self.gui.btn_quit:
                        if self.gui.message_box(message = "Are you sure?") == True:
                            self.state = Game.STATE_QUIT
                # ostatní GUI eventy
                self.gui.manager.process_events(event)
                # kliknutí myší hlavním tlačítkem
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # tah hráče
                    for r in range (self.board.rows):
                        for c in range(self.board.cols):
                            # kliknul na hrací desku?
                            if self.board.btns[r][c].collidepoint(pygame.mouse.get_pos()): # type: ignore
                                print("Klik na " + str(r) + ":" + str(c))
                                # jestli je tu prázdno
                                if self.board.grid[r][c] == Board.CELL_EMPTY:
                                    # pokud je hráč člověk a hra běží
                                    if self.players.active.type == Player.TYPE_HUMAN and self.state == Game.STATE_GAME_RUN:
                                        # tak řekneme desce, že táhnul tam kam kliknul
                                        self.board.make_move(self.players.active, (r, c))
                                        # konec zvýrazňování
                                        self.mark_coords = None
                                        # stav je konec tahu
                                        self.state = Game.STATE_GAME_END_MOVE

            # je hráč AI a hra běží?
            if self.players.active.type == Player.TYPE_AI and self.state == Game.STATE_GAME_RUN:
                # další tah je právě sem
                next_move = self.board.best_move(self.players.active)
                # proveď ten tah
                self.board.make_move(self.players.active, next_move)
                # zvýrazníme tento tah
                self.mark_coords = list()
                self.mark_coords.append(next_move)
                # stav je konec tahu
                self.state = Game.STATE_GAME_END_MOVE

            # vykreslíme hrací desku na kreslící plochu
            self.board.draw(self.gui.screen, self.players, self.mark_coords)
            # kreslíme všechno
            self.gui.draw(time_delta)

    def run_new_game(self, mode: int) -> None:
        """Inicializace nové hry."""
        self.mode = mode
        # začneme nové kolo
        self.run_new_round()
        # vymažeme skóre
        self.players.reset_win_count()
        # nastavíme skóre k vykreslování
        self.gui.lbl_score.set_text(self.players.score())

    def run_new_round(self) -> None:
        """Inicializace nového kola."""
        # resetujeme hráče a hrací desku do nastavení pro začátek hry
        self.players.reset()
        self.board.reset()
        # vymažeme označení
        self.mark_coords = None
        # přepneme do stavu běhu hry
        self.state = self.STATE_GAME_RUN
        # jsme v módu open game?
        if self.mode == Game.MODE_OPEN_GAME: 
            # tak nastavíme stav inicializace hry
            self.state = Game.STATE_OPEN_GAME_INIT
