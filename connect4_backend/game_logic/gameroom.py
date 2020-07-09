import numpy as np
import uuid

class InvalidTurnError(Exception):
    print('invalid turn attempt')
    pass


class GameRoom:

    def __init__(self, width, height):
        self.n_players = 2
        self.width = width
        self.height = height
        self.turn_player = 0
        self.turn_num = 0
        self.matrix = np.full((width, height), dtype=int, fill_value=-1)
        self.players_sid = []
        self.players_info = []
        self.spectators_sid = []
        self.winner_num = -1
        self.finished = False
        self.uuid = uuid.uuid1()

        # array([[-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1]])

    def move(self, sid, column):
        player_num = self.get_player_num(sid)
        print(player_num)
        try:
            res = max(idx for idx, val in enumerate(self.matrix[column]) if val == -1)
            self.matrix[column][res] = player_num
            self.turn_num = self.turn_num + 1
            self.turn_player = self.turn_num % 2
            return True
        except (InvalidTurnError, ValueError) as e:
            return False

    def check_winner(self):
        board_height = self.height
        board_width = self.width

        # check horizontal spaces
        for y in range(board_height):
            for x in range(board_width - 3):
                tile_val = self.matrix[x][y]
                if tile_val != -1:
                    if self.matrix[x + 1][y] == tile_val and self.matrix[x + 2][y] == tile_val and \
                            self.matrix[x + 3][y] == tile_val:
                        return tile_val

        # check vertical spaces
        for x in range(board_width):
            for y in range(board_height - 3):
                tile_val = self.matrix[x][y]
                if tile_val != -1:
                    if self.matrix[x][y + 1] == tile_val and self.matrix[x][y + 2] == tile_val and \
                            self.matrix[x][y + 3] == tile_val:
                        return tile_val

        # check / diagonal spaces
        for x in range(board_width - 3):
            for y in range(3, board_height):
                tile_val = self.matrix[x][y]
                if tile_val != -1:
                    if self.matrix[x + 1][y - 1] == tile_val and self.matrix[x + 2][y - 2] == tile_val and \
                            self.matrix[x + 3][y - 3] == tile_val:
                        return tile_val

        # check \ diagonal spaces
        for x in range(board_width - 3):
            for y in range(board_height - 3):
                tile_val = self.matrix[x][y]
                if tile_val != -1:
                    if self.matrix[x + 1][y + 1] == tile_val and self.matrix[x + 2][y + 2] == tile_val and \
                            self.matrix[x + 3][y + 3] == tile_val:
                        return tile_val

        return -1

    def get_player_num(self, sid):
        print(sid)
        print(self.players_info)
        return next(x['num'] for x in self.players_info if x['sid'] == sid)

    def add_user(self, sid):
        if len(self.players_sid) < self.n_players:
            self.players_info.append({'sid': sid,
                                     'num': [num for num in list(range(self.n_players)) if num not in [player['num'] for player in self.players_info]][0]
                                      })
            self.players_sid.append(sid)
        else:
            self.spectators_sid.append(sid)

    def remove_user(self, sid):
        if self.is_player(sid):
            for i in range(len(self.players_info)):
                if self.players_info[i]['sid'] == sid:
                    del self.players_info[i]
                    break
            self.players_sid.remove(sid)
        else:
            self.spectators_sid.remove(sid)

    def is_player(self, sid):
        return sid in self.players_sid

    def get_data(self, sid=None):
        winner = self.check_winner()
        data = {
            'width': self.width,
            'height': self.height,
            'matrix': self.matrix.tolist(),
            'turn_num': self.turn_num,
            'turn_player': self.turn_player
        }
        if sid is not None and sid in self.players_sid:
            data['player_num'] = self.get_player_num(sid)
            print('player num', data['player_num'])
        if winner != -1:
            self.finished = True
            data['winner'] = int(winner)
            data['finished'] = self.finished

        return data
