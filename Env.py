"test"

import numpy as np
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk


UNIT = 40   # pixels
MAZE_H = 3  # grid height
MAZE_W = 3  # grid width
points = [[UNIT/2,UNIT/2],       [UNIT/2+UNIT,UNIT/2],       [UNIT/2+2*UNIT,UNIT/2],
          [UNIT/2,UNIT/2+UNIT],  [UNIT/2+UNIT,UNIT/2+UNIT],  [UNIT/2+2*UNIT,UNIT/2+UNIT],
          [UNIT/2,UNIT/2+2*UNIT],[UNIT/2+UNIT,UNIT/2+2*UNIT],[UNIT/2+2*UNIT,UNIT/2+2*UNIT]]
# board_info 0 for free, 1 for red, 2 for yellow 
board = ['0','0','0','0','0','0','0','0','0']

class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = list(range(0,9))
        self.n_actions = len(self.action_space)
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)
        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)
        # pack all
        self.canvas.pack()
        
    def redgo(self,place):
        oval_center = points[place]
        self.ovalr = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='red')
        #print("red go ",place)
        
    def yellowgo(self,place):
        oval_center = points[place]
        self.ovaly = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')
        #print("yellow go ",place)

    def reset(self):
       
        #self.canvas.delete(self.ovalr)
        #self.canvas.delete(self.ovaly)
        self.canvas.delete("all")

        for i in range(0,9):
            board[i] = '0'
        self.update()
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)
        # pack all
        self.canvas.pack()
        self.update()
        return "".join(board)
        
        #print()

    def step(self, action, player):
        s_ = board
        reward_red = 0
        reward_yellow = 0
        done = False
        keep_state = False
        nextplayre = ""
        if(board[action]!='0' and player == "red"):
            reward_red = -1
            s_ = board
            s_ = "".join(s_)
            done = False
            keep_state = True
            nextplayer = "red"
        if(board[action]!='0' and player == "yellow"):
            reward_yellow = -1
            s_ = board
            s_ = "".join(s_)
            done = False
            keep_state = True
            nextplayer = "yellow"
        if(board[action] == '0' and player == "red"):
            board[action] = "1"
            self.redgo(action)
            s_ = "".join(s_)
            nextplayer = "yellow"
            if(self.checkwin()==1):
                reward_red = 1
                reward_yellow = -1
                done = True
                s_ = "terminal"
        if(board[action] == '0' and player == "yellow"):
            board[action] = "2"
            self.yellowgo(action)
            s_ = "".join(s_)
            nextplayer = "red"
            if(self.checkwin()==2):
                reward_yellow = 1
                reward_red = -1
                done = True
                s_ = "terminal"
        if(self.checkeven()):
            done = True
            s_ = "terminal"
            reward_red = 0.5
            reward_yellow = 0.5
        print("board: ",s_)
        return s_, reward_red, reward_yellow, done, nextplayer, keep_state

    def render(self):
        time.sleep(0.5)
        self.update()
        
    def checkwin(self):
        win = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for i in win:
            count_1 = 0
            count_2 = 0
            for j in i:
                if(board[j] == '1'):
                    count_1 += 1
                if(board[j] == '2'):
                    count_2 += 1
            if(count_1 == 3):
                print("red win")
                return 1
            if(count_2 == 3):
                print("yellow win")
                return 2
        return 0

    def checkeven(self):
        for i in board:
            if(i == '0'):
                return False
        return True

def update():
    for t in range(10):
        s = env.reset()
        while True:
            env.render()
            a = 1
            s, r, done = env.step(a)
            if done:
                break

if __name__ == '__main__':
    env = Maze()

    env.mainloop()
