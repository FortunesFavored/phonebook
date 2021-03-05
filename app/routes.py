from app import App, db
from flask import render_template, request, flash, redirect, url_for
from app.forms import UserInfoForm, gamePost, LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash


@App.route('/')
@App.route('/index')
def index():
    return render_template('index.html', title='Lucky | Home')


@App.route('/register', methods=["GET", "POST"])
def register():
    Form = UserInfoForm()
    if request.method == 'POST' and Form.validate():
        username = Form.username.data
        email = Form.email.data
        address = Form.address.data
        phone = Form.phone.data
        password = Form.password.data
        new_user = User(username, email, password, address, phone)
        db.session.add(new_user)
        db.session.commit()
        flash('You have made an account', 'success')
        return render_template('index.html', title='Lucky | Home')
        print(username,email,password)
    return render_template('register.html', title='Lucky | Register', form=UserInfoForm())


@App.route('/submitGame', methods=["GET", "POST"])
@login_required
def submitGame():
    Post = gamePost()
    if request.method == 'POST' and Post.validate():
        game = Post.game.data
        content = Post.content.data
        print(game, content)
    return render_template('submitGame.html', post=gamePost())

@App.route('/login', methods=['GET', 'POST'])
def login():
    Title = "Lucky | Login"
    form = LoginForm()
    if request.method == 'POST' and form.validate:
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password, password):
            flash('That password or email is not correct.', 'danger')
            return redirect(url_for(login))
        login_user(user, remember = form.remember_me)
        flash('You have been logged in.', 'success')
        next_page = request.args.get('next')
        if next_page:

            return redirect(url_for(next_page.lstrip('/')))
        return redirect(url_for('index'))
    return render_template('login.html', title = "Lucky | Login", form=LoginForm())


@App.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.  You have lost the game.')
    return redirect(url_for('index'))
