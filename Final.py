
from Env import Maze
from Brain import QLearningTable


def update():
    player = "red"
    for episode in range(100):
        player = "red"
        # initial observation
        observation_1 = env.reset()
       
        
        while True:
            # fresh env
            env.render()
            keep_state = True
            while keep_state:
                # RL choose action based on observation
                action_red = RL.choose_action(observation_1, player)
            
                # RL take action and get next observation and reward
                observation_2, reward_red, reward_yellow, done, player, keep_state = env.step(action_red, player)
                
                if(keep_state):
                # RL learn from this transition (punish for placing at unable space)
                    RL.learn(observation_1, action_red, reward_red, observation_2, "red")
                if done:
                    print("even")
                    break
    
              
            if done:
                RL.learn(observation_1, action_red, reward_red, observation_2, "red")
                break
            keep_state = True
            while keep_state:
                # RL choose action based on observation
                action_yellow = RL.choose_action(observation_2, player)
            
                # RL take action and get next observation and reward
                observation_3, reward_red, reward_yellow, done, player, keep_state = env.step(action_yellow, player)
                print(done)
                # RL learn from this transition (punish for placing at unable space)
                if(keep_state):
                    RL.learn(observation_2, action_yellow, reward_yellow, observation_3, "yellow")
                else:
                    RL.learn(observation_1, action_red, reward_red, observation_3, "red")
                   
                    observation_1 = observation_3
                  
                if done:
                    print("even")
                    break
                    
            # break while loop when end of this episode
            if done:
                break
        print("round:",episode+1,"end---------------------------------")
    # end of game
    print('game over')
    env.destroy()

if __name__ == "__main__":
    
    env = Maze()
    RL = QLearningTable(actions=list(range(env.n_actions)))

    env.after(1000, update)
    env.mainloop()
