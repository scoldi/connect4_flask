from game_logic.gameroom import GameRoom
import json

class GameBroker:

    def __init__(self, x, y, n_games):
        self.games = []
        self.agents = []
        self.stats = []
        self.x = x
        self.y = y
        self.turn_player = 0

        for n in range(n_games):
            game = GameRoom(x=self.x, y=self.y)
            self.games.append(game)

    def get_game(self, uuid):
        return next(game for game in self.games if game.uuid == uuid)

    def get_info(self):
        result = []
        for game in self.games:
            result.append(game.get_data())
        return json.dumps(result)



