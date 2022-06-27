from flask import Flask, redirect, render_template, request
from apis.route import api

app = Flask(__name__)


#Pour gerer les routes
app.register_blueprint(api)


@app.route('/', methods = ["POST", "GET"])
def login():

    if request.method == 'POST':
            
        return redirect('/admin')

    return render_template('pages/login.html')



@app.route('/a', methods = ["POST", "GET"])
def register():

    if request.method == 'POST':
        return redirect('/')
    
    return render_template('pages/register.html')




@app.route('/admin', methods = ["GET", "POST"])
def admin():

    if request.method == 'POST':
        print('hello')

    return render_template('pages/admin/admin.html')







@app.route('/archive')
def archive():
    return render_template('pages/admin/archive.html')

@app.route('/user')
def user():
    return render_template('pages/user/home.html')



@app.route('/tree', methods = ["GET", "POST"])
def tree():
    if request.method == 'POST':
        print('hello')
    return render_template('pages/user/tree.html')





@app.route('/chat')
def chat():
    return render_template('pages/user/chat.html')





if __name__=='__main__':
    app.run(debug=True,port=5000)