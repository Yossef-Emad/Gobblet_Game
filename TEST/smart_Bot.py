from Gobblet_Game import Game
from start import Player
class smart_Bot(Player):
    def __init__(self,player_number,name,game):
        super().__init__(player_number, name, game)
    def play(self):
        game=Game()
        result=game.minimax(game.board,5,True,True)
        print(game.Draw_board())
#while True:
