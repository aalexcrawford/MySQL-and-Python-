from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from MysqlConn import connector
app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def test():
    return "Hello from Flask!"

@app.route('/loginUser')
def verifyLogin():
	conn = connector.connect()
	c = conn.cursor()
	data = request.get_json()
	uName = data['user_name']
	hashPassword = data['hashed_password']
	try:
		c.execute("SELECT user_id FROM users WHERE user_name=%s AND hashed_password=%s", (str(uName), str(hashPassword)))
		rows = c.fetchone()
		return jsonify({"user_id":rows[0]})
	except:
		print("No such user found")
		return jsonify({"user_id":"-1"})

@app.route('/newUser', methods = ['POST'])
def createUser():
	conn = connector.connect()
	c = conn.cursor()
	data = request.get_json()
	uName = data['user_name']
	hPassword = data['hashed_password']
	eMail = data['email']
	val = (uName, hPassword, eMail)
	sql = "INSERT INTO users (user_name, hashed_password, email) VALUES (%s, %s, %s)"
	try:
		c.execute(sql, val)
		conn.commit()
		return jsonify({"user_id":"Welcome " + uName})
	except:
		print("Failed to create user")
		return jsonify({"user_id":"error creating user account"})

# The /request is how we are going to differ between different queries i.e. /requestUserData or /requestContactData
@app.route('/test', methods=['POST'])
def printFromJSON():
	conn = connector.connect()
	#data = request.get_json() gets the entire JSON
	data = request.get_json()
	#userID = data['id'] get the specific variable in the JSON
	userID = data['id']

	return '''user ID is {}'''.format(userID)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
