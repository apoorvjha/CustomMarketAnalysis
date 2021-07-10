''' 
policy : state -> action ; The policy is the strategy to make moves based on the observations it makes about
the environment.

Time series forecasting models are models that can anticipate input space with tempoal dimension/dependency. Most common ones are LSTM 
and CNN. 

Q-Learning is the method through which an optimal policy is learned by optimizing the 'Q' value associated with
the policy adopted. Provided markov property is adhered i.e. states are unique & distinguishable and future states
are dependent on current state.The agent is confered with epsilon-greedy strategy for balanced exploitation and exploration tradeoff.
The replay memory will store the last 'N' onservations along with the action, previous observation and reward received. The sample 
from this replay memory will be drawn at random to refrain the order dependency incurring in the model.

The observation/state space of the stock market is continous as we can observe the price of stocks and volume 
available for trade. This is the reason I am not using q-tables and move on with Deep Q Networks (DQNs).
Apart from this, I am also going to use some benchmark models like LSTM and CNN which are inherently good with 
time series data which we have in our hand. 
'''
# Note : The cuda toolkit version 11.4 has been isntalled to leverage the computation speed of GPU for data transformation jobs. 
# The extraction and loading of data from the disk if much faster in CPU and left to that by default.
# Ensure that cuDNN version 8.x library is properly installed.

