from game_logic.gameroom import GameRoom
from dqn.agent import DQNAgent
import json
import time

class GameBroker:

    def __init__(self, x, y, consec_games, total_games):
        self.games = []
        self.agents = []
        self.stats = []
        self.consec_games = consec_games
        self.total_games = total_games
        self.x = x
        self.y = y
        self.games_elapsed = 0
        self.turn_player = 0

    def resolve_game(self, game):
        while not game.finished:
            self.agents[game.turn_player].move_and_learn(game)
            print(game.matrix)
            time.sleep(1)
        self.agents[game.turn_player].win = True
        self.games_elapsed += 1
        print('games_elapsed', self.games_elapsed)

        # losers = self.agents
        # del losers[game.winner]
        # for loser in losers:
        #     loser.learn_after_game(game)

    def reset(self):
        print('created games: ', min(self.consec_games, self.total_games - self.games_elapsed))
        self.games = []
        for n in range(min(self.consec_games, self.total_games - self.games_elapsed)):
            game = GameRoom(self.x, self.y)
            self.games.append(game)

    def execute(self):
        while self.games_elapsed < self.total_games:
            self.reset()
            for agent in self.agents:
                self.add_user(agent.sid)
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




