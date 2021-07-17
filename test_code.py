import stockMarketSimulator as sim
from random import randint
import RL_Agent as trader
from numpy import argmax, array
import numpy as np
if __name__=='__main__':
	#n=int(input("Enter number of entities : "))
	companies=[]
	#for i in range(n):
		#name=input(f"Enter name of #entity[{i+1}] : ")
		#price=float(input(f"Enter the price of {name}'s share : "))
		#volume=int(input(f"Enter the volume of {name}'s share : "))
		#companies.append(sim.Company(name,price,volume))
	companies.append(sim.Company("A",2,100))
	companies.append(sim.Company("B",3,100))
	#time=int(input("Enter the quantum of simulation time : "))
	time=100
	market=sim.StockMarket(companies,time)
	users=[]
	#n_users=int(input("Enter the number of users : "))
	#for i in range(n_users):
	#	seed=float(input(f"Enter the amount of {i+1} user's investment : "))
	#	users.append(trader.Agent((len(companies),2),len(companies)*3,market.register(seed)))
	users.append(trader.Agent((len(companies),2),len(companies)*3,market.register(100)))
	users.append(trader.Agent((len(companies),2),len(companies)*3,market.register(200)))
	n_episodes=200
	for episode in range(n_episodes):
		done=market.reset()
		reward_aggregate=[]
		while(not done):
			market.render()
			uid=randint(0,len(users)-1)
			user=users[uid]
			obs=market.next_observation()
			action_firm=argmax(user.selectAction(array(obs).reshape(1,len(companies),-1)))
			action=action_firm % 3
			firm=companies[action_firm % len(companies)].name
			print(action_firm)
			#print(f"user={uid}; action={action} ; firm={firm}")
			new_obs, reward, done, info=market.step(action,user.id,firm)
			reward_aggregate.append(reward)
			users[uid].update_memory(array(obs),action_firm,reward,array(new_obs),done)
			for user in users:
				#print(user.id)
				user.optimize(episode)
		if episode % 20 == 0:
			print(f"[+] Average reward {episode+1}/{n_episodes} = {np.sum(array(reward_aggregate))/episode+1}")
