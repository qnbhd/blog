import os
import secrets

from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostingForm, RequestResetForm, ResetPasswordForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

ADMIN_ID = 5


def crypt_password(pw):
    pw_hash = bcrypt.generate_password_hash(pw).decode('utf-8')
    return pw_hash


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    all_posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=all_posts)


@app.route('/about')
def about():
    user = User.query.filter_by(id=ADMIN_ID).first()
    if user is not None:
        image_file = url_for('static', filename='profile_pics/' + user.image_file)
        return render_template('about.html', user=user, image_file=image_file)
    else:
        return 'Not found', 404


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=crypt_password(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash(f'Ваш аккаунт был успешно создан! Теперь вы можете войти', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next', 'home')
            return redirect(next_page)

        else:
            flash('Ошибка входа. Пожалуйста, проверьте ваши данные входа', 'danger')
    return render_template('login.html', title='Вход', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.split(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            print(form.picture.data)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Данные вашего аккаунты были успешно обновлены', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        print(current_user.image_file)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Вход', image_file=image_file, form=form)


@app.route("/post/new", methods=['POST', 'GET'])
@login_required
def posting():
    form = PostingForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Пост был успешно создан!', 'success')
        return redirect(url_for('home'))
    return render_template('posting.html', title='Новый пост', form=form)


@app.route('/user/<string:username>')
def user_page(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        page = request.args.get('page', 1, type=int)
        all_posts = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
        image_file = url_for('static', filename='profile_pics/' + user.image_file)
        return render_template('user_page.html', user=user, posts=all_posts, image_file=image_file)
    else:
        return 'Not found', 404


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostingForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Ваш пост был успешно изменен!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('posting.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Ваш пост был успешно удален!', 'success')
    return redirect(url_for('home'))


@app.route("/reset_password", methods=['POST', 'GET'])
def reset_request():
    pass
