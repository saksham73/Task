from flask import Flask, render_template,request, session, redirect, url_for
from pymongo import MongoClient
#from flask.ext.pymongo import PyMongo
from bot_response import botResponse, chat_history
from flask_pymongo import PyMongo
from flask_login import logout_user
import bcrypt

app = Flask(__name__)

#client=MongoClient("mongodb+srv://saksham:saksham@cluster0-nvuma.mongodb.net/test?retryWrites=true&w=majority")
#db=client.get_database('db')
#records=db.chats

#print(records.count_documents({}))

#chats_two={
	#'How is the weather' : 'Sunny',
#}

#records.insert(chats_two)

app.config['MONGO_DBNAME'] = 'db'
app.config['MONGO_URI'] = 'mongodb+srv://saksham:saksham@cluster0-nvuma.mongodb.net/test?retryWrites=true&w=majority'

mongo=PyMongo(app)


@app.route('/')
def index():
	if 'username' in session:
		return 'You are logged in as ' + session['username']

	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
	users = mongo.db.chat
	present_user = users.find_one({'name' : request.form['username']})

	if present_user:
		if(request.form['pass'] == present_user['password']):
		#if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
			session['username'] = request.form['username']
			return render_template('chat.html')
	

	return 'Wrong Credentials'

@app.route('/register', methods=['POST', 'GET'])
def register():
	if request.method == 'POST':
		users = mongo.db.chat
		present = users.find_one({'name' : request.form['username']})

		if present is None:
			#hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
			users.insert({'name' : request.form['username'],'E-mail' :  request.form['E-mail'],'password' : request.form['pass']})
			session['username'] = request.form['username']
			return render_template('chat.html')

		return 'username taken'

	return render_template('register.html')

@app.route("/bot_response", methods = ["GET","POST"] )
def resp():
	data = request.json
	#chat_history(session["username"])
	return botResponse(data["user"], session["username"])


#@app.route("/hellogreeting", methods = ["GET","POST"])
#def greeting():
#	name= session["username"]
#	return 'Hi'+name
@app.route("/get_uname", methods = ["GET","POST"] )
def uname():
    if(session["username"] != ""):
        a = chat_history(session["username"])
        r = {"username":session["username"], 'bot':a['bot'], 'user':a['user']}
        return r
    return ""

@app.route('/logout')
def logout():
    if 'username' in session:
    	session.pop('username',None)
    	return redirect(url_for('index'))

    else:
    	return 'User already logged out.'

if __name__=='__main__':
	app.secret_key = 'mysecret'
	app.run(debug=True)

