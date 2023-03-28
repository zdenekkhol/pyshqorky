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
            Players.PLAYER_1: Player(id=Players.PLAYER_1, name="Human", color=(255, 64, 64), shape=Player.SHAPE_SQUARE, type=Player.TYPE_HUMAN, ai_level=Player.AI_LVL_BALANCED), 
            Players.PLAYER_2: Player(id=Players.PLAYER_2, name="Computer", color=(64, 64, 255), shape=Player.SHAPE_CIRCLE, type=Player.TYPE_AI, ai_level=Player.AI_LVL_BALANCED)})

        if Players.load() == None:
            self.players.save()
        else:
            self.players = self.players.load()

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
                        ui_menu.disable()
                        self.menu_settings()
                        ui_menu.enable()
                    if event.ui_element == btn_quit:
                        self.mode = Game.MODE_QUIT
                # ostatní GUI eventy
                self.manager.process_events(event)
                # kliknutí myší
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # tah hráče
                    for r in range (self.board.rows):
                        for c in range(self.board.cols):
                            if self.board.btns[r][c].collidepoint(pygame.mouse.get_pos()): # type: ignore
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
        player1_y = 10
        player2_y = 210

        self.mode = Game.MODE_MENU_SETTINGS
        # vytvoříme menu
        ui_settings = pygame_gui.elements.UIWindow(rect=pygame.Rect((30, 30), (300, 560)), manager=self.manager, window_display_title="Settings", draggable=False)
        ui_settings.close_window_button = None
        btn_save = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 440), (100, 50)), text='Save', manager=self.manager, container=ui_settings, anchors={'centerx': 'centerx'})

        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player1_y), (100, 50)), text='Player 1',
                                    manager=self.manager, container=ui_settings, anchors={'centerx': 'centerx'})
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player1_y+40), (100, 40)), text='Name:',
                                    manager=self.manager, container=ui_settings, anchors={'left': 'left'})
        tb_name1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((-160, player1_y+40), (150, 40)), initial_text=self.players.get(Players.PLAYER_1).name, #type: ignore
                                                       manager=self.manager, container=ui_settings, anchors={'right': 'right'}) #type: ignore
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player1_y+80), (100, 40)), text='Type:', manager=self.manager, container=ui_settings, anchors={'left': 'left'})
        dd_type1 = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((-160, player1_y+80), (150, 40)), options_list=Player.type_list, #type: ignore
                                                      starting_option=Player.type_list[self.players.get(Players.PLAYER_1).type], #type: ignore
                                                      manager=self.manager, container=ui_settings, anchors={'right': 'right'})
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player1_y+120), (100, 40)), text='Shape:', manager=self.manager, container=ui_settings, anchors={'left': 'left'})
        dd_shape1 = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((-160, player1_y+120), (150, 40)), options_list=Player.shape_list, #type: ignore
                                                      starting_option=Player.shape_list[self.players.get(Players.PLAYER_1).shape], #type: ignore
                                                      manager=self.manager, container=ui_settings, anchors={'right': 'right'})
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player1_y+160), (100, 40)), text='AI Level:', manager=self.manager, container=ui_settings, anchors={'left': 'left'})
        dd_ailevel1 = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((-160, player1_y+160), (150, 40)), options_list=Player.ai_level_list, #type: ignore
                                                      starting_option=Player.ai_level_list[self.players.get(Players.PLAYER_1).ai_level], #type: ignore
                                                      manager=self.manager, container=ui_settings, anchors={'right': 'right'})

        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player2_y+0), (100, 50)), text='Player 2', manager=self.manager, container=ui_settings, anchors={'centerx': 'centerx'})
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player2_y+40), (100, 40)), text='Name:', manager=self.manager, container=ui_settings, anchors={'left': 'left'})
        tb_name2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((-160, player2_y+40), (150, 40)), initial_text=self.players.get(Players.PLAYER_2).name, #type: ignore
                                                       manager=self.manager, container=ui_settings, anchors={'right': 'right'}) #type: ignore
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player2_y+80), (100, 40)), text='Type:', manager=self.manager, container=ui_settings, anchors={'left': 'left'})
        dd_type2 = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((-160, player2_y+80), (150, 40)), options_list=Player.type_list, #type: ignore
                                                      starting_option=Player.type_list[self.players.get(Players.PLAYER_2).type], #type: ignore
                                                      manager=self.manager, container=ui_settings, anchors={'right': 'right'})
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player2_y+120), (100, 40)), text='Shape:', manager=self.manager, container=ui_settings, anchors={'left': 'left'})
        dd_shape2 = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((-160, player2_y+120), (150, 40)), options_list=Player.shape_list, #type: ignore
                                                      starting_option=Player.shape_list[self.players.get(Players.PLAYER_2).shape], #type: ignore
                                                      manager=self.manager, container=ui_settings, anchors={'right': 'right'})
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player2_y+160), (100, 40)), text='AI Level:', manager=self.manager, container=ui_settings, anchors={'left': 'left'})
        dd_ailevel2 = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((-160, player2_y+160), (150, 40)), options_list=Player.ai_level_list, #type: ignore
                                                      starting_option=Player.ai_level_list[self.players.get(Players.PLAYER_2).ai_level], #type: ignore
                                                      manager=self.manager, container=ui_settings, anchors={'right': 'right'})


        while self.mode == Game.MODE_MENU_SETTINGS:
            time_delta = self.clock.tick(self.FPS)/1000.0
            # zpracujeme eventy
            for event in pygame.event.get():
                # odchod bez uložení ESC
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    self.mode = prev_mode
                # eventy GUI
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == btn_save:
                        print('Save!')
                        self.players.get(Players.PLAYER_1).name = tb_name1.text # type: ignore
                        self.players.get(Players.PLAYER_2).name = tb_name2.text # type: ignore
                        self.players.get(Players.PLAYER_1).shape = Player.shape_list.index(dd_shape1.selected_option) # type: ignore
                        self.players.get(Players.PLAYER_2).shape = Player.shape_list.index(dd_shape2.selected_option) # type: ignore
                        self.players.get(Players.PLAYER_1).type = Player.type_list.index(dd_type1.selected_option) # type: ignore
                        self.players.get(Players.PLAYER_2).type = Player.type_list.index(dd_type2.selected_option) # type: ignore
                        self.players.get(Players.PLAYER_1).ai_level = Player.ai_level_list.index(dd_ailevel1.selected_option) # type: ignore
                        self.players.get(Players.PLAYER_2).ai_level = Player.ai_level_list.index(dd_ailevel2.selected_option) # type: ignore
                        self.players.save()
                        self.mode = prev_mode
                if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                    pass
                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    pass

                # ostatní GUI eventy
                self.manager.process_events(event)
    
            self.manager.update(time_delta)
            self.display.blit(self.screen, (0, 0))
            self.manager.draw_ui(self.display)
            pygame.display.update()

        ui_settings.hide()
