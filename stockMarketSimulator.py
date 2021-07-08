from random import choices,randint
from string import ascii_lowercase, ascii_uppercase, digits  
import gym
from numpy import array,inf,exp

class Company:
    def __init__(self,name,price,volume):
        # 'name' : String ; Represents name of the company.
        # 'dataset' : Pandas.DataFrame ; the DataFrame object corresponding to the company's stock market data.
        self.name=name
        self.price=price
        self.volume=volume
        self.holders=[]   

class StockMarket(gym.Env):
    def __init__(self,firms,sim_time):
        # 'firms' : [...] ; each element is object of "Company" class.
        # 'n_observations' : Integer ; representing the size of observation space.
        # 'actions' : Integer ; Number of permissible actions allowed in the market.  
        super(StockMarket,self).__init__()
        self.firms=firms
        self.index=1    # the point upto which the market is simulated.
        self.normalization_factor=10
        self.n_actions=3
        self.invester=[]
        #self.n_observations=n_observations
        #self.n_actions=n_actions
        self.investment={}
        self.balance={}
        self.n_firms=0
        self.sim_time=sim_time
        for i in self.firms:
            self.n_firms+=1
        self.action_space=gym.spaces.Discrete(self.n_actions)
        # Normalized prices will be returned as observation within the range of 0-1. 
        # Each observation will contain the n_observations steps of data (time series formalism).
        self.observation_space=gym.spaces.Box(low=array([-inf,0]),high=array([inf,inf]))
        # init_price_vector stores the initial price of all the partiipating companies.
        self.init_price_vector=[i.price for i in self.firms]
    def reset(self):
        for i,j in zip(self.firms,self.init_price_vector):
            i.price=j
            i.holders=[]
        self.index=1
        return self.next_observation()
    def generate_id(self):
        return ''.join(choices(ascii_uppercase + digits + ascii_lowercase, k = 10))
    def register(self,investment):
        flag=0
        while(flag==0):
            id=self.generate_id()
            if id not in self.invester:
                flag=1
                break
        self.invester.append(id)
        self.investment[id]=investment
        self.balance[id]=self.investment
        return id
    def next_observation(self,name):
        for i in self.firms:
            if i.name==name:
                obs=[i.price,i.volume]
        return obs
    def asset_balance(self,id):
        total=0
        for i in self.firms:
            if id in i.holders:
                total+=i.price
        return total
    def reward_function(self,id):
        return (self.balance[id] - self.investment[id] + self.asset_balance(id)) / self.normalization_factor 
    def step(self, action, id, name=None):
        status=self.take_action(action,id,name)
        self.update_prices()
        reward=self.reward_function()
        obs=self.next_observation(name)
        info={}
        if self.index>=self.sim_time or self.balance <= 0:
            self.index=1
            done=True
        else:
            done=False
            self.index+=1
        info["Status"]=status
        return obs, reward, done, info
    def take_action(self,action,id,name=None):
        if action==0:
            # buy order
            # a entity with unique identifier 'id' can only issue single buy order at an instant.
            for i in self.firms:
                if i.name==name: 
                    if i.volume <= 0:
                        return False   
                    self.balance[id]-=i.price
                    i.holders.append(id)
                    i.volume-=1
                    return True
        elif action==1:
            # hold
            return True 
        else:
            # sell order
            for i in self.firms:
                if i.name==name:   
                    self.balance[id]+=i.price
                    i.holders.remove(id)
                    i.volume+=1
                    return True            
    def update_prices(self):
        for i in self.firms:
            i.prices += exp(len(i.holders) / self.index)
    def render(self):
        print("<- Market ->")
        for i in self.firms:
            print(f"{i.name}    {i.price}   {i.volume} {len(i.holders)}")
        print("<- Players ->")
        for i in self.investment.keys():
            print(f"{i}     {self.investment[i]}    {self.balance[i]}")


if __name__=='__main__':
    firms=[]
    firms.append(Company('XYZ',2,200))
    market=StockMarket(firms,10)
    id=market.register(100)
    obs=market.reset()
    while(not done):
        action=randint(0,2)
        obs, reward, done, info = market.step(action,id,'XYZ')
        market.render()



    

        
        
        
        
        




