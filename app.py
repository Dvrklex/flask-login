from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secretaa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flask_login'

db=SQLAlchemy(app)
login_manager = LoginManager(app)




class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, name, lastname, email, password):
        self.username = username
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = password
    
    def __str__(self):
        return self.username
    
    def is_active(self):
        return True
    def get_id(self):
        return self.id
    def check_password(self, password):
        return self.password == password
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    return render_template('profile.html')

def check_db(userid):
    user = User.query.filter_by(id=userid).first()
    return user

@login_manager.user_loader
def load_user(id):
     return check_db(id)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password_log']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('profile'),
                            usu=user.username)
        else:
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

# Tomar datos del registro y guardarlos en la base de datos
@app.route('/register_user/',methods=['POST'])
def save_user():
    print('entra en el metodo save_user')
    if request.method=='POST':
        #Recuperar datos del formulario
        username=request.form['username']
        name=request.form['name']
        lastname=request.form['lastname']
        email=request.form['email']
        password=request.form['password']
        #Creo el objeto usuario
        user=User(username,name,lastname,email,password)
        #Guardo el usuario en la base de datos
        db.session.add(user)
        db.session.commit()
        flash('Usuario registrado correctamente')
        print('Usuario registrado correctamente')
        return redirect(url_for('login'))





if __name__ == '__main__':
    app.run(debug=True)