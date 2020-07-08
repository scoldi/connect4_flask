from game_logic.gameroom import GameRoom
from dqn.agent import DQNAgent
import json
import time

class GameBroker:

    def __init__(self, x, y, n_games):
        self.games = []
        self.agents = []
        self.stats = []
        self.x = x
        self.y = y
        self.turn_player = 0

        for n in range(n_games):
            game = GameRoom(self.x, self.y)
            self.games.append(game)

    def resolve_game(self, game):
        while not game.finished:
            self.agents[game.turn_player].move_and_learn(game)
            print(game.matrix)
            time.sleep(1)
        self.agents[game.turn_player].win = True

        # losers = self.agents
        # del losers[game.winner]
        # for loser in losers:
        #     loser.learn_after_game(game)

    def execute_batch(self):
        print('execute_batch')
        for game in self.games:
            print('started game')
            self.resolve_game(game)

    def get_game(self, uuid):
        return next(game for game in self.games if game.uuid == uuid)

    def get_data(self, sid=None):
        result = []
        for game in self.games:
            result.append(game.get_data())
        return json.dumps(result)

    def add_agent(self):
        agent = DQNAgent(self.x, self.y)
        self.agents.append(agent)
        self.add_user(agent.sid)
        print('agent added: ', agent.sid)

    def add_user(self, sid):
        for game in self.games:
            game.add_user(sid)

    def remove_user(self, sid):
        for game in self.games:
            game.remove_user(sid)




