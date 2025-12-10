# modelos.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Familiar(db.Model):
    __tablename__ = 'familiares'

    id_familiar = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20), unique=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    idosos = db.relationship('Idoso', backref='responsavel', lazy='dynamic')

    def to_dict(self):
        return {
            "id": self.id_familiar,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "data_cadastro": self.data_cadastro.isoformat() if self.data_cadastro else None
        }

class Idoso(db.Model):
    __tablename__ = 'idosos'

    id_idoso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_familiar_responsavel = db.Column(db.Integer, db.ForeignKey('familiares.id_familiar'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    lembretes = db.relationship('Lembrete', backref='idoso', lazy='dynamic')
    logs = db.relationship('LogConversa', backref='idoso_log', lazy='dynamic')

class Lembrete(db.Model):
    __tablename__ = 'lembretes'

    id_lembrete = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_idoso = db.Column(db.Integer, db.ForeignKey('idosos.id_idoso'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    horario = db.Column(db.Time, nullable=False)
    # Status mapeado como string no SQLAlchemy, mas validado pelo Enum do banco
    status_hoje = db.Column(db.String(10), default='pendente') 
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

class LogConversa(db.Model):
    __tablename__ = 'logs_conversa'

    id_log = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_idoso = db.Column(db.Integer, db.ForeignKey('idosos.id_idoso'), nullable=True)
    mensagem = db.Column(db.String(500), nullable=False)
    origem = db.Column(db.String(10), nullable=False) # 'idoso', 'familiar', 'bot'
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

class LoginTentativa(db.Model):
    __tablename__ = 'login_tentativas'

    id_tentativa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_familiar = db.Column(db.Integer, db.ForeignKey('familiares.id_familiar'), nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
    sucesso = db.Column(db.Boolean, nullable=False)
    ip = db.Column(db.String(45))