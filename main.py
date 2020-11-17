from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from MysqlConn import connector
app = Flask(__name__)
cors = CORS(app)

def verifyContact(c_id):
	conn = connector.connect()
	c = conn.cursor()
	print(c_id)
	try:
		c.execute("SELECT * FROM users WHERE user_id=%s", (str(c_id),))
		contact = c.fetchone()
		c_id_actual = contact[0]
		return c_id_actual
	except:
		return -1

@app.route('/')
def test():
    return "Hello from Alex"

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

@app.route('/addContact', methods=['POST'])
def addContact():
	conn = connector.connect()
	c = conn.cursor()
	data = request.get_json()
	u_id = data['user_id']
	c_id = data['contact_id']
	c_id_actual = verifyContact(c_id)
	sql = "INSERT INTO contacts (user_id, contact_id) VALUES(%s, %s)"
	val = (u_id, c_id_actual)
	try:
		if (c_id_actual == -1):
			raise ValueError("No Such User Found")
		c.execute(sql,val)
		conn.commit()
		return jsonify({"message":"contact successfully added"})
	except ValueError as e:
		return jsonify({"message":"No Such User Found"})
	except:
		return jsonify({"message": "contact unable to be added"})

@app.route('/removeContact', methods=['POST'])
def removeContact():
	conn = connector.connect()
	c = conn.cursor()
	data = request.get_json()
	u_id = data['user_id']
	c_id = data['contact_id']
	c_id_actual = verifyContact(c_id)
	print(c_id_actual)
	sql = "DELETE FROM contacts WHERE user_id=%s AND contact_id=%s"
	val = (u_id, c_id_actual)
	try:
		if(c_id_actual == -1):
			raise ValueError("No Such User Found")
		c.execute(sql, val)
		conn.commit()
		return jsonify({"message": "contact successfully removed"})
	except ValueError:
		return jsonify({"message": "No Such User Found"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
