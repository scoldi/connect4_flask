import json
import numpy as np


class GameRoom:

    def __init__(self, width, height):
        # self.g = 1
        # 7
        self.width = width
        self.turn = 1
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

    def move(self, player_num, column):
        for cell in self.matrix[column]:
            if cell == -1:
                continue
            else:
                self.matrix[column][cell] = player_num
        self.turn = self.turn
        print(self.matrix)

    def add_user(self, sid, name):
        if len(self.players) < 2:
            self.players.append({'sid': sid,
                                 'num': len(self.players),
                                 'name': name
                                 })
        else:
            self.spectators.append(sid)

    def get_data(self):
        data = {
            'width': self.width,
            'height': self.height,
            'matrix': self.matrix.tolist()
        }
        return json.dumps(data)

    # def get_user(self):
















