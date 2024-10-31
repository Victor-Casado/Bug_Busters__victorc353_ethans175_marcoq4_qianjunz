from flask import Flask
from flask import render_template   
from flask import request
from flask import session
from flask import redirect
from flask import url_for

app = Flask(__name__)
app.secret_key = 'haha'

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('response'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username:  # If a username is provided, log in the user
            session['username'] = username
            return redirect(url_for('response'))
        else:
            return 'Please enter a username!'
    return render_template('login.html')

# Allow only GET requests to the response page
@app.route('/response', methods=['GET'])
def response():
    if 'username' in session:
        return render_template('response.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        user = session['username']
        session.pop('username', None)
        return render_template('logout.html', username=user)
    return redirect(url_for('response'))

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
