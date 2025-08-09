import torch
import random
import numpy as np
from collections import deque
from model import LinearQNet, QTrainer
from game import Game2024  # Make sure this matches your class name

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness for exploration
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # experience replay buffer
        self.model = LinearQNet(16, 256, 4)  # input=16, hidden=256, output=4 actions
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        return game.get_state()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games  # Decaying epsilon
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
        return move

def train():
    agent = Agent()
    game = Game2024()

    while True:
        state_old = agent.get_state(game)
        action = agent.get_action(state_old)
        next_state, reward, done, score= game.step(action)

        agent.train_short_memory(state_old, action, reward, next_state, done)
        agent.remember(state_old, action, reward, next_state, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            print(f'Game {agent.n_games} Score: {score}')

if __name__ == '__main__':
    train()
