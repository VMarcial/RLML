
class grid():

    def __init__(self, punishment ):
        self.ttt = [[0,0,0],
                    [0,0,0],
                    [0,0,0]]
        
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
        for linha in self.ttt:
            if linha.count(linha[0]) == 3:
                return linha[0]

        for i in range(2):
            coluna = [self.ttt[0][i], self.ttt[1][i], self.ttt[2][i]]
            if coluna.count(coluna[0]) == 3:
                return coluna[0]

        diagonal1 = [self.ttt[0][0], self.ttt[1][1], self.ttt[2][2]]
        if diagonal1.count(diagonal1[0]) == 3:
                return diagonal1[0]

        diagonal2 = [self.ttt[0][2], self.ttt[1][1], self.ttt[2][0]]
        if diagonal2.count(diagonal2[0]) == 3:
                return diagonal2[0]
        return 0
   

    def changeGrid(self, player, number):
        number = int(number)
        if number > 0 and number < 10:
            number = int(number) - 1
        else:
            self.reward -= self.punishment
            return False

        linha = number % 3
        coluna = number // 3

        if self.ttt[coluna][linha] != 0:
            return False 
        
        self.ttt[coluna][linha] = player
        return True


def main():
    game()


def game(tipo = ["humano", "humano"], echo = True):
    gameWon = False
    playerMark = ["O", "X"]
    turno = 0
    gameGrid = grid()

    while not gameWon:
        jogador = turno % 2
        marca = playerMark[jogador]
        if echo: print("Vez do jogador: ", marca)

        print(gameGrid.ttt)
        #gamegrid.show()

        if tipo[jogador] == "humano":
            jogada = input("Número da casa: ")
        else:
            #TODO colocar interação do bot aqui
            pass

        gameGrid.changeGrid(marca, jogada)

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