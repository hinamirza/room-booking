import sys
sys.setrecursionlimit(10**6)
from flask import Flask, redirect, render_template, request, session, url_for
from flask_admin import Admin, AdminIndexView, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import (LoginManager, UserMixin, current_user, login_user,
                         logout_user)
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'hinamirza886@gmail.com',
    MAIL_PASSWORD = 'vehdysgguaupvuow'
)
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/mydatabase'
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)
login = LoginManager(app)


@login.user_loader
def load_user(iduser):
    return User.query.get(iduser)

# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

class Book_Now(db.Model, UserMixin):
    ''' id, name, email, phone, rooms, guests, checkin, checkout'''
    __tablename__ = 'Book_Now'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50),  nullable=False)
    Email = db.Column(db.String(120),  nullable=False)
    Phone = db.Column(db.String(12),  nullable=False)
    Rooms = db.Column(db.Integer,  nullable=False)
    Guests = db.Column(db.String(12), nullable=False)
    Check_in = db.Column(db.String(12), nullable=False)
    Check_out = db.Column(db.String(12), nullable=False)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45),  nullable=False)
    password = db.Column(db.String(50),  nullable=False)


class ControlView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app, name = 'Delight Height',template_mode='bootstrap3')  #,base_template='admin/index.html'
admin.add_view(ControlView(Book_Now, db.session))
admin.add_view(ControlView(User, db.session))


@app.route("/", methods= ['GET', 'POST'])
def hotel_booking():
    if request.method=='POST':
        name =request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        rooms=request.form.get('rooms')
        guests=request.form.get('guests')
        checkin=request.form.get('checkin')
        checkout=request.form.get('checkout')
        
        ''' id, name, email, phone, rooms, guests, checkin, checkout'''
        entry = Book_Now(Name=name, Email=email, Phone = phone, Rooms=rooms, Guests=guests, Check_in=checkin, Check_out = checkout)
        
        if entry.Check_in > entry.Check_out:
            return "Please enter a valid checkin or checkout date"
        else:
            if entry.Rooms == '1':
                result = Book_Now.query.filter_by(Rooms ='1').first()
                if result :
                   return "Room is booked please try booking another room!"
                else:
                    db.session.add(entry)
                    db.session.commit()
                     
            elif entry.Rooms=='2':
                result = Book_Now.query.filter_by(Rooms ='2').first()
                if result :
                    return "Room is booked please try booking another room!"
                else:
                    db.session.add(entry)
                    db.session.commit() 
            elif entry.Rooms == '3':
                result = Book_Now.query.filter_by(Rooms ='3').first()
                if result :
                    return "Room is booked please try booking another room!"
                else:
                    db.session.add(entry)
                    db.session.commit() 
        
        mail.send_message('reserved room by you', sender = 'hinamirza886@gmail.com',recipients = [email],
                            body = "Your name: "+name+"\n"+"Room No:"+ rooms +"\n"+ "No. of persons: "+guests+"\n" + "Check-in: "+checkin+"\n" + "Check-out: "+checkout
                            )

        if entry:
            return redirect('/admin')
    return render_template('admin/index.html')


@app.route("/login", methods=['GET','POST'])
def login():
    # if('user' in session and session['user']) == User.password:
    #     return redirect('/admin')
    if request.method=='POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        user = User.query.filter_by(username=username).first()
        pas = User.query.filter_by(password = userpass).first()
        if user:
            if pas:
                login_user(user)
                return redirect('/admin')
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/login')








if __name__ == "__main__":
    app.run(debug=True)
