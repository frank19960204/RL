"""
This part of code is the Q learning brain, which is a brain of the agent.
All decisions are made in here.
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

import numpy as np
import pandas as pd


class QLearningTable:
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table_red = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.q_table_yellow = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def choose_action(self, observation, player):
        # action selection
        if np.random.uniform() < self.epsilon:
            # choose best action
            if(player == "red"):
                self.check_state_exist(observation,player)
                state_action = self.q_table_red.loc[observation, :]
            if(player == "yellow"):
                self.check_state_exist(observation,player)
                state_action = self.q_table_yellow.loc[observation, :]
            
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            # choose random action
            action = np.random.choice(self.actions)
        print(player," go ",action)
        return action

    def learn(self, s, a, r, s_, player):
        self.check_state_exist(s_,player)
        if(player == "red"):
            q_predict = self.q_table_red.loc[s, a]
             
            if s_ != 'terminal':
                q_target = r + self.gamma * self.q_table_red.loc[s_, :].max()  # next state is not terminal
            else:
                q_target = r  # next state is terminal
            self.q_table_red.loc[s, a] += self.lr * (q_target - q_predict)  # update
            print("red\n",self.q_table_red)
        if(player == "yellow"):
            q_predict = self.q_table_yellow.loc[s, a]
             
            if s_ != 'terminal':
                q_target = r + self.gamma * self.q_table_yellow.loc[s_, :].max()  # next state is not terminal
            else:
                q_target = r  # next state is terminal
            self.q_table_yellow.loc[s, a] += self.lr * (q_target - q_predict)  # update
            print("yellow\n",self.q_table_yellow)

    def check_state_exist(self, state, player):
        if(player == "red"):
            if state not in self.q_table_red.index:
            # append new state to q table
                self.q_table_red = self.q_table_red.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table_red.columns,
                    name=state,
                )
            )
        if(player == "yellow"):
            if state not in self.q_table_yellow.index:
            # append new state to q table
                self.q_table_yellow = self.q_table_yellow.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table_yellow.columns,
                    name=state,
                )
            )
       
