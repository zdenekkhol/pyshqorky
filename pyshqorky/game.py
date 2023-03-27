import pygame
import pygame_gui
from players import *

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
    MODE_MENU_GAME = 3

    mode = MODE_MENU_MAIN
    FPS = 30 # maximální počet FPS

    def __init__(self):
        #self.mode = Game.MODE_MENU_MAIN
        pygame.init()
        pygame.display.set_caption("Pyshqorky")
        self.display = pygame.display.set_mode((800, 600))
        self.screen = pygame.Surface((800, 600))
        self.screen.fill(pygame.Color('#000000'))
        self.manager = pygame_gui.UIManager((800, 600))
        self.clock = pygame.time.Clock()

        #self.board = Board()
        self.players = Players({Players.PLAYER_1: Player(Players.PLAYER_1, "Player 1", (255,0,0), Player.TYPE_HUMAN), Players.PLAYER_2: Player(Players.PLAYER_2, "Player 2", (0,0,255), Player.TYPE_AI)})
        #self.active_player = 0

    def main(self):
        # vstupní bod po spuštění hry
        # nastavíme menu
        ui_menu = pygame_gui.elements.UIWindow(rect=pygame.Rect((0, 0), (200, 600)), manager=self.manager, window_display_title="Menu", draggable=False)
        ui_menu.close_window_button = False
        button_run = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 10), (100, 50)), text='Run', manager=self.manager, container=ui_menu, anchors={'centerx': 'centerx'})
        button_settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 60), (100, 50)), text="Settings", manager=self.manager, container=ui_menu, anchors={'centerx': 'centerx'})
        button_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 480), (100, 50)), text='Quit', manager=self.manager, container=ui_menu, anchors={'centerx': 'centerx'})
        """
        rows = cols = 15
        sqsize = 525 / 15
        btns = [[0 for col in range(cols)] for row in range(rows)]
        for r in range (rows):
            for c in range(cols):
                #btns[r][c] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((sqsize*r+22, sqsize*c+8), (sqsize, sqsize)), text="", manager=manager, container=ui_board)
                btns[r][c] = pygame.draw.rect(self.screen, (0x40,0x40,0x40), pygame.Rect(sqsize*r+235, sqsize*c+35, sqsize-1, sqsize-1))
        border = pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(205, 5, 585, 585), 30)
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
                    if event.ui_element == button_run:
                        print('Run!')
                    if event.ui_element == button_settings:
                        print("Settings")
                    if event.ui_element == button_quit:
                        self.mode = Game.MODE_QUIT
                # ostatní GUI eventy
                self.manager.process_events(event)
        
            self.manager.update(time_delta)
            self.display.blit(self.screen, (0, 0))
            self.manager.draw_ui(self.display)
            pygame.display.update()
    
    def run(self):
        pass