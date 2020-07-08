from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
from keras.utils import to_categorical

import random
import numpy as np
import uuid

LOAD_WEIGHTS = False

class DQNAgent(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reward = 0
        self.gamma = 0.9
        self.short_memory = np.array([])
        self.learning_rate = 0.0005
        if LOAD_WEIGHTS:
            self.model = self.network("weights/weights2_after_empty.hdf5")
            print('weights loaded successfully!')
            self.epsilon = 0
        else:
            self.model = self.network()
            self.epsilon = 500
        self.actual = []
        self.last_move = -1
        self.memory = []
        self.sid = uuid.uuid4()
        self.win = False

    def get_state(self, game):
        state = game.matrix.tolist()
        return np.asarray(state)

    def network(self, weights=None):
        model = Sequential()
        model.add(Dense(output_dim=120, activation='relu', input_dim=self.x * self.y))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=4, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if weights:
            model.load_weights(weights)
        return model

    def replay_new(self, memory):
        self.win = False
        if len(memory) > 2000:
            minibatch = random.sample(memory, 2000)
            memory = minibatch
        else:
            minibatch = memory
        for state, action, reward, next_state, defeat in minibatch:
            target = reward
            if not defeat:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    def move_and_learn(self, game):
        state_old = self.get_state(game)
        success = False
        while not success:
            if random.randint(0, self.epsilon) < self.epsilon:
                move = random.randint(0, self.x - 1)
            else:
                # predict action based on the old state
                prediction = self.model.predict(state_old.reshape((1, self.x * self.y)))
                move = np.argmax(prediction[0])
            # add negative reward for wrong turns
            success = game.move(self.sid, move)

        state_new = self.get_state(game)
        reward = self.set_reward(game)

        # train short memory base on the new action and state
        defeat = game.finished and not self.win
        self.train_short_memory(state_old, move, reward, state_new, defeat)

        # store the new data into a long term memory
        self.remember(state_old, move, reward, state_new, defeat)

    def set_reward(self, game):
        self.reward = 0
        if game.finished and self.win:
            self.reward = 10
        return self.reward


    def remember(self, state, action, reward, next_state, defeat):
        self.memory.append((state, action, reward, next_state, defeat))
        # print(len(self.memory))

    def train_short_memory(self, state, action, reward, next_state, defeat):
        target = reward
        if not defeat:
            target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, self.x * self.y)))[0])
        target_f = self.model.predict(state.reshape((1, self.x * self.y)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1, self.x * self.y)), target_f, epochs=1, verbose=0)
