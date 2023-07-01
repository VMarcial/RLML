import numpy as np
import random
from rlml import agent
import matplotlib.pyplot as plt
from tqdm import tqdm


class snake():
    def __init__(self, gamesize = 8):

        self.gamesize = gamesize
        self.grid = np.zeros((self.gamesize, self.gamesize))
        self.snake = [np.array([gamesize//2, gamesize//2]), np.array([(gamesize//2)-1,(gamesize//2) ])]
        self.direction = 3 # 0 cima, 1 baixo, 2 esquerda, 3 direita
        self.gameOver = False
        self.food = np.array([None, None])
        self.score = 0
        self.reward = 0
        self.remaningMoves = gamesize * gamesize
        self._generateFood()
        self._updateGrid()


    def _vectorDirection(self):
        #converte int em um vetor de direção
        if self.direction == 0:
            return np.array([0,1])
        elif self.direction == 1:
            return np.array([0,-1])
        elif self.direction == 2:
            return np.array([-1,0])
        elif self.direction == 3:
            return np.array([1,0])
        else:
            print("algo deu errado")
    
    def _move(self):
        #movimento da cobra, checa se comeu comida e recompensa por isso
        self.snake.insert(0, self.snake[0] + self._vectorDirection())
        if self._colision():
            self.gameOver = True
            return False
        if self._food():
            self.reward += 10
            self.score += 1
            self.remaningMoves += ((gamesize * gamesize)//4)
            pass
        else:
            self.snake.pop()
        return True

    def _food(self):
        #verifica se a cobra comeu a comida
        if self.food[0] == self.snake[0][0] and self.food[1] == self.snake[0][1]:
            self._generateFood()
            return True

    def _updateGrid(self):
        # coloca no grid 
        temp = np.zeros((self.gamesize, self.gamesize))
        for position in self.snake:
            temp[position[0]][position[1]] = -1
        temp[self.food[0]][self.food[1]] = 1

        self.grid = temp
    
    def getState(self):
        #temp = self.grid.flatten()
        #return temp

        flat = self.grid.flatten()
        head = self.snake[0]

        #distancia até as paredes
        dx1 = head[0]
        dx2 = gamesize - head[0]
        dy1 = head[1]
        dy2 = gamesize - head[1]

        #distancia até a comida
        df1 = self.food[0] - head[0]
        df2 = self.food[1] - head[1]

        signals = np.array([dx1,dx2,dy1,dy2,df1,df2])

        temp = np.concatenate((flat, signals), axis = 0)

        return temp

            
    def _generateFood(self):
        # cria comida no mapa
        x = random.randint(0, self.gamesize - 1)
        y = random.randint(0, self.gamesize - 1)
        is_in_list = np.any(np.all(np.array([x,y]) == self.snake, axis=1))
        if is_in_list: 
            self._generateFood()
        else: self.food = np.array([x,y])

    def show(self):
        #mostra o jogo
        print(self.grid)

    def changeDirection(self, action):
        # Muda a direção que está indo, 4 significa continuar reto/fazer nada
        action = action.index(1)
        if action < 0 or action > 4:
            print("resultado invalido")
        elif action == 4:
            pass
        else:
            self.direction = action
        

    def _colision(self):
        # Checa se a cobra se chocuo com as beiras do mapa ou com ela mesma
        is_in_list = np.any(np.all(self.snake[0] == self.snake[1:], axis=1))
        if self.snake[0][0] < 0 or self.snake[0][0] > self.gamesize-1 or self.snake[0][1] < 0 or self.snake[0][1] > self.gamesize-1:
            return True
        elif is_in_list:
            return True
        return False
    
    def step(self, action = None):
        self.reward = 0
        if action == None: temp = int(input("Test: "))
        else: temp = action
        self.changeDirection(temp)
        if self._move():
            self._updateGrid()
            #self.show()
        if self.remaningMoves <= 0:
            self.gameOver == True
        return self.getState(), self.reward, int(self.gameOver)

def plot(scores, mean_scores):
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show()
        

if __name__ == "__main__":
    
    echo = False #Caso queira ver a AI jogando coloque pra True
    ngames = 5000
    gamesize = 8
    
    player = agent(nnformat=[6+(gamesize*gamesize), 120, 5])
    scores = []
    meanScores = [0,0,0,0,0]
    record = 0
    n = 0

    for i in tqdm(range(ngames)):
        session = snake()
        if echo: session.show()
        state = session.getState()
        while not session.gameOver:

            action = player.action(state)
            newstate, reward, done = session.step(action)
            player.shortTermMemory(state, action, newstate, reward, done)
            player.remember(state, action, newstate, reward, done)
        
        player.longTermMemory()
        scores.append(session.score)
        if session.score > record:
            record = session.score
        if len(scores) > 5:
            meanScores.append(sum(scores[-100:])/5)
        if echo: print("Game Over")
    plot(scores, meanScores)
    import pdb
    pdb.set_trace()




    
            
