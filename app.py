from flask import Flask,request,redirect,url_for,session,flash,render_template
import test_code as runner
import json


app=Flask(__name__)
app.secret_key='QwErTY9934@123'

@app.route('/')
def analytics_portal():
	return render_template('simulator.html')
@app.route('/about')
def about():
	return render_template('about.html')	
@app.route('/analyze',methods=['POST'])
def analyze():
	'''
	In this function, the stock market simulator and trader agents will be initialized.
	'''
	if request.method=='POST':
		n_entity=int(request.form['n_entities'])
		entities={'Name' : [request.form['Name'+str(i)] for i in range(n_entity)], 
		'Price' : [int(request.form['Price'+str(i)]) for i in range(n_entity)],
		'Volume' : [int(request.form['Volume'+str(i)]) for i in range(n_entity)]
		}
		n_users=int(request.form['n_users'])
		users={'seed' : [int(request.form['seed'+str(i)]) for i in range(n_users)]}
		sim_time=int(request.form['sim_time'])
		n_episode=int(request.form['n_episode'])
		data={
			"n_entities" : n_entity,
			"entities" : [
				{"name" : entities['Name'][i], "price" : entities['Price'][i], "volume" : entities['Volume'][i]} for i in range(n_entity)
			],
			"simulaton_time" : sim_time,
			"n_users" : n_users,
			"users" : [{"seed" : users['seed'][j]} for j in range(n_users)],
			"n_episodes" : n_episode
		}
		with open('config.json','w') as output:
			json.dump(data,output)
		market_data=runner.driver()
	return render_template('report.html',report=market_data)