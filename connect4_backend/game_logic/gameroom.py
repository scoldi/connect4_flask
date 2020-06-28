import json
import numpy as np


class GameRoom:

    def __init__(self, width, height):
        # self.g = 1
        # 7
        self.width = width
        self.turn_player = 0
        self.turn_num = 0
        # 6
        self.height = height
        self.matrix = np.full((width, height), dtype=int, fill_value=-1)
        self.players = []
        self.spectators = []

        # array([[-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1]])

    def move(self, sid, column):
        player_num = self.players.index(sid)
        print(player_num)
        try:
            res = max(idx for idx, val in enumerate(self.matrix[column])
                  if val == -1)
        except:
            # success = False
            print('invalid turn')
        self.matrix[column][res] = player_num
        self.turn_num = self.turn_num + 1
        self.turn_player = self.turn_num % 2
        print(self.matrix)

    def add_user(self, sid):
        if len(self.players) < 2:
            # self.players.append({'sid': sid,
            #                     'num': len(self.players),
            #                     'name': name
            #                     })
            self.players.append(sid)
        else:
            self.spectators.append(sid)

    def remove_user(self, sid):
        if self.is_player(sid):
            self.players.remove(sid)
        else:
            self.spectators.remove(sid)

    def is_player(self, sid):
        return sid in self.players

    def get_data(self, sid=None):
        data = {
            'width': self.width,
            'height': self.height,
            'matrix': self.matrix.tolist(),
            'turn_num': self.turn_num,
            'turn_player': self.turn_player
        }
        if sid is not None and sid in self.players:
            data['player_num'] = self.players.index(sid)
        return json.dumps(data)

    # def get_user(self):
















