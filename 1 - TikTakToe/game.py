
class grid():
    def __init__(self):
        self.ttt = [[1,2,3],
                    [4,5,6],
                    [7,8,9]
                    ]
        self.teste = 0

    #
    def show(self):
        pass

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
            return False

        linha = number % 3
        coluna = number // 3

        #TODO colocar um check se a casa não está ocupada

        self.ttt[coluna][linha] = player

        return True

def main():
    game()

def game(tipo = ["humano", "humano"]):
    gameWon = False
    playerMark = ["X", "O"]
    turno = 0
    gameGrid = grid()

    while not gameWon:
        jogador = turno % 2
        marca = playerMark[jogador]
        print("Vez do jogador: ", marca)

        print(gameGrid.ttt)

        if tipo[jogador] == "humano":
            jogada = input("Número da casa: ")
        else:
            #TODO colocar interação do bot aqui
            pass

        gameGrid.changeGrid(marca, jogada)

        if gameGrid.checkGame() != 0:
            gameWon = True
            print(gameGrid.ttt)
            print(marca, "Venceu!!!")
        elif turno == 9:
            print("Deu velha!")
            break
        else:
            turno += 1

    
if __name__ == "__main__":
    main()