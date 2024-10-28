from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import connect, Error
from flask import session
from models import Usuario_Comum
from routes import routes_bp
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo
import os


auth_bp = Blueprint('auth', __name__)

# conexão com o banco de dados
def get_db_connection():
    connection = connect(
        host='localhost',
        user='root',
        password='pass_word',
        database='dbschool_bot'
    )
    return connection

# Registro de usuário
@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = RegisterForm()  # Cria uma instância do formulário
    if form.validate_on_submit():  # Verifica se o formulário foi submetido e é válido
        nome = form.nome.data
        email = form.email.data
        telefone = form.telefone.data
        genero = form.genero.data
        data_nascimento = form.data_nascimento.data
        senha = generate_password_hash(form.senha.data, method='pbkdf2:sha256')
        tipo_usuario = form.tipo_usuario.data

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
    "INSERT INTO usuario_comum (nome, email, telefone, genero, data_nascimento, senha, tipo_usuario, status) VALUES (%s, %s, %s, %s, %s, %s, %s, 'conta ativada')",
    (nome, email, telefone, genero, data_nascimento, senha, tipo_usuario)
)

        connection.commit()
        cursor.close()
        connection.close()

        flash('Conta criada com sucesso! Faça login.')
        return redirect(url_for('auth.login'))

    return render_template('cadastro.html', form=form)

# Login de usuário
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario_comum WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        cursor.close()
        connection.close()
        

        if user_data and check_password_hash(user_data['senha'], senha):
            user = Usuario_Comum(
                id_usuario=user_data['id_usuario'],
                nome=user_data['nome'],
                email=user_data['email'],
                senha=user_data['senha'],
                telefone=user_data['telefone'],
                genero=user_data['genero'],
                data_nascimento=user_data['data_nascimento'],
                tipo_usuario=user_data['tipo_usuario'],
                data_criacao=user_data['data_criacao'],
                status=user_data['status']
            )
            
            # Salva o id_usuario na sessão para uso em outras rotas
            session['user_id'] = user_data['id_usuario']
            
            # Autentica o usuário
            login_user(user)
            flash('Login bem-sucedido', 'Sucess')
            
             # Redireciona para a próxima página ou para a interface principal
            next_page = request.args.get('next')
            return redirect(next_page or url_for('interface'))
        else:
            flash('Email ou senha incorretos', 'danger') 
    return render_template('login.html', form=form)

    id_usuario = session['user_id'] = id_usuario
    return redirect('/interface')  # Redireciona o usuário após o login


# Logout de usuário
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso!', 'success')
    return redirect(url_for('home'))


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    genero = SelectField('Gênero', choices=[('Masculino', 'Masculino'), ('Feminino', 'Feminino')], validators=[DataRequired()])
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirm_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    tipo_usuario = SelectField('Tipo de Usuário', choices=[('Aluno', 'Aluno'), ('Professor', 'Professor'), ('Funcionario', 'Funcionário')], validators=[DataRequired()])
    submit = SubmitField('Registrar')


auth_bp.register_blueprint(routes_bp)

