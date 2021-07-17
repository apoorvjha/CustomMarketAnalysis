from collections import namedtuple, deque
from random import sample, random, randint
from math import exp
from numpy import array
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPool1D, LSTM, Dropout, Flatten, Dense
from tensorflow.keras.optimizers import Adam
import stockMarketSimulator as sim

'''
State_Transition is structured way to store the state transiton of the environment and the
corresponding reward received in due course of action.
'''
State_Transition=namedtuple('Transition',('Current_State','Action','Reward','Next_State','done'))

class Experience:
    '''
    This class implements the replay memory which is essentially a bounded buffer which is
    used to store the transitions of the environment. The sample method randomly summons
    the N state transitions which our agent encountered. N is the batch size chosen by the model.
    This will be used to train the agent to maximize it's expected reward.
    '''
    def __init__(self,capacity):
        self.memory=deque([],maxlen=capacity)
    def see(self,transition):
        self.memory.append(transition)
    def sample(self,batch_size):
        return sample(self.memory,batch_size)
    def __len__(self):
        return (len(self.memory))

class DQN:
    def __init__(self,input_shape,n_output,mode=1):
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
            self.model.add(Conv1D(16,1,input_shape=input_shape,padding='same',activation='relu'))
            self.model.add(Conv1D(32,1,padding='same',activation='relu'))
            self.model.add(Conv1D(64,1,padding='same',activation='relu'))
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
            self.model.add(Flatten())
            self.model.add(Dense(16,activation='relu'))
            self.model.add(Dropout(0.2))
            self.model.add(Dense(n_output))
        self.model.compile(optimizer=Adam(lr=1e-3),loss='huber',metrics=['mse'])
    def getModelInstance(self):
        return self.model


class Agent:
    def __init__(self,input_shape,n_output,id):
        self.id=id
        self.GAMMA=0.999             # The discount factor for normalizing future reward.
        self.BATCH_SIZE=128           # The chunk of states provisioned randomly for training.
        # ---------- Epsilon greedy strategy variables -------------#
        self.EPSILON_START=0.9       
        self.EPSILON_END=0.05
        self.EPSILON_DECAY=200
        #-----------------------------------------------------------#
        self.TARGET_UPDATE=10
        self.action_space=n_output
        '''
        The TARGET_VALUE is number of episodes after which the weights and biases of target network
        to be set as same as that of policy network. This provides stability to the model as 
        suggested in orignal DQN paper.
        '''
        self.MEMORY_SIZE=10000       # Experience replay memory capacity.
        MODEL=DQN(input_shape,n_output)
        self.policy_net=MODEL.getModelInstance()
        self.target_net=MODEL.getModelInstance()
        self.target_net.set_weights(self.policy_net.get_weights())
        self.memory=Experience(self.MEMORY_SIZE)
        self.time_step=0

    def selectAction(self,state):
        EPSILON_THRESHOLD=self.EPSILON_END + (self.EPSILON_START - self.EPSILON_END) * exp(-1 * self.time_step / self.EPSILON_DECAY)
        self.time_step+=1
        if random() > EPSILON_THRESHOLD:
            # Exploitation
            return self.policy_net.predict(state)
        else:
            # Exploration
            return randint(0,self.action_space)
    def optimize(self,episode_number):
        if len(self.memory) < self.BATCH_SIZE:
            print("Memory instances insuffcient for training!")
            return
        transitions=self.memory.sample(self.BATCH_SIZE)
        current_states=array([transition[0] for transition in transitions])
        current_q_values=self.policy_net.predict(current_states)
        new_states=array([transition[3] for transition in transitions])
        future_q_values=self.target_net.predict(new_states)
        X=[]
        Y=[]
        for index,(Current_State,Action,Reward,Next_State,done) in enumerate(transitions):
            if not done:
                max_future_q=np.max(future_q_values[index])
                new_q=Reward + self.GAMMA * max_future_q
            else:
                new_q=Reward
            current_q_value=current_q_values[index]
            current_q_value[Action]=new_q
            X.append(Current_State)
            Y.append(current_q_value)
        self.policy_net.fit(array(X),array(Y),batch_size=self.BATCH_SIZE,verbose=0,shuffle=False)
        if episode_number % self.TARGET_UPDATE == 0:
            self.target_net.set_weights(self.policy_net.get_weights())
    def update_memory(self,state,action,reward,next_state,done):
        self.memory.see((state, action, reward,next_state,done))
