from flask import Flask, render_template, request, redirect, url_for, session
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'whatever_you_want'

# Connect to the database
# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='',
#                              database='laundryapp',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)

# Handles GET form submission
@app.route('/query-example', methods=['GET'])
def query_example():
    date1 = request.args.get('date1')
    date2 = request.args.get('date2')

    # Any actual logic that you want to implement

    return render_template('query_example.html', date1=date1, date2=date2)

# Handles POST form submission
@app.route('/form-example', methods=['POST'])
def form_example():
    data1 = request.form.get('data1')
    data2 = request.form.get('data2')
    data = {
        'data1': data1,
        'data2': data2
    }

    # Any actual logic that you want to implement

    return render_template('form_example.html', data=data)
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
    pass

@app.route('/login', methods=['POST'])
def login():
    # Verify username and password here
    session['logged_in'] = True
    return redirect(url_for('protected'))

#Authenticates the register
@app.route('/customerRegisterAuth', methods=['GET', 'POST'])
def customerRegisterAuth():
	#grabs information from the forms
	username = request.form['email address']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES(%s, %s)'
		cursor.execute(ins, (username, password))
		conn.commit()
		cursor.close()
		return render_template('index.html')#Authenticates the register
     
@app.route('/staffRegisterAuth', methods=['GET', 'POST'])
def staffregisterAuth():
	#grabs information from the forms
	username = request.form['email address']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES(%s, %s)'
		cursor.execute(ins, (username, password))
		conn.commit()
		cursor.close()
		return render_template('index.html')

# Basic protected route example
@app.route('/protected', methods=['GET'])
def protected():
    if session.get('logged_in'):
        # let the user see the protected page
        return render_template('protected.html')
    else:
        # otherwise redirect to somewhere else
        return render_template('unauthorized.html')
    
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
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


@app.route('/check_user_role')
def check_user_role():
    # please complete this function
    #query the database to check if the user is a staff
    # if the user is a staff, take them to the staff profile page. otherwise, take them to the customer profile page
    # if is_user_staff(user_id): 
    #     return redirect('/staff_profile.html')
    # else:
    #     return redirect('/customer_profile.html')
    pass 


@app.route('/confirmService', methods=['POST'])
def confirmService():
    #  please complete this function
    # query the database and input to confirm the service
    pass


@app.route('/customerProfile')
def customerProfile():
    #  please complete this function
    # query the database to get the customer profile which will be used in customer_profile.html
    # user_id = session.get('user_id')
    # if not user_id:
    #     # Redirect to login page if the user is not logged in
    #     return redirect(url_for('login'))

    # # Connecting to the database
    # conn = get_db_connection()
    # cursor = conn.cursor(dictionary=True)

    # # Fetching user data
    # cursor.execute("SELECT email_address, password, first_name, last_name, address, phone_number, date_of_birth FROM users WHERE id = %s", (user_id,))
    # personal_info = cursor.fetchone()
     # Fetch order details
    # cursor.execute("SELECT * FROM `order` WHERE email_address = %s ORDER BY purchase_date_time DESC", (user_email,))
    # orders = cursor.fetchall()
    # cursor.close()
    # conn.close()

    # # Check if personal_info is not None
#    return render_template('customer_profile.html', personal_info=personal_info, orders=orders)    
    pass

@app.route('/edit_personal_info')
def edit_personal_info():
    # Assuming user_id is stored in session
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    # Fetch and pass user information to the template
    # Redirect or render an editing form
    return render_template('edit_personal_info.html')

@app.route('/cancel_order/<order_id>')
def cancel_order(order_id):
    # Logic to cancel the order
    # Redirect back to the profile or order page
    return redirect(url_for('customer_profile'))

@app.route('/edit_order/<order_id>')
def edit_order(order_id):
    # Fetch order details for editing
    # Redirect or render an editing form
    return render_template('edit_order.html', order_id=order_id)

@app.route('/reorder/<order_id>')
def reorder(order_id):
    # Logic to duplicate and reorder based on existing order details
    # Redirect back to the profile or order page
    return redirect(url_for('customer_profile'))

@app.route('/average_order_weight')
def average_order_weight():
    # Fetch the average order weight
    # Redirect or render the average order weight page
    # return render_template('average_order_weight.html')
    pass 

@app.route('/total_revenue')
def total_revenue():
    # Fetch the total revenue
    # calculate the total revenue of all the orders 
    pass

@app.route('/machine_utilization')
def machine_utilization():
    # Fetch the machine utilization
    # calculate the machine utilization
    pass

@app.route('/confirmed_orders')
def confirmed_orders():
    # Fetch the confirmed orders
    # Fetch all the confirmed orders
    pass


@app.route('/')
def index():
    return render_template('customer_profile.html')

if __name__ == '__main__':
    app.run(debug=True)