from random import choices,randint,random
from string import ascii_lowercase, ascii_uppercase, digits  
import gym
from numpy import array,inf,exp,float64
from matplotlib import pyplot as plt

class Company:
    def __init__(self,name,price,volume):
        # 'name' : String ; Represents name of the company.
        # 'price' : Float ; Initial Public Offering price of the stock.
        # 'volume' : Integer ; Unit share the company is willing to offer.
        # 'holders' : List [AlphaNumeric] ; Unique identifiers of each trader who currently owns the stake of the firm.
        # 'lock' : Boolean ; For conurrency control. 
        self.name=name
        self.price=price
        self.volume=volume
        self.holders=[]
        self.lock=False
        self.init_price=self.price
        self.init_volume=self.volume
    def getLock(self):
        if self.lock == False:
            self.lock=True
    def releaseLock(self):
        if self.lock == True:
            self.lock=False 
    def reset(self):
        self.price=self.init_price
        self.volume=self.init_volume
        self.holders=[]
        self.lock=False
class StockMarket(gym.Env):
    '''
    Multi-Agent (More than one agent can interact simultaneously) 
    Multi-Asset (More than one firm can be part of the market) 
    Stock market simulation environment.
    '''
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
        # 'held_volume' : Dictionary=>AlphaNumeric->List ; To track the volume holdings of each trader and stock. 
        # 'init_price_vector' : [Float] ; The initial price values which will be used to reset the simulator to it's orignal checkpoint.
        super(StockMarket,self).__init__()
        self.firms=firms
        self.index=1     
        self.normalization_factor=10
        self.n_actions=3
        self.invester=[]
        self.investment={}
        self.balance={}
        self.held_volume={}
        self.n_firms=0
        self.sim_time=sim_time
        for i in self.firms:
            self.n_firms+=1
        self.action_space=gym.spaces.Discrete(self.n_actions)
        self.observation_space=gym.spaces.Box(low=array([-inf,0]),high=array([inf,inf]),dtype=float64)
        #self.init_price_vector=[i.price for i in self.firms]
        #self.init_vol_vector=[i.volume for i in self.firms]
    def reset(self):
        '''
        The 'price' and 'holders' list of each 'Company' object in 'firms' list will be set to the initial_price_vector and
        empty list respectively.
        The 'index' is set to 1.
        The balance of each trader is set to the initial 'investment' of that trader.
        Returns : Boolean ; This value is used to denote the 'done' value which is used for halting the simulation.   
        '''
        self.dataset_firms={i.name : {"Price" : [],"Volume" : [],"Holders" : []} for i in self.firms}
        self.dataset_trader={i : {"Cash_Balance" : [],"Asset_Balance" : []} for i in self.investment.keys() }
        for i in self.firms:
            i.reset()
        self.index=1
        self.held_volume={}
        for i in self.investment.keys():
            self.balance[i]=self.investment[i]
            self.held_volume[i]=[]
            for j in self.firms:
                self.held_volume[i].append([j.name, 0])
        return False
    def generate_id(self):
        '''
        Returns : AlphaNumeric ; Returns the random string of Alphanumeric characters which will act as unique identifier of each trader of
        length 10 which can be increased or decreased based on the expected userbase.
        Example : length=10 can incorporate 62^10 unique users.
        '''
        return ''.join(choices(ascii_uppercase + digits + ascii_lowercase, k = 10))
    def register(self,seed):
        # 'seed' : Float ; Initial investment provided by the trader who is willing to egister into the simulator.
        '''
        Tries to generate a random string of AlphaNumeric characters untill a unique string is found which is not allocated to any
        trader yet.
        The invester is registered by appending the unique identifier hence generated into the 'invester' list.
        The 'investment' and 'balance' of the trader is also initialized with the 'seed' provided as argument.
        Returns : AlphaNumeric ; The unique identifier of the user allocated into the system.  
        '''
        flag=0
        while(flag==0):
            id=self.generate_id()
            if id not in self.invester:
                flag=1
                break
        self.invester.append(id)
        self.investment[id]=seed
        self.balance[id]=seed
        self.held_volume[id]=[]
        for i in self.firms:
            self.held_volume[id].append([i.name, 0])
        return id
    def next_observation(self,name=None):
        # 'name' : String ; Name of the firm whose observation is intended by the user.
        '''
        From the 'firms' list searches for the firm having the name same as provided as argument. 
        If the match is found then returns list containing 'price' and 'volume' of the unit shares of the firm;
        Otherwise returns the empty list.
        If name is not specified then returns the observation regarding entire list of 'firms'.
        Returns  : List ; Observation 
        '''
        obs=[]
        if name == None : 
            for i in self.firms:
                obs.append([i.price,i.volume]) 
        else:
            for i in self.firms:
                if i.name==name:
                    obs.append([i.price,i.volume])
        return obs
    def asset_balance(self,id):
        # 'id' : AlphaNumeric ; The unique identifier of the trader.
        '''
        Calculates and returns the valuation of the asset holdings interms of the stocks. 
        Returns : Float ; asset valuation
        ''' 
        total=0
        for i in self.firms:
            if id in i.holders:
                for j in range(len(self.held_volume[id])):
                    total+=i.price * self.held_volume[id][j][1] 
        return total
    def lockStatus(self,name):
        # 'name' : String ; Name of the firm whose observation is intended by the user.
        '''
        Checks the value of lock variable associated with corresponding asset for which agent has issued a trade order. 
        Returns : Boolean ; The status of lock variable.
        '''
        for i in self.firms:
            if i.name==name:
                if i.lock==True:
                    return True
        return False
    def reward_function(self,id):
        # 'id' : AlphaNumeric ; The unique identifier of the trader.
        '''
        Self curated reward policy which needs to be optimized to inturn optimize the performance in the simulated market. 
        Returns : Float ; Reward value (Normalized by the 'normalization_factor')
        '''        
        return (self.balance[id] - self.investment[id] + self.asset_balance(id)) / self.normalization_factor 
    def step(self, action, id, name=None):
        # 'action' : Integer ; The Integer mapping of the action that the agent/trader is willing to take.
        # 'id' : AlphaNumeric ; The unique identifier of the trader.
        # 'name' : String ; Name of the firm whose observation is intended by the user.
        '''
        Driver method to take the 'action' specified by the trader and collect the status of the action in the market, Update the 
        price of each firm's stock based on the curated policy, Compute and collect the reward received by the trader, Obtain the 
        observation of the environment after taking the action and checks if the simulation reached the time threshold specified in 
        'sim_time' or any of the traders becomes bankrupt.
        Returns : List, Float, Boolean, Dictionary ; Observation, reward , halting status and status of action.  
        '''
        if self.lockStatus(name):
            status=False
        else:
            for i in self.firms:
                if i.name==name:
                    i.getLock()
            status=self.take_action(action,id,name)
            for i in self.firms:
                if i.name==name:
                    i.releaseLock()
        self.update_prices()
        reward=self.reward_function(id)
        obs=self.next_observation()
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
        # 'action' : Integer ; The Integer mapping of the action that the agent/trader is willing to take.
        # 'id' : AlphaNumeric ; The unique identifier of the trader.
        # 'name' : String ; Name of the firm whose observation is intended by the user.
        '''
        if action=0, Then buy order is executed for the corresponding trader and firm whose name and unique identifier is supplied 
        respectively.
        if action=2, Then sell order is executed for the corresponding trader and firm whose name and unique identifier is supplied 
        respectively.
        If action=1, Then the nothing is done and signifies holding whatever shares the trader holds currently.
        After executing the corresponding actions, the execution status is returned for diagnostic purposes.
        Returns : Boolean ; Diagnostic value corresponding to the execution status of the action.
        '''        
        if action==0:
            for i in self.firms:
                if i.name==name: 
                    if i.volume <= 0:
                        return False   
                    self.balance[id]-= i.price
                    if id not in i.holders:
                        i.holders.append(id)
                    i.volume-=1
                    for j in range(len(self.held_volume[id])):
                        if self.held_volume[id][j][0]==name:
                            self.held_volume[id][j][1]+=1
                    return True
        elif action==1:
            return True 
        else:
            for i in self.firms:
                if i.name==name:
                    if id not in i.holders:
                        return False   
                    self.balance[id]+= i.price
                    for j in range(len(self.held_volume[id])):
                        if self.held_volume[id][j][0]==name:
                            self.held_volume[id][j][1]-=1
                    for j in range(len(self.held_volume[id])):
                        if self.held_volume[id][j][0]==name and self.held_volume[id][j][1] <= 0:
                            i.holders.remove(id)
                    i.volume+=1
                    return True            
    def update_prices(self):
        '''
        Curated policy to update price of each firms shares.
        '''
        for i in self.firms:
            i.price += exp(-1 * i.price / self.index) * (random() * len(i.holders)/len(self.invester)+1) - random() / self.index + random() / self.index
    def render(self):
        '''
        Renders the state of the stock market after every iteration of trade.
        '''
        print()
        print(f"# Iteration : {self.index}")
        print()
        print("#--------------------------------------Market Metadata---------------------------------------------#")
        print("Company Name",end="")
        for i in range(35-len("Company Name")):
            print(end=" ")
        print(" Price",end="")
        for i in range(15-len("Price")):
            print(end=" ")
        print(" Volume",end="")
        for i in range(15-len("Volume")):
            print(end=" ")
        print(" Number of Holders")
        print("-----------------------------------------------------------------------------------------------")
        for col in self.firms:
            print(col.name,end="")
            for i in range(30-len(col.name)):
                print(end=" ")
            print("|   ",round(col.price,3),end="")
            for i in range(10-len(str(round(col.price,3)))):
                print(end=" ")
            print("|   ",round(col.volume,3),end="")
            for i in range(10-len(str(round(col.volume,3)))):
                print(end=" ")
            print("|   ",len(col.holders))
        print()
        print("#--------------------------------------Player Metadata---------------------------------------------#")
        print("Invester ID",end="")
        for i in range(35-len("Invester ID")):
            print(end=" ")
        print(" Seed Amount",end="")
        for i in range(15-len("Seed Amount")):
            print(end=" ")
        print(" Cash Balance",end="")
        for i in range(15-len("Cash Balance")):
            print(end=" ")
        print(" Asset Balance")
        print("-----------------------------------------------------------------------------------------------")
        for col in self.investment.keys():
            print(col,end="")
            for i in range(30-len(col)):
                print(end=" ")
            print("|   ",round(self.investment[col],3),end="")
            for i in range(10-len(str(round(self.investment[col],3)))):
                print(end=" ")
            print("|   ",round(self.balance[col],3),end="")
            for i in range(10-len(str(round(self.balance[col],3)))):
                print(end=" ")
            print("|   ",round(self.asset_balance(col),3))
        print()
    def renderUI(self,mode="info"):
        if mode=="debug":
            data=""
            data+="<hr><br><h2>"+f"# Iteration : {self.index}"+"</h2><br>"
            data+="<center><h2><u>Market Metadata</u></h2></center><br>"
            data+="<center><table>"
            data+="<tr>"
            data+="<th>Company Name</th>"
            data+="<th>Price</th>"
            data+="<th>Volume</th>"
            data+="<th>Number of Holders</th>"
            data+="</tr>"
            for col in self.firms:
                data+="<tr>"
                data+=f"<td>{col.name}</td>"
                data+=f"<td>{round(col.price,3)}</td>"
                data+=f"<td>{round(col.volume,3)}</td>"
                data+=f"<td>{len(col.holders)}</td>"
                data+="</tr>"
            data+="</table></center>"
            data+="<center><h2><u>Player Metadata</u></h2></center><br>"
            data+="<center><table>"
            data+="<tr>"
            data+="<th>Invester ID</th>"
            data+="<th>Seed</th>"
            data+="<th>Cash Balance</th>"
            data+="<th>Asset Balance</th>"
            data+="</tr>"
            for col in self.investment.keys():
                data+="<tr>"
                data+=f"<td>{col}</td>"
                data+=f"<td>{round(self.investment[col],3)}</td>"
                data+=f"<td>{round(self.balance[col],3)}</td>"
                data+=f"<td>{round(self.asset_balance(col),3)}</td>"
                data+="</tr>"
            data+="</table></center>"
            data+="<br>"
            for col in self.firms:
                self.dataset_firms[col.name]["Price"].append(round(col.price,3))
                self.dataset_firms[col.name]["Volume"].append(round(col.volume,3))
                self.dataset_firms[col.name]["Holders"].append(len(col.holders))
            for col in self.investment.keys():
                self.dataset_trader[col]["Cash_Balance"].append(round(self.balance[col],3))
                self.dataset_trader[col]["Asset_Balance"].append(round(self.asset_balance(col),3))
            return data
        elif mode=="info":
            for col in self.firms:
                self.dataset_firms[col.name]["Price"].append(round(col.price,3))
                self.dataset_firms[col.name]["Volume"].append(round(col.volume,3))
                self.dataset_firms[col.name]["Holders"].append(len(col.holders))
            for col in self.investment.keys():
                self.dataset_trader[col]["Cash_Balance"].append(round(self.balance[col],3))
                self.dataset_trader[col]["Asset_Balance"].append(round(self.asset_balance(col),3))
            return ""            
        else:
            return None
    def plot(self,ep):
        entity_frames=[]
        agent_frames=[]
        for col in self.firms:
            plt.xlabel("Price")
            plt.ylabel("Holders")
            plt.title(f"Price versus Holders for {col.name} entity")
            plt.plot(self.dataset_firms[col.name]["Price"],self.dataset_firms[col.name]["Holders"],linewidth=2)
            plt.savefig(f"./static/plots/{col.name}{ep}.png")
            entity_frames.append(f"./static/plots/{col.name}{ep}.png")
            plt.close()
        for col in self.investment.keys():
            plt.xlabel("Cash_Balance")
            plt.ylabel("Asset_Balance")
            plt.title(f"Cash_Balance versus Asset_Balance for {col} agent")
            plt.plot(self.dataset_trader[col]["Cash_Balance"],self.dataset_trader[col]["Asset_Balance"],linewidth=2)
            plt.savefig(f"./static/plots/{col}{ep}.png")
            agent_frames.append(f"./static/plots/{col}{ep}.png")
            plt.close()
        return entity_frames,agent_frames






    

        
        
        
        
        




