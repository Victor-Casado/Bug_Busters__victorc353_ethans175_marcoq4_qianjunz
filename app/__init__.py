from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

    return render_template('signup.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login.html'))

    return render_template('home.html', stories=stories)

@app.route('/view/<int:story_id>')
def view_story(story_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('viewStory.html', story=story)

@app.route('/create', methods=['GET', 'POST'])
def create_story():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('createStory.html')

@app.route('/edit/<int:story_id>', methods=['GET', 'POST'])
def edit_story(story_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('editStory.html', story=story)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
