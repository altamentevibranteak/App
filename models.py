from flask_login import UserMixin
from datetime import datetime
from flask import flash
import mysql.connector

class Usuario_Comum(UserMixin):
    def __init__(self, id_usuario, nome, email, senha, telefone, genero, data_nascimento, tipo_usuario, data_criacao, status):
        self.id = id_usuario
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.genero = genero
        self.data_nascimento = data_nascimento
        self.tipo_usuario = tipo_usuario
        self.data_criacao = data_criacao
        self.status = status

    @property
    def is_active(self):
        return self.status == 'conta ativada'

    @property
    def is_authenticated(self):
        return True  # Alterar conforme sua lógica de autenticação

    @property
    def is_anonymous(self):
        return False  # Sempre que um usuário está logado, isso deve ser False

   
    def get_id(self):
        return self.id
    
    
class Feedback:
    def __init__(self, id_usuario, comentario, nota, data=None):
        self.id_usuario = id_usuario
        self.comentario = comentario
        self.nota = nota
        self.data = data or datetime.now()
        
# Classe que lida com as operações do banco para o Feedback
class FeedbackDB:
    def __init__(self, connection):
        self.connection = connection

    def criar_feedback(self, id_usuario, comentario, nota):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO feedback (id_usuario, comentario, nota, data)
                VALUES (%s, %s, %s, %s)
            """, (id_usuario, comentario, nota, datetime.now()))
            self.connection.commit()
            flash("Feedback registrado com sucesso!", "success")
        except mysql.connector.Error as err:
            flash(f"Erro ao registrar feedback: {err}", "danger")
        finally:
            cursor.close()

    def obter_feedbacks(self, id_usuario):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM feedback WHERE id_usuario = %s
        """, (id_usuario,))
        feedbacks = cursor.fetchall()
        cursor.close()
        return [Feedback(**feedback) for feedback in feedbacks]        
            