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
		firm=companies[randint(0,len(companies))].name
		obs, reward, done, info=market.step(action,id,firm)
