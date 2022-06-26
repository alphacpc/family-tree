from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('pages/login.html')

@app.route('/a')
def register():
    return render_template('pages/register.html')

@app.route('/admin')
def admin():
    return render_template('pages/admin.html')

@app.route('/add')
def add():
    return render_template('pages/add_user.html')

@app.route('/archive')
def archive():
    return render_template('pages/archive.html')

@app.route('/user')
def user():
    return render_template('pages/home.html')

@app.route('/tree')
def tree():
    return render_template('pages/tree.html')

if __name__=='__main__':
    app.run(debug=True,port=5000)