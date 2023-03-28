import pygame
import pygame_gui
from pyshqorky.players import *
from pyshqorky.board import *

"""
class Game
- running
- mode - menumain, menusettings, run
- active_player
* menu_main
* menu_settings
* main
"""
class Game:
    MODE_QUIT = 0
    MODE_MENU_MAIN = 1
    MODE_MENU_SETTINGS = 2
    MODE_GAME_RUN = 3
    MODE_GAME_END_TURN = 4

    def __init__(self):
        self.mode = self.MODE_MENU_MAIN
        self.FPS = 30 # maximální počet FPS
        pygame.init()
        pygame.display.set_caption("Pyshqorky")
        self.display = pygame.display.set_mode((800, 600))
        self.screen = pygame.Surface((800, 600))
        self.screen.fill(pygame.Color('#000000'))
        self.manager = pygame_gui.UIManager((800, 600))
        self.clock = pygame.time.Clock()

        self.board = Board(15, 15, 525, 525, 235, 35)
        self.players = Players({
            Players.PLAYER_1: Player(Players.PLAYER_1, "Player 1", (255, 64, 64), Player.TYPE_HUMAN), 
            Players.PLAYER_2: Player(Players.PLAYER_2, "Player 2", (64, 64, 255), Player.TYPE_AI)})
        #self.active_player = 0

    def main(self):
        # vstupní bod po spuštění hry
        # nastavíme menu
        ui_menu = pygame_gui.elements.UIWindow(rect=pygame.Rect((0, 0), (200, 600)), manager=self.manager, window_display_title="Menu", draggable=False)
        ui_menu.close_window_button = None
        btn_run = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 10), (100, 50)), text='Run', manager=self.manager, container=ui_menu, anchors={'centerx': 'centerx'})
        btn_settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 60), (100, 50)), text="Settings", manager=self.manager, container=ui_menu, anchors={'centerx': 'centerx'})
        btn_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 480), (100, 50)), text='Quit', manager=self.manager, container=ui_menu, anchors={'centerx': 'centerx'})
        self.board.draw(self.screen, self.players)

        """
        # vyzkoušíme pár tahů
        for i in range (2):
            self.board.make_move(self.players[self.players.active.id], self.board.best_move(self.players[self.players.active.id]))
            self.players.next()
            self.board.draw(self.screen, self.players)
            self.display.blit(self.screen, (0, 0))
        """

        while self.mode > Game.MODE_QUIT:
            time_delta = self.clock.tick(self.FPS)/1000.0
            # zpracujeme eventy
            for event in pygame.event.get():
                # křížkem nebo zmáčknutím q je konec
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_q):
                    self.mode = Game.MODE_QUIT
                # eventy GUI
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == btn_run:
                        print('Run!')
                        self.mode = self.MODE_GAME_RUN
                        self.players.reset()
                        self.board.reset()
                        self.board.draw(self.screen, self.players)
                        btn_run.disable()
                    if event.ui_element == btn_settings:
                        print("Settings")
                    if event.ui_element == btn_quit:
                        self.mode = Game.MODE_QUIT
                # ostatní GUI eventy
                self.manager.process_events(event)
                # kliknutí myší
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # tah hráče
                    for r in range (self.board.rows):
                        for c in range(self.board.cols):
                            if self.board.btns[r][c].collidepoint(pygame.mouse.get_pos()):
                                print("Klik na " + str(r) + ":" + str(c))
                                if self.board.grid[r][c] == Board.EMPTY:
                                    if self.players.active.type == Player.TYPE_HUMAN and self.mode == Game.MODE_GAME_RUN:
                                        self.board.make_move(self.players.active, (r, c))
                                        self.mode = Game.MODE_GAME_END_TURN

            # tah AI?
            if self.players.active.type == Player.TYPE_AI and self.mode == Game.MODE_GAME_RUN:
                next_move = self.board.best_move(self.players.active)
                self.board.make_move(self.players.active, next_move)
                self.mode = Game.MODE_GAME_END_TURN

            # vyhodnocení a přepnutí
            if self.mode == Game.MODE_GAME_END_TURN:
                # jedeme dál
                if self.board.win_tie(self.players.active) == Board.WT_NONE:
                    self.players.next()
                    self.mode = Game.MODE_GAME_RUN
                else:
                # hle něco se děje, ale co?
                    match self.board.win_tie(self.players.active):
                        case Board.WT_WINNER:
                            print("And The Winner is : " + self.players.active.name)
                        case Board.WT_LOSER:
                            print("And The Winner is : " + self.players.oponent.name)
                        case Board.WT_TIE:
                            print("Remíza hoši")
                    # vracíme se zpět do menu
                    btn_run.enable()
                    self.mode = Game.MODE_MENU_MAIN

            self.board.draw(self.screen, self.players)

            self.manager.update(time_delta)
            self.display.blit(self.screen, (0, 0))
            self.manager.draw_ui(self.display)
            pygame.display.update()
    
    def menu_settings(self):
        prev_mode = self.mode
        self.mode = Game.MODE_MENU_SETTINGS
        # vytvoříme menu
        ui_settings = pygame_gui.elements.UIWindow(rect=pygame.Rect((30, 30), (200, 500)), manager=self.manager, window_display_title="Menu", draggable=False)
        ui_settings.close_window_button = None
        btn_save = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 400), (100, 50)), text='Save', manager=self.manager, container=ui_settings, anchors={'centerx': 'centerx'})

        while self.mode == Game.MODE_MENU_SETTINGS:
            time_delta = self.clock.tick(self.FPS)/1000.0
            # zpracujeme eventy
            for event in pygame.event.get():
                # eventy GUI
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == btn_save:
                        print('Save!')
                        self.mode = prev_mode
                # ostatní GUI eventy
                self.manager.process_events(event)
    
        print('Ukládám...')
