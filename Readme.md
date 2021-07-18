				      					# Phases of the project
## Brainstorming 
The end result of this project is an Algorithmic trading bot that can make optimal/sub-optimal trading decisions in the inhouse simulated environment. The simulated stock market is created using the data that dynamically gets generated based on the actions of the agents and random fluctuations coded into the price update policy. 

The bot will be trainned using Reinforcement learning paradigm which allows for optimization of actions based on the reward received from the simulator. 

The architecture of the project can be thought as two isolated environments communicating through the gateway. The components are Simulator and Trading bot, which will use the rest API to communicate with one another.

The simulator is planned to be developed in such a way that it can be beneficial and usable outside the scope of this project and same design thinking is put into the Trading bot as well. This is important for me that even though someone who wants to test either their own market condition or machine learning model, cannot feel left out and can build upon either of the components of this project.

For the sake of experimentation I will be incorporating some subset of RL as well as some other timeseries forecasting models into the test so as to benchmark the RL baed solution with respect to traditional models.

## Simulator
The open AI gym library is used as blueprint for our simulator and former is inherited in the later. The Entities/Assets of the market is defined in Company class. The list of such Company class objects will be passed into the the StockMarket class. The later is capable of maneuvering the asset's price in the market based on the curated price update policy which can be tweaked to change the nature of the market. In my perception I have adoped the policy of overall progressing market with certain random fluctions exploded with respect to the number of trading agents. This inherently simulates inflation. The reaward which a trader receives is also curated and is subjective decision of the person using this simulator. The reward heavily supports liquidity as asset valuation and diference between initial investment and balance amount arethe key factors for the same.
Following are possible ways which one can use to run the simulator : 
	1. Imporing the code.
		a. Create a new python file as [FILE_NAME].py
		b. Inside the created python file write below code,
			import stockMarketSimulator as sim
			from random import randint
			if __name__=='__main__':
				n=int(input("Enter number of entities : "))
				companies=[]
				for i in range(n):
					name=input(f"Enter name of #entity[{i+1}] : ")
					price=float(input("Enter the price of {name}'s share : "))
					volume=int(input("Enter the volume of share : "))
					companies.append(sim.Company(name,price,volume))
				time=int(input("Enter the quantum of simulation time : "))
				market=sim.StockMarket(companies,time)
				users=[]
				n_users=int(input("Enter the number of users : "))
				for i in range(n_users):
					seed=float(input("Enter the amount to invest : "))
					users.append(market.register(seed))
				done=market.reset()
				while(not done):
					market.render()
					action=market.action_space.sample()
					id=users[randint(0,len(users)-1)]
					firm=companies[randint(0,len(companies)-1)].name
					obs, reward, done, info=market.step(action,id,firm)
		c. Execute the newly created file using the below command,
			$python3 [FILE_NAME].py
	2. Alternatively, the same code as part 1b can be written at the end of the file stockMarketSimulator.py excluding the import part and droping the prefix "sim.". The updated code an then be executed as below,
	$python3 stockMarketSimulator.py
# Note : The Snippet described here is provide as a seperte file as test_code.py for instances if you do not want to go through pain of writing one for yourself. 
#Note : The Simulator is modified to incorporat concurrency control by using lock on the asset untill the transaction/trade order has been completed.
# Reinforcement Learning agent
The RL_Agent.py contains code for defining the architecture of deep learning network based on the paradigm discussed in DQN paper for solving problems with continous observation spaces. The constraint of this architecture is that it does not work for realm outside discrete action space. To deal with such shortcomming a more versatile but computationally exensive architecture is prescribed in literature as DDPG which is outside scope of this project. Since, our action space is discrete so we need to get into that pathway. The Epsilon greedy strategy is used to choose appropriate actions for the agents as it provides a balanced opportunity to the agents to explore and exploit. The gaussian smoothing operation is used to degrade the value of epsilon. The discount factor used is very high as used in many literary articles I have read. The experience replay memory is used to break the shackles of order dependency of states. Finally the configuration related to multiagent multi entity framework is defined in a JSON file which may gets generated dynamically on request of a web server implementing restfull architecture to provide API for leveraging the agent and simulated environment functinality.

