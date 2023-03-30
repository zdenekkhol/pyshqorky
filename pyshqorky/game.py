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
from pyshqorky.players import *
from pyshqorky.board import *

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
    #: Stav hry: Menu nastavení
    STATE_MENU_SETTINGS = 2
    #: Stav hry: Běh hry (tahu)
    STATE_GAME_RUN = 3
    #: Stav hry: Konec tahu
    STATE_GAME_END_TURN = 4

    def __init__(self):
        pygame.init()
        #: Stav hry. Na začátku se spouští do hlavního menu.
        self.state: int = self.STATE_MENU_MAIN
        #: Počet FPS pro běh hry = 30
        self.fps: int = 30 # maximální počet FPS
        #: Kde to zobrazujeme.
        self.display: pygame.Surface = pygame.display.set_mode((800, 600))
        #: Na co kreslíme.
        self.screen: pygame.Surface = pygame.Surface((800, 600))
        #: Manažer GUI rozhranní
        self.manager: pygame_gui.UIManager = pygame_gui.UIManager((800, 600))
        #: Hodiny pro sledování času hry
        self.clock: pygame.time.Clock = pygame.time.Clock()
        #: Seznam polí, která budou zvýrazněna (další tah počítače nebo výhra)
        self.mark_coords: list[tuple[int, int]] | None = None

        #: Hrací deska o velikosti 15x15 polí, 525x525 px, offset pro vykreslení do okna je 235x35 px
        self.board: Board = Board(15, 15, 525, 525, 235, 35)
        #: Seznam hráčů s implicitním nastavením.
        self.players: Players = Players({
            Players.PLAYER_1: Player(id=Players.PLAYER_1, name="Human", color=(255, 64, 64), shape=Player.SHAPE_SQUARE, type=Player.TYPE_HUMAN, ai_level=Player.AI_LVL_BALANCED), 
            Players.PLAYER_2: Player(id=Players.PLAYER_2, name="Computer", color=(64, 64, 255), shape=Player.SHAPE_CIRCLE, type=Player.TYPE_AI, ai_level=Player.AI_LVL_BALANCED)
            })

        # Pozadí je černě
        self.screen.fill(pygame.Color('#000000'))
        # A jmenuju se Pyshqorky
        pygame.display.set_caption("Pyshqorky")

        # Pokud jsme nedokázali nahrát uložené nastavení
        if Players.load() == None:
            # tak uložíme to aktuální jako základ
            self.players.save()
        else:
            # jinak hráče nastavíme podle uloženého souboru
            self.players = self.players.load()

    def main(self):
        """
        Vstupní bod po spuštění hry. Nastavení menu, hlavní smyčka hry a vykreslování.
        """
        # okno hlavního menu
        ui_menu = pygame_gui.elements.UIWindow(rect=pygame.Rect((0, 0), (200, 600)), manager=self.manager, window_display_title="Menu", draggable=False)
        # zneaktivnění křížku v menu, aby se nezavřelo
        ui_menu.close_window_button = None
        # definice tlačítek
        btn_run = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 10), (100, 50)), text='Run', manager=self.manager, container=ui_menu, anchors={'centerx': 'centerx'})
        btn_settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 60), (100, 50)), text="Settings", manager=self.manager, container=ui_menu, anchors={'centerx': 'centerx'})
        btn_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 480), (100, 50)), text='Quit', manager=self.manager, container=ui_menu, anchors={'centerx': 'centerx'})
        # label pro počet vítězství
        lbl_score = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((95, 0), (100, 30)),
                                    text=self.players.score(),
                                    manager=self.manager, anchors={'centerx': 'centerx'})

        # hlavní smyčka hry
        while self.state > Game.STATE_QUIT:
            # nastavení FPS + časová delta (dle dokumentace důležité pro GUI)
            time_delta = self.clock.tick(self.fps)/1000.0
            # zpracujeme eventy
            for event in pygame.event.get():
                # křížkem nebo zmáčknutím q je konec
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_q):
                    self.state = Game.STATE_QUIT
                # event GUI - zmáčkli jsme tlačítko myši
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    # spouštíme hru
                    if event.ui_element == btn_run:
                        print('Run!')
                        # přepneme do stavu běhu hry
                        self.state = self.STATE_GAME_RUN
                        # resetujeme hráče a hrací desku do nastavení pro začátek hry
                        self.players.reset()
                        self.board.reset()
                        self.mark_coords = None
                        # neumožníme znovuspustit hru, pokud běží
                        btn_run.disable()
                    # zobrazíme nastavení
                    if event.ui_element == btn_settings:
                        print("Settings")
                        # zakážeme hlavní menu
                        ui_menu.disable()
                        # spustíme okno nastavení
                        self.menu_settings()
                        # povolíme hlavní menu
                        ui_menu.enable()
                    # končíme?
                    if event.ui_element == btn_quit:
                        self.state = Game.STATE_QUIT
                # ostatní GUI eventy
                self.manager.process_events(event)
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
                                        self.state = Game.STATE_GAME_END_TURN

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
                self.state = Game.STATE_GAME_END_TURN

            # je stav konec tahu? vyhodnocení a přepnutí
            if self.state == Game.STATE_GAME_END_TURN:
                # co nám vrátí wintie?
                wt_state, to_mark = self.board.win_tie(self.players.active)
                # Není výhra, prohra ani remíza
                if wt_state == Board.WT_NONE:
                    # přepneme hráče
                    self.players.next()
                    # a hra jede dál
                    self.state = Game.STATE_GAME_RUN
                else:
                # A hle něco se děje, ale co?
                    match wt_state:
                        # Hráč zvítězil
                        case Board.WT_WINNER:
                            print("And The Winner is : " + self.players.active.name)
                            self.mark_coords = to_mark
                            self.players.active.wins()
                        # Hráč prohrál
                        case Board.WT_LOSER:
                            print("And The Winner is : " + self.players.oponent.name)
                            self.mark_coords = to_mark
                            self.players.oponent.wins()
                        # Remíza - ani jeden jedokáže udělat na tomto boardu žádnou pětku
                        case Board.WT_TIE:
                            print("Remíza hoši")
                    # Aktualizace skóre
                    #lbl_score.text = self.players.score()
                    lbl_score.set_text(self.players.score())
                    # Povolíme spustit další hru
                    btn_run.enable()
                    # a stav je hlavní menu
                    self.state = Game.STATE_MENU_MAIN

            # vykreslíme hrací desku na kreslící plochu
            self.board.draw(self.screen, self.players, self.mark_coords)

            # vykreslíme GUI (podle dokumentace a testů musí být právě tady, aby fungovalo správně)
            self.manager.update(time_delta)
            self.display.blit(self.screen, (0, 0))
            self.manager.draw_ui(self.display)

            # tohle s GUI nefunguje
            #pygame.transform.scale(self.screen, self.display.get_size(), self.display)
            
            # provedeme update dipleje
            pygame.display.update()

    def menu_settings(self):
        """
        Vykreslení a obsluha menu nastavení
        """
        # uložíme si aktuální mód hry
        prev_mode = self.state
        # a nahodíme stav menu nastavení
        self.state = Game.STATE_MENU_SETTINGS
        # kam se začíné kreslit menu nastavení pro hráče 1 a 2 
        player1_y = 10
        player2_y = 210

        # vytvoříme okno menu nastavení
        ui_settings = pygame_gui.elements.UIWindow(rect=pygame.Rect((30, 30), (300, 560)), manager=self.manager, window_display_title="Settings", draggable=False)
        #ui_settings.close_window_button = None
        # tlačítko pro uložení
        btn_save = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 440), (100, 50)), text='Save', manager=self.manager, container=ui_settings, anchors={'centerx': 'centerx'})

        # menu pro hráče 1
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
        # menu pro hráče 2
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


        # hlavní obslužná smyčka - dokud jsme ve stavu menu nastavení
        while self.state == Game.STATE_MENU_SETTINGS:
            # nastavení FPS + časová delta (dle dokumentace důležité pro GUI)
            time_delta = self.clock.tick(self.fps)/1000.0
            # zpracujeme eventy
            for event in pygame.event.get():
                # odchod bez uložení = ESC
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    self.state = prev_mode
                # eventy GUI - zmáčkli jsme tlačítko
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    # a je to save (kupodivu)
                    if event.ui_element == btn_save:
                        print('Save!')
                        # nastavíme hráče podle toho, co uživatel zvolil
                        self.players.get(Players.PLAYER_1).name = tb_name1.text # type: ignore
                        self.players.get(Players.PLAYER_2).name = tb_name2.text # type: ignore
                        self.players.get(Players.PLAYER_1).shape = Player.shape_list.index(dd_shape1.selected_option) # type: ignore
                        self.players.get(Players.PLAYER_2).shape = Player.shape_list.index(dd_shape2.selected_option) # type: ignore
                        self.players.get(Players.PLAYER_1).type = Player.type_list.index(dd_type1.selected_option) # type: ignore
                        self.players.get(Players.PLAYER_2).type = Player.type_list.index(dd_type2.selected_option) # type: ignore
                        self.players.get(Players.PLAYER_1).ai_level = Player.ai_level_list.index(dd_ailevel1.selected_option) # type: ignore
                        self.players.get(Players.PLAYER_2).ai_level = Player.ai_level_list.index(dd_ailevel2.selected_option) # type: ignore
                        # uložíme do souboru pro perzistentní uchování
                        self.players.save()
                        # vrátíme se do předchozího módu
                        self.state = prev_mode
                # křížek pro zavření menu = návrat bez uložení
                if event.type == pygame_gui.UI_WINDOW_CLOSE:
                    self.state = prev_mode
                # tyhle GUI eventy nakonec není třeba obsluhovat
                if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                    pass
                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    pass

                # ostatní GUI eventy
                self.manager.process_events(event)
    
            # vykreslíme GUI (podle dokumentace a testů musí být právě tady, aby fungovalo správně)
            self.manager.update(time_delta)
            self.display.blit(self.screen, (0, 0))
            self.manager.draw_ui(self.display)
            # provedeme update displeje
            pygame.display.update()

        # na konci před odchodem skryjeme menu nastavení
        ui_settings.hide()
