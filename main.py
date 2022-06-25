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

if __name__=='__main__':
    app.run(debug=True,port=5000)