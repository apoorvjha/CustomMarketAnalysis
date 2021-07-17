from collections import namedtuple, deque
from random import sample, random
from math import exp
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPool1D, LSTM, Dropout, Flatten, Dense
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
    def __init__(self,input_shape,n_output,mode=0):
        '''
        [+] Mode=0, if the model needs to contain Convolution layers.
        [+] Mode=1, if the model is composed of LSTM layers.
        [+] ultimately few final layers shall be composed of fully connected Dense neurons.
        [+] input_shape is a tuple that is supplied by the object of this class denoting the 
            size of input vector/matrix.
        [+] n_output is an integer denoting the total number of neurons that shall be present 
            in output layer.
        '''
        self.model=Sequential()
        if mode==0:
            self.model.add(Conv1D(16,2,input_shape=input_shape,padding='same',activation='relu'))
            self.model.add(Conv1D(32,2,padding='same',activation='relu'))
            self.model.add(Conv1D(64,2,padding='same',activation='relu'))
            self.model.add(Flatten())
            self.model.add(Dense(input_shape[0] * 64,activation='relu'))
            self.model.add(Dropout(0.2))
            #self.model.add(Dense(64,activation='relu'))
            #self.model.add(Dropout(0.2))
            #self.model.add(Dense(32,activation='relu'))
            #self.model.add(Dropout(0.2))
            self.model.add(Dense(16,activation='relu'))
            self.model.add(Dropout(0.2))
            self.model.add(Dense(n_output))
        else:
            self.model.add(LSTM(8,dropout=0.2,input_shape=input_shape,return_sequences=True))
            self.model.add(LSTM(16,dropout=0.2,return_sequences=True))
            self.model.add(LSTM(32,dropout=0.2,return_sequences=True))
            self.model.add(Dense(16,activation='relu'))
            self.model.add(Dropout(0.2))
            self.model.add(Dense(n_output))
        self.model.compile(optimizer=Adam(1e-3),loss='huber',metrics=['mse'])
    def getModelInstance(self):
        return self.model


class Agent:
    def __init__(self,input_shape,n_output):
        self.GAMMA=0.999             # The discount factor for normalizing future reward.
        self.BATCH_SIZE=32           # The chunk of states provisioned randomly for training.
        # ---------- Epsilon greedy strategy variables -------------#
        self.EPSILON_START=0.9       
        self.EPSILON_END=0.05
        self.EPSILON_DECAY=200
        #-----------------------------------------------------------#
        self.TARGET_UPDATE=10
        '''
        The TARGET_VALUE is number of episodes after which the weights and biases of target network
        to be set as same as that of policy network. This provides stability to the model as 
        suggested in orignal DQN paper.
        '''
        self.MEMORY_SIZE=50000       # Experience replay memory capacity.
        self.policy_net=DQN(input_shape,n_output)
        self.target_net=DQN(input_shape,n_output)
        self.target_net.set_weights(self.policy_net.get_weights())
        self.memory=Experience(self.MEMORY_SIZE)
        self.time_step=0

    def selectAction(self,action_space):
        EPSILON_THRESHOLD=self.EPSILON_END + (self.EPSILON_START - self.EPSILON_END) * exp(-1 * self.time_step / EPSILON_DECAY)
        self.time_step+=1
        if random() > EPSILON_THRESHOLD:
            # Exploitation
            return self.policy_net.predict(state)
        else:
            # Exploration
            return choice(action_space)
    def optimize(self):
        if len(self.memory) < self.BATCH_SIZE:
            return
        transitions=memory.sample(self.BATCH_SIZE)
        








