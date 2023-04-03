import unittest
from pyshqorky.board import *
#from pyshqorky.players import *

class Board_test(unittest.TestCase):
    def test_score_wnd5(self):
        board = Board(15, 15, 600, 600, 0, 0)
        players: Players = Players({
            Players.PLAYER_1: Player(id=Players.PLAYER_1, name="Human", color=(255, 64, 64), shape=Player.SHAPE_SQUARE, type=Player.TYPE_HUMAN, ai_level=Player.AI_LVL_BALANCED), 
            Players.PLAYER_2: Player(id=Players.PLAYER_2, name="Computer", color=(64, 64, 255), shape=Player.SHAPE_CIRCLE, type=Player.TYPE_AI, ai_level=Player.AI_LVL_BALANCED)
            })
        self.assertEqual(board.score_wnd5([0,0,0,0,0], players.active), 0)
        self.assertEqual(board.score_wnd5([0,1,-1,0,0], players.active), 0)
        self.assertEqual(board.score_wnd5([1,0,1,1,1], players.active),
                         Player.AI_VALUES[players.active.ai_level][Player.AI_SCORE_MY][4])
        self.assertEqual(board.score_wnd5([0,-1,-1,-1,0], players.active),
                         -Player.AI_VALUES[players.active.ai_level][Player.AI_SCORE_OPONENT][3])

    def test_score_board(self):
        board = Board(15, 15, 600, 600, 0, 0)
        players: Players = Players({
            Players.PLAYER_1: Player(id=Players.PLAYER_1, name="Human", color=(255, 64, 64), shape=Player.SHAPE_SQUARE, type=Player.TYPE_HUMAN, ai_level=Player.AI_LVL_BALANCED), 
            Players.PLAYER_2: Player(id=Players.PLAYER_2, name="Computer", color=(64, 64, 255), shape=Player.SHAPE_CIRCLE, type=Player.TYPE_AI, ai_level=Player.AI_LVL_BALANCED)
            })
        self.assertEqual(board.score_board(players.active), 0)
        board.make_move(players.active, (0,0))
        self.assertEqual(board.score_board(players.active), 
                         3*Player.AI_VALUES[players.active.ai_level][Player.AI_SCORE_MY][1])
        board.reset()
        board.make_move(players.active, (5,5))
        self.assertEqual(board.score_board(players.active), 
                         (5+5+5+5)*Player.AI_VALUES[players.active.ai_level][Player.AI_SCORE_MY][1])
        players.next()
        self.assertEqual(board.score_board(players.active), 
                         -(5+5+5+5)*Player.AI_VALUES[players.active.ai_level][Player.AI_SCORE_OPONENT][1])
        board.reset()
        board.make_move(players.active, (5,5))
        board.make_move(players.active, (5,6))
        self.assertEqual(board.score_board(players.active), 
                         ((2+10+10+10)*Player.AI_VALUES[players.active.ai_level][Player.AI_SCORE_MY][1])
                         +((4+0+0+0)*Player.AI_VALUES[players.active.ai_level][Player.AI_SCORE_MY][2]))
        board.reset()
        board.make_move(players.active, (5,5))
        board.make_move(players.active, (6,5))
        self.assertEqual(board.score_board(players.active), 
                         ((2+10+10+10)*Player.AI_VALUES[players.active.ai_level][Player.AI_SCORE_MY][1])
                         +((4+0+0+0)*Player.AI_VALUES[players.active.ai_level][Player.AI_SCORE_MY][2]))
        board.reset()
        board.make_move(players.active, (5,5))
        board.make_move(players.active, (6,6))
        self.assertEqual(board.score_board(players.active), 
                         ((2+10+10+10)*Player.AI_VALUES[players.active.ai_level][Player.AI_SCORE_MY][1])
                         +((4+0+0+0)*Player.AI_VALUES[players.active.ai_level][Player.AI_SCORE_MY][2]))
        board.reset()
        board.make_move(players.active, (5,6))
        board.make_move(players.active, (6,5))
        self.assertEqual(board.score_board(players.active), 
                         ((2+10+10+10)*Player.AI_VALUES[players.active.ai_level][Player.AI_SCORE_MY][1])
                         +((4+0+0+0)*Player.AI_VALUES[players.active.ai_level][Player.AI_SCORE_MY][2]))

    def test_make_move(self):
        board = Board(15, 15, 600, 600, 0, 0)
        players: Players = Players({
            Players.PLAYER_1: Player(id=Players.PLAYER_1, name="Human", color=(255, 64, 64), shape=Player.SHAPE_SQUARE, type=Player.TYPE_HUMAN, ai_level=Player.AI_LVL_BALANCED), 
            Players.PLAYER_2: Player(id=Players.PLAYER_2, name="Computer", color=(64, 64, 255), shape=Player.SHAPE_CIRCLE, type=Player.TYPE_AI, ai_level=Player.AI_LVL_BALANCED)
            })
        self.assertEqual(board.grid[5][5], Board.CELL_EMPTY)
        board.make_move(players.active, (5,5))
        self.assertEqual(board.grid[5][5], players.active.id)

    def test_reset(self):
        board = Board(15, 15, 600, 600, 0, 0)
        players: Players = Players({
            Players.PLAYER_1: Player(id=Players.PLAYER_1, name="Human", color=(255, 64, 64), shape=Player.SHAPE_SQUARE, type=Player.TYPE_HUMAN, ai_level=Player.AI_LVL_BALANCED), 
            Players.PLAYER_2: Player(id=Players.PLAYER_2, name="Computer", color=(64, 64, 255), shape=Player.SHAPE_CIRCLE, type=Player.TYPE_AI, ai_level=Player.AI_LVL_BALANCED)
            })
        board.make_move(players.active, (5,5))
        board.reset()
        self.assertEqual(board.grid[5][5], Board.CELL_EMPTY)

if __name__ == '__main__':
    unittest.main()