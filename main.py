from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from MysqlConn import connector
app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def test():
    return "Hello from Pycharm"

@app.route('/loginUser')
def verifyLogin():
	conn = connector.connect()
	c = conn.cursor()
	data = request.get_json()
	u_name = data['user_name']
	h_password = data['hashed_password']
	sql = "SELECT user_id FROM users WHERE user_name=%s AND hashed_password=%s"
	val = (str(u_name), str(h_password))
	try:
		c.execute(sql, val)
		u_id = c.fetchone()
		return jsonify({"user_id":u_id[0]})
	except:
		print("No such user found")
		return jsonify({"user_id":"-1"})

@app.route('/newUser', methods = ['POST'])
def createUser():
	conn = connector.connect()
	c = conn.cursor()
	data = request.get_json()
	u_name = data['user_name']
	h_password = data['hashed_password']
	e_mail = data['email']
	sql = "INSERT INTO users (user_name, hashed_password, email) VALUES (%s, %s, %s)"
	val = (u_name, h_password, e_mail)
	try:
		c.execute(sql, val)
		conn.commit()
		return jsonify({"user_name":"Welcome " + uName})
	except:
		print("Failed to create user")
		return jsonify({"user_name":"error creating user account"})

# The /request is how we are going to differ between different queries i.e. /requestUserData or /requestContactData
@app.route('/test', methods=['POST'])
def addContact():
	conn = connector.connect()
	c = conn.cursor()
	data = request.get_json()
	u_id = data['user_id']
	c_id = data['contact_id']
	sql = "INSERT INTO contacts (contact_id) VALUES(%S) WHERE user_id=%s"
	val = (c_id, u_id)
	try:
		c.execute(sql,val)
		return jsonify({"message":"contact successfully added"})
	except:
		return jsonify({"message":"contact unable to be added"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
