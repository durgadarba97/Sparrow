import flask
import psycopg2
import json
import collections
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

conn = psycopg2.connect(database="sparrow", user = "sparrow", password ="password", host = "127.0.0.1", port = "5432")
cur = conn.cursor()


@app.route('/', methods=['GET'])
def home():
	return "<h1> Welcome to the App </h1>"

@app.route('/users', methods=['GET'])
def getusers():
	cur.execute("SELECT * FROM users")
	rows = cur.fetchall()
	conn.commit()
	arr = []
	dict = collections.OrderedDict()
	for i in rows:
		arr.append({"id" : i[0], "username" : i[1], "password" : i[2], "email" : i[3]})
		print(i)
	j = json.dumps(arr)
	print(type(j))
	return j

@app.route('/newuser', methods=['POST'])
def newuser():
	if not request.json:
        	abort(400)
	
	userjson = json.dumps(request.json)
	data = json.loads(userjson)
	print(data)
	cur.execute("INSERT INTO users(username, password, email) VALUES (%s, %s, %s)", (data["username"], data["password"], data["email"]))
	conn.commit()

	return "OK"


if __name__ == "__main__":
	app.run(host='0.0.0.0')
