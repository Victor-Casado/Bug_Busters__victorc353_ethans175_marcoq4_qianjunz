from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import db

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

@app.route('/')
def home():
    # CHECK DB FOR USER HERE
    if 'username' in session:
        render_template('home.html')
        #render_template('home.html', stories=stories) #list of 2d strings which are story titles
        #as the first entry and id as the second entry
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    #if request.method == 'POST':
    #    username = request.form['username']
    #    password = request.form['password']
    #    return redirect(url_for('home'))
    baseReturn = "Enter your username and password below to proceed."
    if request.method == 'POST':
        #takes all username + password checks if there is a match returns to login.html if there isnt
        #passUser = db.getPassword(request.form['username'])
        '''
        if passUser == null:
            return redirect(url_for('home'))
        if passUser == request.form['password']:
            session[request.form['username']] = passUser
            '''
        userInfo = db.allUserData()
        for i in userInfo:
            if userInfo[i] == request.form['username'] + ',' + request.form['password']:
                session[request.form['username']] = request.form['password']
                return redirect(url_for('home'))
            baseReturn = "Wrong username and password. Please try again."
    return render_template('login.html', statement = baseReturn)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        userInfo = db.allUserData()
        baseReturn = "Enter your desired username and password below to proceed."
        #STORE USER IN DB
        if password == password2:
            for i in userInfo:
                stringUserData = userInfo[i]
                stringUserData.split(",")
                if(stringUserData[0] == username):
                    return redirect(url_for('home'))
                if(stringUserData[1] == password):
                    return redirect(url_for('home'))
            session[username] = password
            db.addUser(username, password)
            return redirect(url_for('home'))
        else:
            baseReturn = "Your desired username and password do not match please try again."

    return render_template('signup.html', statement = baseReturn)

@app.route('/view')
def view_story(story_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('viewStory.html', story=story)

@app.route('/create', methods=['GET', 'POST'])
def create_story():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('createStory.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit_story(story_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('editStory.html', story=story) #story should ONLY be the most recent entry

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
