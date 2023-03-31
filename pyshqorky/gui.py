import pygame
import pygame_gui
from  pyshqorky.players import *

class GUI:
    def __init__(self) -> None:
        pygame.init()
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
        # Pozadí je černě
        self.screen.fill(pygame.Color('#000000'))

        # okno hlavního menu
        self.ui_menu = pygame_gui.elements.UIWindow(rect=pygame.Rect((0, 0), (200, 600)), manager=self.manager, window_display_title="Menu", draggable=False)
        # zneaktivnění křížku v menu, aby se nezavřelo
        self.ui_menu.close_window_button = None
        # definice tlačítek
        self.btn_run = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 10), (100, 50)), text='New game', manager=self.manager, container=self.ui_menu, anchors={'centerx': 'centerx'})
        self.btn_settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 60), (100, 50)), text="Settings", manager=self.manager, container=self.ui_menu, anchors={'centerx': 'centerx'})
        self.btn_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 480), (100, 50)), text='Quit', manager=self.manager, container=self.ui_menu, anchors={'centerx': 'centerx'})
        # label pro počet vítězství
        self.lbl_score = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((95, 0), (100, 30)),
                                    text="",
                                    manager=self.manager, anchors={'centerx': 'centerx'})
        
    def time_delta(self) -> float:
        """Vypočítání time_delta pro pygame_gui"""
        # nastavení FPS + časová delta (dle dokumentace důležité pro GUI)
        return self.clock.tick(self.fps)/1000.0

    def draw(self, delta: float) -> None:
        """Vykreslení GUI, okna a update displeje"""
        # vykreslíme GUI (podle dokumentace a testů musí být právě tady, aby fungovalo správně)
        self.manager.update(delta)
        self.display.blit(self.screen, (0, 0))
        self.manager.draw_ui(self.display)
        # tohle s GUI nefunguje
        #pygame.transform.scale(self.screen, self.display.get_size(), self.display)
        # provedeme update displeje
        pygame.display.update()

    def menu_settings(self, players: Players) -> None:
        """
        Vykreslení a obsluha menu nastavení. Pokud se má uložit právě nastavené, vrací True, jiank False
        """
        run = True
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
        tb_name1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((-160, player1_y+40), (150, 40)), initial_text=players.get(Players.PLAYER_1).name, #type: ignore
                                                       manager=self.manager, container=ui_settings, anchors={'right': 'right'}) #type: ignore
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player1_y+80), (100, 40)), text='Type:', manager=self.manager, container=ui_settings, anchors={'left': 'left'})
        dd_type1 = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((-160, player1_y+80), (150, 40)), options_list=Player.type_list, #type: ignore
                                                      starting_option=Player.type_list[players.get(Players.PLAYER_1).type], #type: ignore
                                                      manager=self.manager, container=ui_settings, anchors={'right': 'right'})
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player1_y+120), (100, 40)), text='Shape:', manager=self.manager, container=ui_settings, anchors={'left': 'left'})
        dd_shape1 = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((-160, player1_y+120), (150, 40)), options_list=Player.shape_list, #type: ignore
                                                      starting_option=Player.shape_list[players.get(Players.PLAYER_1).shape], #type: ignore
                                                      manager=self.manager, container=ui_settings, anchors={'right': 'right'})
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player1_y+160), (100, 40)), text='AI Level:', manager=self.manager, container=ui_settings, anchors={'left': 'left'})
        dd_ailevel1 = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((-160, player1_y+160), (150, 40)), options_list=Player.ai_level_list, #type: ignore
                                                      starting_option=Player.ai_level_list[players.get(Players.PLAYER_1).ai_level], #type: ignore
                                                      manager=self.manager, container=ui_settings, anchors={'right': 'right'})
        # menu pro hráče 2
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player2_y+0), (100, 50)), text='Player 2', manager=self.manager, container=ui_settings, anchors={'centerx': 'centerx'})
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player2_y+40), (100, 40)), text='Name:', manager=self.manager, container=ui_settings, anchors={'left': 'left'})
        tb_name2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((-160, player2_y+40), (150, 40)), initial_text=players.get(Players.PLAYER_2).name, #type: ignore
                                                       manager=self.manager, container=ui_settings, anchors={'right': 'right'}) #type: ignore
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player2_y+80), (100, 40)), text='Type:', manager=self.manager, container=ui_settings, anchors={'left': 'left'})
        dd_type2 = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((-160, player2_y+80), (150, 40)), options_list=Player.type_list, #type: ignore
                                                      starting_option=Player.type_list[players.get(Players.PLAYER_2).type], #type: ignore
                                                      manager=self.manager, container=ui_settings, anchors={'right': 'right'})
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player2_y+120), (100, 40)), text='Shape:', manager=self.manager, container=ui_settings, anchors={'left': 'left'})
        dd_shape2 = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((-160, player2_y+120), (150, 40)), options_list=Player.shape_list, #type: ignore
                                                      starting_option=Player.shape_list[players.get(Players.PLAYER_2).shape], #type: ignore
                                                      manager=self.manager, container=ui_settings, anchors={'right': 'right'})
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, player2_y+160), (100, 40)), text='AI Level:', manager=self.manager, container=ui_settings, anchors={'left': 'left'})
        dd_ailevel2 = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((-160, player2_y+160), (150, 40)), options_list=Player.ai_level_list, #type: ignore
                                                      starting_option=Player.ai_level_list[players.get(Players.PLAYER_2).ai_level], #type: ignore
                                                      manager=self.manager, container=ui_settings, anchors={'right': 'right'})


        # hlavní obslužná smyčka - dokud jsme ve stavu menu nastavení
        while run:
            # nastavení FPS + časová delta (dle dokumentace důležité pro GUI)
            time_delta = self.time_delta()
            # zpracujeme eventy
            for event in pygame.event.get():
                # odchod bez uložení = ESC
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    run = False
                # eventy GUI - zmáčknul jsem tlačítko
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    # a je to save (kupodivu)
                    if event.ui_element == btn_save:
                        print('Save!')
                        # nastavíme hráče podle toho, co uživatel zvolil
                        players.get(Players.PLAYER_1).name = tb_name1.text # type: ignore
                        players.get(Players.PLAYER_2).name = tb_name2.text # type: ignore
                        players.get(Players.PLAYER_1).shape = Player.shape_list.index(dd_shape1.selected_option) # type: ignore
                        players.get(Players.PLAYER_2).shape = Player.shape_list.index(dd_shape2.selected_option) # type: ignore
                        players.get(Players.PLAYER_1).type = Player.type_list.index(dd_type1.selected_option) # type: ignore
                        players.get(Players.PLAYER_2).type = Player.type_list.index(dd_type2.selected_option) # type: ignore
                        players.get(Players.PLAYER_1).ai_level = Player.ai_level_list.index(dd_ailevel1.selected_option) # type: ignore
                        players.get(Players.PLAYER_2).ai_level = Player.ai_level_list.index(dd_ailevel2.selected_option) # type: ignore
                        # uložíme do souboru pro perzistentní uchování
                        players.save()
                        # vrátíme se do předchozího módu
                        run = False
                # GUI - křížek pro zavření menu = návrat bez uložení
                if event.type == pygame_gui.UI_WINDOW_CLOSE:
                    run = False
                # ostatní GUI eventy
                self.manager.process_events(event)
    
            # vykreslíme GUI (podle dokumentace a testů musí být právě tady, aby fungovalo správně)
            self.draw(time_delta)

        # na konci před odchodem skryjeme menu nastavení
        ui_settings.hide()

    def message_box(self, message: str, title: str = "Warning", position: tuple[int, int] = (0, 0),
                    size: tuple[int, int] = (300, 100)) -> bool:
        """
        Modální dialogové okno pro upozornění nebo otázku s odpovědí OK / Cancel
        """
        run = True
        ret = False
        # Vytvoříme modální dialog
        cdialog = pygame_gui.windows.UIConfirmationDialog(rect=pygame.Rect(position, size),
                    action_long_desc=message, manager=self.manager, window_title=title, blocking=True, )
        while run:
            # nastavení FPS + časová delta (dle dokumentace důležité pro GUI)
            time_delta = self.time_delta()
            # zpracujeme eventy
            for event in pygame.event.get():
                print("event: " + str(event.type))
                # ESC = jako Cancel
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    ret = False
                    run = False
                # eventy GUI - co se nás týká
                if cdialog.process_event(event) == True:
                    # zmáčkli jsme confirm
                    if cdialog.confirm_button.hovered:
                        print("zmackli jsme confirm")
                        ret = True
                        run = False
                    # zmáčkli jame cancel nebo zavřít okno
                    if cdialog.cancel_button.hovered or cdialog.close_window_button.hovered: #type: ignore
                        print("cancel")
                        ret = False
                        run = False
                    
            # vykreslíme GUI (podle dokumentace a testů musí být právě tady, aby fungovalo správně)
            self.draw(time_delta)

        cdialog.hide()
        return ret    