from flask import Flask, render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from mysql.connector import connect, Error
from auth import LoginForm, RegisterForm
from wtforms.validators import Email
from models import Usuario_Comum
from auth import auth_bp
from routes import routes_bp
import os
#from datetime import timedelta
from flask import current_app as app

app = Flask(__name__)
#app.secret_key = os.urandom(24)
#app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=5)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Configurações do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass_word'
app.config['MYSQL_DATABASE'] = 'dbschool_bot'

# Inicializa o login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Função para obter conexão com o banco de dados
def get_db_connection():
    connection = connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DATABASE']
    )
    return connection


# Definindo a classe User para o Flask-Login
class Usuario_Comum(UserMixin):
    def __init__(self, id_usuario, nome, email, telefone, genero, data_nascimento, tipo_usuario, data_criacao, status):
        self.id = id_usuario
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.genero = genero
        self.data_nascimento = data_nascimento
        self.tipo_usuario = tipo_usuario
        self.data_criacao = data_criacao
        self.status = status
        
        def get_id(self):
            return self.id

@login_manager.user_loader
def load_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario_comum WHERE id_usuario = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if user_data:
        return Usuario_Comum(
            id_usuario=user_data['id_usuario'],
            nome=user_data['nome'],
            email=user_data['email'],
            telefone=user_data['telefone'],
            genero=user_data['genero'],
            data_nascimento=user_data['data_nascimento'],
            tipo_usuario=user_data['tipo_usuario'],
            data_criacao=user_data['data_criacao'],
            status=user_data['status']
        )
    return None



# Registrar o Blueprint das rotas de autenticação
app.register_blueprint(auth_bp)

# Registrar o Blueprint das rotas de gerais
app.register_blueprint(routes_bp)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/interface')
@login_required
def interface():
    # conexao com o chatbot
    return render_template('interface.html')


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)


