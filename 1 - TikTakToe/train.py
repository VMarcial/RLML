from rlml import agent
from game import grid
import random

def trainNN(ngames = 1000):
    score1 = []
    score2 = []
    mean1 = []
    mean2 = []
    record1 = 0
    record2 = 0
    k = 0
    player1 = agent()
    player2 = agent()
    playerMark = ["O", "X"]
    players = [player1, player2]

    while k < ngames:
        game = grid()
        gameWon = False
        turno = 0
        firstplayer = random.randint(0,1)

        while not gameWon:
            player = (turno + firstplayer) %2
            marca = playerMark[player]
            oldState = game.ttt.copy()
            moveAccepted = False
            wrongMoves  = 0
            reward = 0
            
            while not moveAccepted:
                action = players[player].action(game.ttt)
                
                if not game.changeGrid(marca, action):
                    wrongMoves +=1
                    players[player].shortTermMemory(game.ttt, action, game.ttt, game.wrongMovePunishment, wrongMoves, done)
                
                if wrongMoves > 4:
                    reward  -= 100
                    done     = 1
                    gameWon  = True
                    winner   = (player + 1)%2
                    break

                if game.checkGame() != 0:
                    gameWon = True
                    done    = 1
                    winner  = player
                elif turno == 9:
                    gameWon = True
                    done    = 1 
                    winner  = None
            
            if winner == None:
                players[0].shortTermMemory(oldState, action, game.ttt, game.winReward/2, wrongMoves, done)
                players[1].shortTermMemory(oldState, action, game.ttt, game.winReward/2, wrongMoves, done)
            else:
                players[winner].shortTermMemory(oldState, action, game.ttt, game.winReward, wrongMoves, done)
            turno += 1
        k += 1


