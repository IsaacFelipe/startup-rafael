# rotas.py
from flask import Blueprint, jsonify, request, current_app
from modelos import db, Familiar, LoginTentativa
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import sqlalchemy.exc

# 1. Definição do Blueprint
api = Blueprint('api', __name__)

# Helpers
def ip_from_request(req):
    if req.headers.get('X-Forwarded-For'):
        return req.headers.get('X-Forwarded-For').split(',')[0].strip()
    return req.remote_addr or 'unknown'

# --- ROTAS ---
# Note que removemos o "/api" do início. O aplicativo.py vai adicionar isso.

@api.route('/auth/registro', methods=['POST'])
def registro():
    data = request.get_json() or {}
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    telefone = data.get('telefone')

    if not nome or not email or not senha:
        return jsonify({"erro": "nome, email e senha são obrigatórios"}), 400

    if Familiar.query.filter_by(email=email).first():
        return jsonify({"erro": "Email já cadastrado"}), 409

    hashed = generate_password_hash(senha)

    novo = Familiar(
        nome=nome,
        email=email,
        senha_hash=hashed,
        telefone=telefone
    )

    try:
        db.session.add(novo)
        db.session.commit()
        return jsonify(novo.to_dict()), 201
    except sqlalchemy.exc.SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar familiar: {e}")
        return jsonify({"erro": "Erro interno ao criar usuário"}), 500

@api.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({"erro": "email e senha são obrigatórios"}), 400

    familiar = Familiar.query.filter_by(email=email).first()
    ip = ip_from_request(request)

    if not familiar:
        return jsonify({"erro": "Credenciais inválidas"}), 401

    # Lógica de bloqueio (5 tentativas em 15 min)
    window = datetime.utcnow() - timedelta(minutes=15)
    falhas_recentes = LoginTentativa.query.filter(
        LoginTentativa.id_familiar == familiar.id_familiar,
        LoginTentativa.data_hora >= window,
        LoginTentativa.sucesso == False
    ).count()

    if falhas_recentes >= 5:
        return jsonify({"erro": "Conta bloqueada temporariamente. Tente em 15 min."}), 403

    if check_password_hash(familiar.senha_hash, senha):
        tentativa = LoginTentativa(id_familiar=familiar.id_familiar, sucesso=True, ip=ip)
        db.session.add(tentativa)
        db.session.commit()
        return jsonify({"msg": "Login bem-sucedido", "familiar": familiar.to_dict()}), 200
    else:
        tentativa = LoginTentativa(id_familiar=familiar.id_familiar, sucesso=False, ip=ip)
        db.session.add(tentativa)
        db.session.commit()
        return jsonify({"erro": "Credenciais inválidas"}), 401

@api.route('/familiares/<int:id_familiar>', methods=['GET'])
def get_familiar(id_familiar):
    fam = Familiar.query.get_or_404(id_familiar)
    return jsonify(fam.to_dict()), 200

@api.route('/familiares', methods=['GET'])
def listar_familiares():
    familiares = Familiar.query.all()
    return jsonify([f.to_dict() for f in familiares]), 200