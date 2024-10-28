from flask import Blueprint
from flask import render_template, redirect, request, jsonify, session
import mysql.connector
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from datetime import datetime

#blueprint para definir as rotas
routes_bp = Blueprint('routes', __name__)

# conexao com o banco de dados
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='pass_word',
    database='dbschool_bot'
)

# Função para adicionar feedback
def adicionar_feedback(id_usuario, comentario, nota):
    try:
        cursor = conexao.cursor()
        data_atual = datetime.now()
        consulta = """
            INSERT INTO feedback (id_usuario, comentario, nota, data)
            VALUES (%s, %s, %s, %s)
        """
        valores = (id_usuario, comentario, nota, data_atual)
        cursor.execute(consulta, valores)
        conexao.commit()
        print("Feedback adicionado com sucesso!")
    except mysql.connector.Error as erro:
        print("Erro ao adicionar o feedback: {erro}")
    finally:
        cursor.close()
        
        
# Exemplo de uso
adicionar_feedback(1, "Ótimo aplicativo! Muito útil e intuitivo.", 9)    
    

#@routes_bp.route('/area_aluno')
#def aluno():
 #   return "Esta é a area do aluno!"

#@routes_bp.route('/area_docente')
#def docente():
 #   return "Funcionando!"

@routes_bp.route('/configuracao')
def config():
    return "Area de configuração"


@routes_bp.route('/feedback', methods=['POST'])
def fedeback():
    # Verifique se o usuário está logado
    if 'user_id' not in session:
        return jsonify({"error": "Usuário não autenticado"}), 403

    id_usuario = session['user_id']  # Obtém o id_usuario da sessão
    data = request.get_json()
    comentario = data.get("comentario")
    nota = data.get("nota")
    
    if not comentario or not nota:
        return jsonify({"error": "Comentario e nota sao obrigatorios"}), 400
    
    adicionar_feedback(id_usuario, comentario, int(nota))
    return jsonify({"message": "Feedback recebido com sucesso"}), 200

@routes_bp.route('/visitante')
def test():
    return render_template('visitante.html')

