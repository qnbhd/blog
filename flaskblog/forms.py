from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User, Post


class RegistrationForm(FlaskForm):
    username = StringField('Логин',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Пользователь c таким именем уже существует! Выберите другое имя пользователя.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Пользователь с таким почтовым адресом уже существует! '
                                  'Выберите другое имя пользователя.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class UpdateAccountForm(FlaskForm):
    username = StringField('Логин',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Обновить аватар вашего профиля', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        if username.data == current_user.username:
            return
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Пользователь c таким именем уже существует! Выберите другое имя пользователя.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if email.data == current_user.email:
            return
        if user:
            raise ValidationError('Пользователь с таким почтовым адресом уже существует! '
                                  'Выберите другое имя пользователя.')


class PostingForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(min=10)])
    content = TextAreaField('Текст поста', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Запросить сброс пароля')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Пользователя с таким email не существует. Вы можете быть первым!')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Сбросить пароль')