import numpy as np
import random

class snake():
    def __init__(self, gamesize = 8):

        self.gamesize = gamesize
        self.grid = np.zeros((self.gamesize, self.gamesize))
        self.snake = []
        self.direction = 3 # 0 cima, 1 baixo, 2 esquerda, 3 direita
        self.gameOver = False
        self.food = np.array([None, None])
        self.score = 0


    def _vectorDirection(self):
        if self.direction == 0:
            return np.array([0,1])
        elif self.direction == 1:
            return np.array([0,-1])
        elif self.direction == 2:
            return np.array([-1,0])
        else:
            return np.array([1,0])
    
    def _move(self):
        self.snake.insert(self.snake[0] + self._vectorDirection())
        if self._colision():
            self.gameOver = True
        if self._food():
            pass
        else:
            self.snake.pop()

    def _food(self):
        if self.food == self.snake:
            self._generateFood()
            return True

            
    def _generateFood(self):
        x = random.randint(0, self.gamesize)
        y = random.randint(0, self.gamesize)
        if np.array(x,y) in self.snake:
            self._generateFood()

    def show(self):
        print(self.grid)

    def _colision(self):

        if self.snake[0][0] < 0 or self.snake[0][0] > self.gamesize or self.snake[0][1] < 0 or self.snake[0][1] > self.gamesize:
            return True
        elif self.snake[0] in self.snake[1:]:
            return True
        return False

    
    def game(self):
        self._generateFood()
        while not self.gameOver:
            self.direction = int(input("Teste"))
            self._move()
            self.show()

if __name__ == "__main__":
    snake.game()