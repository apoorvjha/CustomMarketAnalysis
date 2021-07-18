import stockMarketSimulator as sim
from random import randint
import RL_Agent as trader
from numpy import argmax, array
import numpy as np
from json import load

if __name__=='__main__':
	companies=[]
	users=[]
	with open("config.json",'r') as conf:
		config=load(conf)
	n_entities=config['n_entities']
	entities=config['entities']
	simulation_time=config['simulaton_time']
	n_users=config['n_users']
	investers=config['users']
	n_episodes=config['n_episodes']
	market=sim.StockMarket(companies,simulation_time)
	for i in entities:
		companies.append(sim.Company(i["name"],float(i["price"]),int(i["volume"])))
	for i in investers:
		users.append(trader.Agent((n_entities,2),n_entities*3,market.register(float(i["seed"]))))
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
			print(f"user={uid}; action={action} ; firm={firm}")
			new_obs, reward, done, info=market.step(action,user.id,firm)
			reward_aggregate.append(reward)
			users[uid].update_memory(array(obs),action_firm,reward,array(new_obs),done)
			for user in users:
				user.optimize(episode+1,done)
		if episode % 20 == 0:
			print(f"[+] Average reward {episode+1}/{n_episodes} = {np.sum(array(reward_aggregate))/episode+1}")
