from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('pages/login.html')



@app.route('/a', methods = ["POST", "GET"])
def register():
    return render_template('pages/register.html')






@app.route('/admin')
def admin():
    return render_template('pages/admin/admin.html')

@app.route('/add')
def add():
    return render_template('pages/admin/add_user.html')

@app.route('/archive')
def archive():
    return render_template('pages/admin/archive.html')

@app.route('/user')
def user():
    return render_template('pages/user/home.html')

@app.route('/tree')
def tree():
    return render_template('pages/user/tree.html')

@app.route('/member')
def member():
    return render_template('pages/user/member.html')

@app.route('/chat')
def chat():
    return render_template('pages/user/chat.html')

if __name__=='__main__':
    app.run(debug=True,port=5000)