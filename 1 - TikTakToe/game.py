
class grid():

    def __init__(self, punishment = 10):
        self.ttt = [0,0,0,
                    0,0,0,
                    0,0,0]
        
        self.winReward = 0
        self.wrongMovePunishment = punishment
        

    def show(self):
        #TODO deixar apresentação mais bonita
        temp = ""
        for i in range(0,9):
            if self.table[i] == 1: temp = temp + "X"
            elif self.table[i] == -1: temp = temp + "O"
            else: print(i+1)
            if (i+1)%3!=0:
                temp = temp +" | "
            else:
                print(temp)
                print("------")
                temp = ""


    def checkGame(self):
        table = [self.ttt[0:3],self.ttt[3:6], self.ttt[6:9]]
        for linha in table:
            if linha.count(linha[0]) == 3:
                return linha[0]

        for i in range(2):
            coluna = [table[0][i],table[1][i], table[2][i]]
            if coluna.count(coluna[0]) == 3:
                return coluna[0]

        diagonal1 = [table[0][0], table[1][1], table[2][2]]
        if diagonal1.count(diagonal1[0]) == 3:
                return diagonal1[0]

        diagonal2 = [table[0][2], table[1][1], table[2][0]]
        if diagonal2.count(diagonal2[0]) == 3:
                return diagonal2[0]
        return 0
   

    def changeGrid(self, player, number):
        if type(number) == list:
            number = number.index(1)
        else:
            number = int(number)
            if number > 0 and number < 10:
                number = int(number) - 1
            else:
                #self.reward -= self.punishment
                return False

        #linha = number % 3
        #oluna = number // 3

        if self.ttt[number] != 0:
            return False 
        
        self.ttt[number] = player
        return True


def main():
    game()


def game(tipo = ["humano", "humano"], echo = True, bot = None):
    gameWon = False
    playerMark = ["O", "X"]
    turno = 0
    gameGrid = grid()
    numeros = [-1, 1]

    while not gameWon:
        moveAccepted = False
        jogador = turno % 2
        marca = playerMark[jogador]
        nmarca = numeros[jogador]
        wrongMoves = 0
        if echo: print("Vez do jogador: ", marca)

        print(gameGrid.ttt)
        #gamegrid.show()

        while not moveAccepted:
            if wrongMoves > 4:
                gameWon = True
                print(playerMark[(jogador + 1)%2], "venceu por WO!!!")
                break
            elif tipo[jogador] == "humano":
                jogada = input("Número da casa: ")
            else:
                jogada = bot.action(gameGrid.ttt)
            
            if not gameGrid.changeGrid(nmarca, jogada):
                wrongMoves += 1
            else:
                moveAccepted = True

        gameGrid.changeGrid(nmarca, jogada)

        if gameGrid.checkGame() != 0:
            gameWon = True
            if echo:
                print(gameGrid.ttt)
                print(marca, "Venceu!!!")
            if jogador == 0: return -1
            return 1
        elif turno == 9:
            if echo: print("Deu velha!")
            return 0
        else:
            turno += 1
    
    
if __name__ == "__main__":
    main()