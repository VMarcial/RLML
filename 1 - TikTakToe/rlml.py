import torch
import torch.nn as nn
import torch.nn.functional as F
import random
import torch.optim as optim
from collections import deque
import numpy as np


class agent():

    def __init__(self, batchSize = 1000, maxMemory = 100_000, nnFormat = [10,45,9], initialEpsilon = 0.01, gamma = 0.01, alpha =0.01):

        self.gamesPlayed = 0
        self.epsilon     = initialEpsilon
        self.gamma       = gamma
        self.alpha       = alpha
        self.memory      = deque(maxlen= maxMemory)
        self.model       = qNet(nnformat= nnFormat)
        self.trainer     = nnTrainer(self.model, lr=self.alpha, gamma = self.gamma)
        self.batchSize   = batchSize


    def getState(self, game):
        state = game.ttt
        return np.array(state, dtype = int)

    def action(self, state):
        move = [0] * self.nnformat[-1]
        if random.randint(0,100)/100 < self.epsilon:
            temp = random.randint(0,self.nnformat[-1] - 1)
            move[temp] = 1
        else:
            state0 = torch.tensor(state, dtype = torch.float)
            pred = self.model(state0)
            temp = torch.argmax(pred).item()
            move[temp] = 1
        return move


    def shortTermMemory(self, state, action, reward, next_state, wrongmove, done):
        self.trainer.train(state, action, reward, next_state, wrongmove, done)


    def longTermMemory(self):
        if len(self.memory) > self.batchSize:
            sample = random.sample(self.memory, self.batchSize)            
        else:
            sample = self.memory

        states, actions, rewards, next_states, wrongmoves, dones = zip(*sample)
        self.trainer.train(states, actions, rewards, next_states, wrongmoves, dones)

    def _updateEpsilon():
        pass

    def remember(self, state, action, reward, nextstate, wrongmoves, done):
        self.memory.append((state, action, reward, nextstate, wrongmoves, done))

class qNet(nn.model):
    
    def __init__(self, nnformat:list):
        super().__init__()
        self.layers = self._defineLayers(nnformat)


    def forward(self,x):
        for i in range(len(self.layers)-1):
            x = F.relu(self.layers[i](x))
        x = self.layers[-1](x)
        return x
    

    def _defineLayers(self, nnformat):
        for i in len(nnformat):
            self.layers.append(nn.Linear(nnformat[i], nnformat[i+1]))


    def export(self, savepath = 0):
        pass


class nnTrainer():
    def __init__(self, lr, gamma, model):
        self.alpha = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters, lr = self.alpha)
        self.criterion = nn.MSELoss()


    def train(self, state, action, reward, next_state, wrongmoves, done):
        state = torch.tensor(state, dtype = torch.float)
        action = torch.tensor(action, dtype = torch.float)
        reward = torch.tensor(reward, dtype = torch.float)
        next_state = torch.tensor(next_state, dtype = torch.float)
        wrongmoves = torch.tensor(wrongmoves, dtype = torch.float)
            
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            next_state = torch.unsqueeze(next_state, 0)
            wrongmoves = torch.unsqueeze(wrongmoves, 0)            
                            
        pred = self.model(state)

        target = pred.clone()

        for i in range(len(done)):
            if done[i]: Qnew = reward[i]
            else:
                Qnew = reward[i] + self.gamma + torch.max(self.model(next_state[i]))

            target[i][torch.argmax(action).item] = Qnew
        
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()

def train():
    scores = []
    meanScores = []
    record = 0
    
    


