from collections import namedtuple, deque
from random import sample
from tensorflow.keras.model import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Flatten, Dense
from tensorflow.keras.optimizers import Adam


'''
State_Transition is structured way to store the state transiton of the environment and the
corresponding reward received in due course of action.
'''
State_Transition=namedtuple('Transition',('Current_State','Action','Reward','Next_State'))

class Experience:
    '''
    This class implements the replay memory which is essentially a bounded buffer which is
    used to store the transitions of the environment. The sample method randomly summons
    the N state transitions which our agent encountered. N is the batch size chosen by the model.
    This will be used to train the agent to maximize it's expected reward.
    '''
    def __init__(self,capacity):
        self.memory=deque([],maxlen=capacity)
    def see(self,*args):
        self.memory.append(State_Transition(*args))
    def sample(self,batch_size):
        return sample(self.memory,batch_size)
    def __len__(self):
        return (len(self.memory))

class DQN:
    def __init__(self):


class Agent:
    def __init__(self,):
        GAMMA=0.999             # The discount factor for normalizing future reward.
        BATCH_SIZE=32           # The chunk of states provisioned randomly for training.
        # ---------- Epsilon greedy strategy variables -------------#
        EPSILON_START=0.9       
        EPSILON_END=0.05
        EPSILON_DECAY=200
        #-----------------------------------------------------------#
        TARGET_UPDATE=10
        '''
        The TARGET_VALUE is number of episodes after which the weights and biases of target network
        to be set as same as that of policy network. This provides stability to the model as 
        suggested in orignal DQN paper.
        '''
        MEMORY_SIZE=50000       # Experience replay memory capacity.






