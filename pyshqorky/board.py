import pygame
from players import *

"""
class Board
- grid
* reset
* draw
* score - z pohledu hráče
* score_5
* wintie - globálně, 0 = jedeme dál, 1/-1 win hráč, jinak = tie
* wintie_5
"""

class Board:
    def __init__(self, rows, cols, width, height, players):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.square_size = width // cols
        self.grid = [[0 for col in range(self.cols)] for row in range(self.rows)]
        self.players = players

    def draw(self, screen):
        # vykreslení herní plochy
        for row in range(self.rows):
            for col in range(self.cols):
                color = (255, 255, 255)
                for pl in self.players:
                    if self.grid[row][col] == pl.id:
                        color = pl.color
                pygame.draw.rect(screen, (0,0,0), (col*self.square_size, row*self.square_size, self.square_size, self.square_size), 1)
                pygame.draw.circle(screen, color, (col*self.square_size+self.square_size//2, row*self.square_size+self.square_size//2), self.square_size//2-5)
