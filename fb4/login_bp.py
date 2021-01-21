'''
Created on 19.01.2021

@author: wf
'''
from flask import Blueprint, redirect,render_template,request, flash, Markup, jsonify, url_for
from flask_wtf import FlaskForm, CSRFProtect
from flask_login import LoginManager,UserMixin
from flask_login import current_user, login_user,logout_user, login_required
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length
from fb4.sqldb import db
from werkzeug.security import generate_password_hash,check_password_hash

class LoginBluePrint(object):
    
    instance=None
    '''
    a blueprint for logins
    '''
    def __init__(self,app,name:str,welcome:str="index",template_folder:str=None):
        '''
        construct me
        
        Args:
            name(str): my name
            welcome(str): the welcome page
            template_folder(str): the template folder
            
        '''
        self.name=name
        self.welcome=welcome
        if template_folder is not None:
            self.template_folder=template_folder
        else:
            self.template_folder='templates'    
        self.blueprint=Blueprint(name,__name__,template_folder=self.template_folder)
        self.app=app
        login = LoginManager(app)
        self.login=login
        self.hint=None
        app.register_blueprint(self.blueprint)
        
        @app.route('/login',methods=['GET', 'POST'])
        def loginForm():
            return self.loginForm()
                    
        @app.route('/logout')
        @login_required
        def logout():
            return self.logOut()
        
        @login.user_loader
        def load_user(userid):
            return User.query.get(userid)
        
    def loginForm(self):
        '''
        show the login form
        '''
        form = LoginForm()
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.checkPassword(form.password.data):
                flash('Invalid username or password')
                if self.hint is not None:
                    flash(self.hint)
                return redirect(url_for('loginForm'))
            login_user(user, remember=form.rememberMe.data)
            return redirect(url_for(self.welcome))
        return render_template('login.html', form=form)
    
    def logOut(self):
        logout_user()
        return redirect(url_for(self.welcome))
    
    def addUser(self,db,username,password):
        '''
        add a user with the given username and password
        
        Args:    
            db: the SqlAlchemy database connection
            username(str): the username for the user
            password(str): the password for the user - only a hash will be stored
        '''
        u=User(id=1,username=username)
        u.setPassword(password)
        db.session.add(u)
        db.session.commit()

class LoginForm(FlaskForm):
    '''
    a form with username/password
    '''
    username = StringField('Username', validators=[DataRequired(), Length(1, 50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 150)])
    rememberMe = BooleanField('Remember me')
    submit = SubmitField('Login')

# User handling
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


