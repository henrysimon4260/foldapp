from flask import Flask, render_template, request, redirect, url_for, session
import pymysql.cursors
import random
import time

app = Flask(__name__)
app.secret_key = 'whatever_you_want'

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='laundryapp',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
# Handles initial routing
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/staffLogin')
def staffLogin():
    return render_template('staffLogin.html')

# Handles login authentication
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	email_address = request.form['email_address']
	password = request.form['password']
	cursor = connection.cursor()
	#executes query
	query = "SELECT * FROM customer WHERE email_address = %s and password = %s" 
	cursor.execute(query, (email_address, password))
	#stores the results in a variable
	dataCustomer = cursor.fetchone()
	cursor.close()
	
	error = None
	if(dataCustomer):
		#creates a session for the the user
		#session is a built in
		session['email_address'] = email_address 
		return render_template('index.html')
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)@app.route('/loginAuth', methods=['GET', 'POST'])

@app.route('/staffLoginAuth', methods=['GET', 'POST'])
def staffLoginAuth():
	#grabs information from the forms
	email_address = session['email_address']
	cursor = connection.cursor()
	query = 'SELECT * FROM laundry_company_staff WHERE email_address = %s'
	cursor.execute(query, (email_address)) 
	staff_info = cursor.fetchone()
	cursor.close()
	cursor = connection.cursor()
	query = 'SELECT * FROM order_table'
	cursor.execute(query) 
	orderData = cursor.fetchall()
	cursor.close()
	
	error = None
	if(staff_info):
		#creates a session for the the user
		#session is a built in
		session['email_address'] = email_address 
		return render_template('staff_profile.html',  staff_info = staff_info, orders = orderData)
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)
#Authenticates the register
@app.route('/customerRegisterAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	
	email_address = request.form['email_address']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	address = request.form['address']
	phone_number = request.form['phone_number']
	date_of_birth = request.form['date_of_birth']  
	#cursor used to send queries
	cursor = connection.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email_address = %s'
	cursor.execute(query, (email_address))
	#stores the results in a variable
	customerData = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(customerData):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('login.html', error = error)
	else:
		ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (email_address, password, first_name, last_name, address, phone_number, date_of_birth))
		connection.commit()
		cursor.close()
		session['email_address'] = email_address
		return render_template('index.html')

#Authenticates the register
@app.route('/confirm_order', methods=['GET', 'POST'])
def confirm_order():
	#grabs information from the forms
	
	order_ID = str(random.randint(1,500))
	email_address = str(session['email_address'])
	weight = int(request.form['weight'])
	price = float(weight)*1.75
	order_status = "awaiting pickup"
	pickup_date_time =  time.ctime(time.time() + 3600)
	delivery_date_time = time.ctime(time.time()+21600)
	address =  '160 E 3rd Street' # replace w request.form['address'] 
	route_ID = 1
	instructions = request.form['instructions']
	purchase_date_time = time.ctime(time.time())
	#cursor used to send queries
	cursor = connection.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email_address = %s'
	cursor.execute(query, (email_address))
	#stores the results in a variable
	customerData = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	ins = 'INSERT INTO order_table VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
	cursor.execute(ins, (order_ID, email_address, delivery_date_time, price, order_status, pickup_date_time, address, route_ID, instructions, weight, purchase_date_time ))
	connection.commit()
	cursor.close()
	return render_template('payment.html', totalprice = price)

