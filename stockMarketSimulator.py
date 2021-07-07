import yfinance  
import gym
from numpy import zeros,ones,int8,float16

class Company:
    def __init__(self,name,dataset,price,volume):
        # 'name' : String ; Represents name of the company.
        # 'dataset' : Pandas.DataFrame ; the DataFrame object corresponding to the company's stock market data.
        self.name=name
        self.dataset=dataset
        # 'n_features' essentially returns the number of columns in the provided dataframe. 
        self.n_features=len(list(dataset.to_dict().keys()))
        self.price=price
        self.holders=[]   

class StockMarket(gym.Env):
    def __init__(self,firms,n_observations,n_actions):
        # 'firms' : [...] ; each element is object of "Company" class.
        # 'n_observations' : Integer ; representing the size of observation space.
        # 'actions' : Integer ; Number of permissible actions allowed in the market.  
        super(StockMarket,self).__init__()
        self.firms=firms
        self.index=0    # the point upto which the market is simulated.
        self.n_observations=n_observations
        self.n_actions=n_actions
        self.n_features=self.firms.n_features
        self.n_firms=0
        for i in self.firms:
            self.n_firms+=1
        self.action_space=gym.spaces.Box(low=zeros((self.n_firms,self.n_actions)),high=ones((self.n_firms,self.n_actions)),dtype=int8)
        # Normalized prices will be returned as observation within the range of 0-1. 
        # Each observation will contain the n_observations steps of data (time series formalism).
        self.observation_space=gym.spaces.Box(low=0,high=1,shape=(self.n_firms,self.n_observations,self.n_features),dtype=float16)
        # init_price_vector stores the initial price of all the partiipating companies.
        self.init_price_vector=[i.price for i in self.firms]
    def reset(self):
        for i,j in zip(self.firms,self.init_price_vector):
            i.price=j
            i.holders=[]
        self.index=0
        return self._next_observation()
    def _next_observation(self):
        pass 
        
        
        
        
        




