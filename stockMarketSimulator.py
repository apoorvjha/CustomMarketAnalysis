from random import choices,randint,random
from string import ascii_lowercase, ascii_uppercase, digits  
import gym
from numpy import array,inf,exp

class Company:
    def __init__(self,name,price,volume):
        # 'name' : String ; Represents name of the company.
        # 'price' : Float ; Initial Public Offering price of the stock.
        # 'volume' : Integer ; Unit share the company is willing to offer.
        # 'holders' : List [AlphaNumeric] ; Unique identifiers of each trader who currently owns the stake of the firm. 
        self.name=name
        self.price=price
        self.volume=volume
        self.holders=[]   

class StockMarket(gym.Env):
    def __init__(self,firms,sim_time):
        # 'firms' : [Company] ; each element is object of "Company" class.
        # 'index' : Integer ; The quantum of time upto which the simulation has been done.
        # 'normalization_factor' : Integer ; Normalizes the reward function into the desired limit.
        # 'n_actions' : Integer ; The permissible size of action space.
        # 'invester' : [AlphaNumeric] ; Unique identifiers of each tradercurrently taking part in the market activities.
        # 'investment' : Dictionary=>AlphaNumeric->Float ; Key value pair to track the initial investment of each trader.
        # 'balance' :  Dictionary=>AlphaNumeric->Float ; Key value pair to track the current cash balance of the trader.
        # 'n_firms' : Integer ; Total number of firms whose shares are available for trade.
        # 'sim_time' : Integer ; The total permissible amount of time upto which the simulation would run.
        # 'action_space' : Integer ; The permissible range of action values.
        # 'observation_space' : Float ; The permissible range of observation values.
        # 'init_price_vector' : [Float] ; The initial price values which will be used to reset the simulator to it's orignal checkpoint.
        super(StockMarket,self).__init__()
        self.firms=firms
        self.index=1     
        self.normalization_factor=10
        self.n_actions=3
        self.invester=[]
        self.investment={}
        self.balance={}
        self.n_firms=0
        self.sim_time=sim_time
        for i in self.firms:
            self.n_firms+=1
        self.action_space=gym.spaces.Discrete(self.n_actions)
        self.observation_space=gym.spaces.Box(low=array([-inf,0]),high=array([inf,inf]))
        self.init_price_vector=[i.price for i in self.firms]
    def reset(self,name):
        for i,j in zip(self.firms,self.init_price_vector):
            i.price=j
            i.holders=[]
        self.index=1
        return self.next_observation(name)
    def generate_id(self):
        return ''.join(choices(ascii_uppercase + digits + ascii_lowercase, k = 10))
    def register(self,seed):
        flag=0
        while(flag==0):
            id=self.generate_id()
            if id not in self.invester:
                flag=1
                break
        self.invester.append(id)
        self.investment[id]=seed
        self.balance[id]=seed
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
        reward=self.reward_function(id)
        obs=self.next_observation(name)
        info={}
        if self.index>=self.sim_time or self.balance[id] <= 0:
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
                    self.balance[id]-= i.price
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
                    if id not in i.holders:
                        return False   
                    self.balance[id]+= i.price
                    i.holders.remove(id)
                    i.volume+=1
                    return True            
    def update_prices(self):
        # Need improvement in the price upfate strategy.
        for i in self.firms:
            i.price += exp(len(i.holders) / self.index) - (random() * len(self.invester) / self.index)
    def render(self):
        print(self.index)
        print("         <- Market ->")
        for i in self.firms:
            print(f"    {i.name}    {i.price}   {i.volume} {len(i.holders)}")
        print("         <- Players ->")
        for i in self.investment.keys():
            print(f"    {i}     {self.investment[i]}    {self.balance[i]}   {self.asset_balance(i)}")


if __name__=='__main__':
    firms=[]
    firms.append(Company('XYZ',2,200))
    market=StockMarket(firms,10)
    uid=[market.register(100)]
    obs=market.reset('XYZ')
    done=False
    while(not done):
        action=randint(0,2)
        id=uid[0]
        obs, reward, done, info = market.step(action,id,'XYZ')
        print(f"Reward = {reward}")
        market.render()



    

        
        
        
        
        




