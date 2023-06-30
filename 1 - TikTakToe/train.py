from rlml import agent
from game import grid, game
import random

def trainNN(ngames = 1000):
    score1 = []
    score2 = []
    mean1 = []
    mean2 = []
    record1 = 0
    record2 = 0
    k = 0
    player1 = agent(-1)
    player2 = agent(1)
    playerMark = ["O", "X"]
    playerNumber = [-1, 1]
    players = [player1, player2]
    empate = 0
    wo = 0
    vencedor = [0,0]

    while k < ngames:
        game = grid()
        gameWon = False
        done = 0
        turno = 0
        firstplayer = random.randint(0,1)
        winner = False

        while not gameWon:
            player = (turno + firstplayer) %2
            marca = playerMark[player]
            numero = playerNumber[player]
            oldState = game.ttt.copy()
            moveAccepted = False
            wrongMoves  = 0
            reward = 0
            
            while not moveAccepted:
                action = players[player].action(game.ttt)
                
                if not game.changeGrid(numero, action):
                    wrongMoves +=1
                    players[player].shortTermMemory(game.ttt, action, game.ttt, game.wrongMovePunishment, wrongMoves, done)
                
                else:
                    moveAccepted = True

                if wrongMoves > 4:
                    reward  -= 100
                    done     = 1
                    gameWon  = True
                    winner   = (player + 1)%2
                    wo += 1
                    break

                if game.checkGame() != 0:
                    gameWon = True
                    done    = 1
                    winner  = player
                    vencedor[player] += 1

                elif turno == 9:
                    gameWon = True
                    done    = 1 
                    winner  = None
                    empate +=1
            
            if winner == None:
                players[0].shortTermMemory(oldState, action, game.winReward/2, game.ttt, wrongMoves, done)
                players[1].shortTermMemory(oldState, action, game.winReward/2, game.ttt, wrongMoves, done)
            else:
                players[winner].shortTermMemory(oldState, action, game.winReward, game.ttt, wrongMoves, done)
            turno += 1
        print(k, winner)
        k += 1

        players[0].gamesPlayed += 1
        players[1].gamesPlayed += 1

    print(vencedor)
    print("empate", empate)
    print("wo", wo)

    return [player1, player2]
    


if __name__ == "__main__":
    x = trainNN()
    player1 = x[0]
    while True:
        game(tipo = ["humano", "bot"], echo = True, bot = player1)

