import stockMarketSimulator as sim
from random import randint
import RL_Agent as trader
from numpy import argmax, array
import numpy as np
from json import load

def driver():
	companies=[]
	users=[]
	data=""
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
		users.append(trader.Agent([n_entities,2],n_entities*3,market.register(float(i["seed"]))))
	for episode in range(n_episodes):
		done=market.reset()
		reward_aggregate=[]
		while(not done):
			market.render()
			data=market.renderUI(mode="info")
			uid=randint(0,len(users)-1)
			user=users[uid]
			obs=market.next_observation()
			action_firm=user.selectAction(array(obs).reshape(1,n_entities,2))
			action=argmax(action_firm[0]) % 3
			firm=companies[argmax(action_firm[0]) % n_entities].name
			#print(f"user={uid}; action={action} ; firm={firm}")
			new_obs, reward, done, info=market.step(action,user.id,firm)
			reward_aggregate.append(reward)
			users[uid].update_memory(array(obs),action_firm,reward,array(new_obs),done)
			for user in users:
				user.optimize(episode+1,done)
		entity_frames,agent_frames=market.plot(episode+1)
		if episode+1 % 5 == 0:
			print(f"[+] Average reward {episode+1}/{n_episodes} = {np.sum(array(reward_aggregate))/episode+1}")
		if data!=None:
			data+="<br><center><h1>Visualization Dashboard</h1></center><br><br>"
			data+="<h3>Entity Plots</h3><br>"
			frame=0
			data+="<table>"
			while(frame<len(entity_frames)):
				data+="<tr>"
				data+='<td><img class="plots" src="'+ entity_frames[frame] +'"></td>'
				frame+=1
				if frame<len(entity_frames):
					data+='<td><img class="plots" src="'+ entity_frames[frame] +'"></td>'
					frame+=1
				data+="</tr>"
			data+="</table><br>"
			data+="<h3>Agent Plots</h3><br>"
			frame=0
			data+="<table>"
			while(frame<len(agent_frames)):
				data+="<tr>"
				data+='<td><img class="plots" src="'+ agent_frames[frame] +'"></td>'
				frame+=1
				if frame<len(agent_frames):
					data+='<td><img class="plots" src="'+ agent_frames[frame] +'"></td>'
					frame+=1
				data+="</tr>"
			data+="</table><br>"
			
	return data