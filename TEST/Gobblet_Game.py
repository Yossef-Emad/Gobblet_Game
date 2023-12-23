import os
import pandas as pd
from matplotlib import pyplot as plt

class Gobbler_piece:
    def __init__(self, player: int, piece_no: int):
        self.player = player  # integer -2-2
        self.piece_no = piece_no  # integers 0-11
        self.board_position = None  # integers 0-15 or None
        self.board_position_previous = None  # so that it can be placed back where it came from
        self.is_on_top = True


class Game:
    def __init__(self):
        self.player_name = ['player 0', 'player 1']
        self.winner = None

        # create the gobblers
        number_of_gobbler_pieces = 12
        self.gobblers = []
        for player in range(2):  # number of players
            piece_no = 1
            for gobbler in range(number_of_gobbler_pieces):
                gobbler = Gobbler_piece(player, piece_no)
                self.gobblers.append(gobbler)
                piece_no += 1

        self.current_player_idx = 0
        self.selected_gobbler_piece = None
        self.board = []
        for _ in range(16):
            self.board.append([])

        self.winning_combinations = [
            [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15],
            [0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15],[0,5,10,15],[3,6,9,12]
        ]
 #the rules for selecting gobbler piece
    def select_gobbler_object(self, gobbler_piece: int) -> bool:
        if self.winner is not None :
            return False
        if self.selected_gobbler_piece:
            return False
        if self.Original_input(gobbler_piece, 0, 11) is None:
            return False
        matching_gobblers = [g for g in self.gobblers if g.player == self.current_player_idx][self.Original_input(gobbler_piece, 0, 11)]
        if not matching_gobblers.is_on_top:
            return False
        self.selected_gobbler_piece = matching_gobblers
        if self.selected_gobbler_piece.board_position is not None:
            del self.board[self.selected_gobbler_piece.board_position][-1]
        self.selected_gobbler_piece.board_position_previous = self.selected_gobbler_piece.board_position
        self.selected_gobbler_piece.board_position = None
        self._update_on_top()
        return True

    def select_gobbler_position(self, board_position: int) -> bool:
        board_position = self.Original_input(board_position, 0, 15)
        if not self.selected_gobbler_piece or self.selected_gobbler_piece.board_position_previous == board_position or board_position is None or self.board[board_position] and self.selected_gobbler_piece.piece_no <= self.board[board_position][-1].piece_no:
            return False, None
        self.board[board_position].append(self.selected_gobbler_piece)
        self.selected_gobbler_piece.board_position = board_position
        self._update_on_top()
        self.current_player_idx = int(not self.current_player_idx)
        self.selected_gobbler_piece = None
        return True, self._check_for_winner()

    def _update_on_top(self):
        """
        checks all of the gobblers on the board and
        updates their is_on_top flag
        """

        for position in self.board:
            for n, gobbler in enumerate(position):
                if len(position) - 1 == n:
                    gobbler.is_on_top = True
                else:
                    gobbler.is_on_top = False

    def set_player_names(self, player_names: list) -> list[bool, str]:
        player_name_0 = player_names[0]
        player_name_1 = player_names[1]
        name_len_requirement = 3
        if len(player_name_0) < name_len_requirement or len(player_name_1) < name_len_requirement:
            return False, f'Player names must be at least {name_len_requirement} characters long.'
        elif player_name_0 == player_name_1:
            return False, 'Player names cannot be identical.'
        else:
            self.player_names = player_names
            return True, 'Let the games begin!'
    def _check_for_winner(self) -> int:
        """
        checks if there is a winner
        if so, returns winner (int)
        if not, returns None
        """
        # check all of the winning combinations for a winner

        for combo in self.winning_combinations:
            # initialize a list to keep track of the
            # owner of each piece
            result_to_check = []
            for position in combo:
                if self.board[position]:
                    # record the player of the current piece in a list
                    result_to_check.append(self.board[position][-1].player)
                else:
                    result_to_check.append(None)
            # if there is only one non-None unique value, then
            # we have a winner
            unique_values = list(set(result_to_check))
            if len(unique_values) == 1 and unique_values[0] is not None:
                self.winner = unique_values[0]
                return self.winner
        return None
            #still shearching
        #for i ,j in enumerate(self.board):
         #   if j==0:
         #       return 1
            #tie case
       # return 0


    def Draw_board(self) -> str:
        new_board = ''
        k = 0
        for cell in self.board:
            if cell:
                str_to_add = f'|{cell[-1].piece_no}({cell[-1].player})'
            else:
                str_to_add = f'|____'
            new_board += str_to_add
            k += 1
            if k > 3:
                new_board += '|\n'
                k = 0
        new_board += '-----------------------'
        return new_board

    def Original_input(self, value: int, minimum: int, maximum: int) -> int:
        return (int(value))-1 if minimum <= ((int(value))-1) <= maximum else None

    def get_possible_moves(self,board,gobblers)->list:
        r1=[g.board_position for g in gobblers if g.is_on_top and g.player==self.current_player_idx]
        r2=[i for i ,cell in enumerate(board) if cell == 0]
        return [r1,r2]
    def get_list_selected_gobblers(self,gobblers)->list:
        r1 = [g.piece_no for g in gobblers if g.is_on_top and g.player == self.current_player_idx]
        r2 =[g.piece_no for g in gobblers if g.board_position is None and g.board_position_previous is None and g.player == self.current_player_idx]
        return [r1,r2]
    def winner_case(self)->int:
        for move in self.winning_combinations:
            result = []
            for pcell in move:
                if self.board[pcell]:
                    result.append(self.board[pcell][-1].player)
                else:
                    result.append(None)
            unique_result= list(set(result))
            if len(unique_result) == 1 and unique_result[0] is not None:
                self.winner = unique_result[0]
                return self.winner
        #return None
        # still shearching
        for i ,cell in enumerate(self.board):
          if cell==0:
               return 1
         #tie case
        return 0

    def minimax(self, board: list, depth: int, isMaximizing: bool, firstTime=True) -> int:
        result = self.winner_case()
        if result is not None or depth == 0:
            return result
        if isMaximizing:
            best_score = float('-inf')
            for r in self.get_list_selected_gobblers(self.gobblers):
                self.select_gobbler_object(r)
                for move in self.get_possible_moves(self.board, self.gobblers):
                    self.select_gobbler_position(move)
                    score = self.minimax(board, depth - 1, False, False)
                    best_score = max(best_score, score)
                    if firstTime:
                        board[move]= r
            return best_score
        else:
            best_score = float('inf')  # Change to positive infinity for minimizing
            for r in self.get_list_selected_gobblers(self.gobblers):
                self.select_gobbler_object(r)
                for move in self.get_possible_moves(self.board, self.gobblers):
                    self.select_gobbler_position(move)
                    score = self.minimax(board, depth - 1, True, False)
                    best_score = min(best_score, score)
                    if firstTime:
                        board[move]= r
            return best_score

    #def minimax_alpha_beta_pruning(self):

    @property
    def winner_name(self) -> str:
        return self.player_name[self.winner] if self.winner is not None else None
    @property
    def current_player_name(self) -> str:
        return self.player_name[self.current_player_idx]



