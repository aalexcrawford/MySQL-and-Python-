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

def validatePassword(u_id, old_pass):
	conn = connector.connect()
	c = conn.cursor()
	sql = "SELECT user_id FROM users WHERE user_id=%s AND hashed_password=%s"
	val = (u_id, old_pass)
	try:
		c.execute(sql, val)
		u_id_actual = c.fetchone()
		print("Able to validate Password")
		return u_id_actual[0]
	except:
		print("Error Validating Password")
		return -1

def verifyUsername(u_name):
	conn = connector.connect()
	c = conn.cursor()
	sql = "SELECT * FROM users WHERE user_name=%s"
	val = (u_name,)
	try:
		c.execute(sql, val)
		conn.commit()
		return -1
	except:
		return 0

@app.route('/')
def test():
	return "Hello from InCognito"

@app.route('/loginUser', methods = ['POST'])
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
	flag = verifyUsername(u_name)
	sql = "INSERT INTO users (user_name, hashed_password, email) VALUES (%s, %s, %s)"
	val = (u_name, h_password, e_mail)
	try:
		if(flag == -1):
			raise ValueError("Username is already used")
		c.execute(sql, val)
		conn.commit()
		return jsonify({"user_name":"Welcome " + u_name})
	except ValueError:
		return jsonify({"message":"Username is already used"})
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
	sql = "INSERT INTO contacts (user_id, contact_id) VALUES(%s, %s)'"
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
	except:
		return jsonify({"message":"Unable to remove contact"})

@app.route('/changePass', methods = ['POST'])
def changePass():
	conn = connector.connect()
	c = conn.cursor()
	data = request.get_json()
	u_id = data['user_id']
	old_h_password = data['old_hashed_password']
	new_h_password = data['new_hashed_password']
	flag = validatePassword(u_id, old_h_password)
	val = (new_h_password,u_id)
	sql = "UPDATE users SET hashed_password=%s WHERE user_id=%s"
	try:
		if(flag == -1):
			raise ValueError("Incorrect password")
		c.execute(sql, val)
		conn.commit()
		return jsonify({"message":"password updated"})
	except ValueError:
		return jsonify({"message":"Incorrect password"})
	except:
		return jsonify({"message":"password was unable to be changed"})

@app.route('/sendMessage', methods = ['POST'])
def sendMessage():
	conn = connector.connect()
	c = conn.cursor()
	data = request.get_json()
	m = data['message']
	s_id = data['sender']
	r_id = data['receiver']
	val = (m, s_id, r_id)
	sql = 'INSERT INTO messages(message, sender, receiver, time) VALUES (%s, %s, %s, unix_timestamp()) '
	try:
		c.execute(sql, val)
		return jsonify({"message":"Message sent"})
	except:
		return jsonify({"message":"Unable to send message"})

@app.route('/getMessages', methods = ['POST'])
def getMessages():
    conn = connector.connect()
    cursor = conn.cursor()
    data = request.get_json()
    val = (data['user_id'],data['contact_id'], data['contact_id'], data['user_id'])
    sql = """
SELECT sender, receiver, message, time FROM messages 
WHERE sender=%s AND receiver=%s
OR sender=%s AND receiver=%s 
ORDER BY time desc;    """
    cursor.execute(sql, val)
    rv = cursor.fetchall()
    payload = []
    content = {}
    for result in rv:
        content = {'sender': result[0], 'receiver': result[1], 'message': result[2], 'time': result[3]}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/getContacts', methods = ['POST'])
def getContacts():
    conn = connector.connect()
    c = conn.cursor()
    data = request.get_json()
    condition = (data['user_id'],)
    sql = "SELECT contact_id FROM contacts WHERE user_id=%s"
    c.execute(sql, condition)
    contacts = []
    for contact in c.fetchall():
        contacts.append(contact[0])
    return jsonify({"contacts" : contacts})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
