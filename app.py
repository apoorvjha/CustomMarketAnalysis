from flask import Flask,request,redirect,url_for,session,flash,render_template
import test_code as runner

app=Flask(__name__)
app.secret_key='QwErTY9934@123'

@app.route('/')
def analytics_portal():
	return render_template('simulator.html')
@app.route('/analyze')
def analyze():
    '''
	In this function, the stock market simulator and trader agents will be initialized.
	'''
	pass