import torch
import torch.nn as nn
import torch.nn.functional as F
import random
import torch.optim as optim
from collections import deque
import numpy as np


class agent():

    def __init__(self, position, batchSize = 1000, maxMemory = 100_000, nnFormat = [10,45,9], initialEpsilon = 0.1, gamma = 0.9, alpha =0.001):

        self.gamesPlayed = 0
        self.position    = position
        self.nnformat    = nnFormat
        self.epsilon     = initialEpsilon
        self.gamma       = gamma
        self.alpha       = alpha
        self.memory      = deque(maxlen= maxMemory)
        self.model       = qNet(nnformat= nnFormat, position=self.position)
        self.trainer     = nnTrainer(alpha= self.alpha, gamma=self.gamma, model = self.model)
        self.batchSize   = batchSize


    def getState(self, state):
        tstate = torch.tensor(state, dtype = torch.float)
        if tstate.shape[0] != 10:
            x = torch.cat([tstate, torch.tensor(self.position, dtype=torch.float).reshape(1)], 0)
        return x

    def action(self, state):
        move = [0] * self.nnformat[-1]
        if random.randint(0,100)/100 > (self.epsilon/(self.gamesPlayed +1)):
            temp = random.randint(0,self.nnformat[-1] - 1)
            move[temp] = 1
        else:
            state0 = torch.tensor(state, dtype = torch.float) 
            state0 = state0.reshape([9])
            pred = self.model(state0)
            temp = torch.argmax(pred).item()
            move[temp] = 1
        return move


    def shortTermMemory(self, state, action, reward, next_state, wrongmove, done):
        state = self.getState(state)
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
        state = self.getState(state)
        self.memory.append((state, action, reward, nextstate, wrongmoves, done))

class qNet(nn.Module):
    
    def __init__(self, nnformat:list, position:int):
        super().__init__()
        self.position = position
        self.layers = []
        self._defineLayers(nnformat)
        self.layers = nn.ModuleList(self.layers)


    def forward(self,x):


        if len(x.shape) > 1:
            x = x.reshape(10)
        temp = torch.tensor(self.position, dtype=torch.float).reshape(1)
        if len(x.shape) >0:
            if x.shape[0] != 10:
                x = torch.cat((x, temp), 0)
        for i in range(len(self.layers)-1):
            x = F.relu(self.layers[i](x))
        x = self.layers[-1](x)
        return x
    

    def _defineLayers(self, nnformat):
        for i in range(len(nnformat)-1):
            self.layers.append(nn.Linear(nnformat[i], nnformat[i+1]))


    def export(self, savepath = 0):
        pass


class nnTrainer():
    def __init__(self, alpha, gamma, model):
        self.alpha = alpha
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr = self.alpha)
        self.criterion = nn.MSELoss()


    def train(self, state, action, reward, next_state, wrongmoves, done):
        nstate = torch.tensor(state, dtype = torch.float)
        naction = torch.tensor(action, dtype = torch.float)
        nreward = torch.tensor(reward, dtype = torch.float)
        nnext_state = torch.tensor(next_state, dtype = torch.float)
        nwrongmoves = torch.tensor(wrongmoves, dtype = torch.float)
            
        if len(state.shape) == 1:
            nstate = torch.unsqueeze(nstate, 0)
            naction = torch.unsqueeze(naction, 0)
            nreward = torch.unsqueeze(nreward, 0)
            nnext_state = torch.unsqueeze(nnext_state, 0)
            nwrongmoves = torch.unsqueeze(nwrongmoves, 0)       
            ndone = (done, )

        pred = self.model(nstate)

        target = pred.clone()

        if len(pred.shape) > 1:
            for i in range(len(ndone)):
                if ndone[i]: Qnew = reward[i]
                else:
                    import pdb
                    pdb.set_trace()
                    Qnew = nreward[i] + self.gamma + torch.max(self.model(nnext_state[i]))

                target[i][torch.argmax(naction[i]).item()] = Qnew
        
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()