@app.route('/staffRegisterAuth', methods=['GET', 'POST'])
def staffRegisterAuth():
	#grabs information from the forms
	email_address = request.form['email_address']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	address = request.form['address']
	phone_number = request.form['phone_number']
	date_of_birth = request.form['date_of_birth']
	#cursor used to send queries
	cursor = connection.cursor()
	#executes query
	query = 'SELECT * FROM laundry_company_staff WHERE email_address = %s'
	cursor.execute(query, (email_address))
	#stores the results in a variable
	data = cursor.fetchone()
	cursor = connection.cursor()
	query = 'SELECT * FROM order_table'
	cursor.execute(query) 
	orderData = cursor.fetchall()
	cursor.close()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		cursor = connection.cursor()
		ins = 'INSERT INTO laundry_company_staff VALUES(%s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (email_address, password, first_name, last_name, address, phone_number, date_of_birth))
		connection.commit()
		cursor = connection.cursor()
		query = 'SELECT * FROM laundry_company_staff WHERE email_address = %s'
		cursor.execute(query, (email_address)) 
		staff_info = cursor.fetchone()
		cursor.close()
		cursor = connection.cursor()
		query = 'SELECT * FROM order_table'
		cursor.execute(query) 
		orderData = cursor.fetchall()
		cursor.close()
		return render_template('staff_profile.html',  staff_info = staff_info, orders = orderData) 
# Handles GET form submission
@app.route('/confirmService', methods=['POST'])
def confirmService():
	#grabs information from the forms
	
	email_address = session['email_address']
	card_number = request.form['cardNumber']
	cvc = request.form['cvc']
	name = request.form['cardName']
	expirationMonth = request.form['expirationMonth']
	expirationYear = request.form['expirationYear']  
	#cursor used to send queries
	cursor = connection.cursor()
	#executes query
	#stores the results in a variable
	#use fetchall() if you are expecting more than 1 data row
	ins = 'INSERT INTO payment_methods VALUES(%s, %s, %s, %s, %s, %s)'
	cursor.execute(ins, (email_address, card_number,cvc, name, expirationMonth, expirationYear))
	connection.commit()
	cursor.close()
	return render_template('index.html')

# @app.route('/cancel_order')
# def confirmService():
# 	#grabs information from the forms
	
# 	order_Id = order.order_ID
	 
# 	#cursor used to send queries
# 	cursor = connection.cursor()
# 	#executes query
# 	#stores the results in a variable
# 	#use fetchall() if you are expecting more than 1 data row
# 	for 
# 	ins = 'DELETE from payment_methods VALUES(%s, %s, %s, %s, %s, %s)'
# 	cursor.execute(ins, (email_address, card_number,cvc, name, expirationMonth, expirationYear))
# 	connection.commit()
# 	cursor.close()
# 	return render_template('staffLoginAuth.html')

# Handles POST form submission

from functools import wraps

# This is a decorator that will make the route only accessible to logged in users
# Make sure to import functools
def protected_route(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        if session.get('logged_in'):
            return route(*args, **kwargs) # Direct to the actual function implementation
        else:
            return render_template('unauthorized.html') # Redirect to unauthorized page or whatever of your choice
    return wrapper

# Works just like /protected, but using a decorator
@app.route('/protected2', methods=['GET'])
@protected_route
def protected2():
    return render_template('protected.html')
    
# Set the logged_in session variable to False
# The naming does not matter, whether it is logged_in or just username, it is just a key in the session dictionary
# Just make sure setting it to false or popping it from the session dictionary will let the current user not pass the protected route check anymore
@app.route('/customerProfile')
def customerProfile():
    
    email_address = session['email_address']
    cursor = connection.cursor()
    query = 'SELECT * FROM customer WHERE email_address = %s'
    cursor.execute(query, (email_address)) 
    customerData = cursor.fetchone()
    cursor.close()
    cursor = connection.cursor()
    query = 'SELECT * FROM order_table WHERE email_address = %s'
    cursor.execute(query, (email_address)) 
    orderData = cursor.fetchall()
    cursor.close()
    
    return render_template('customer_profile.html', customerData = customerData, orderData = orderData )

app.route('/StaffProfile')
def customerProfile():
    email_address = session['email_address']
    cursor = connection.cursor()
    query = 'SELECT * FROM laundry_company_staff WHERE email_address = %s'
    cursor.execute(query, (email_address)) 
    staff_info = cursor.fetchone()
    cursor.close()
    cursor = connection.cursor()
    query = 'SELECT * FROM order_table'
    cursor.execute(query) 
    orderData = cursor.fetchall()
    cursor.close()
    return render_template('staff_profile.html',  staff_info = staff_info, orders = orderData)

@app.route('/logout')
def logout():
	return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
	
