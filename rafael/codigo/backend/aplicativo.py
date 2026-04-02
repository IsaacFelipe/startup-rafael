# aplicativo.py
from flask import Flask, jsonify
from configurações import Config
from modelos import db
from rotas import api  # Importa o blueprint corrigido
from flask_cors import CORS
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    logging.basicConfig(level=logging.INFO)
    CORS(app, origins="*") 

    db.init_app(app)

    # Registra as rotas com o prefixo /api
    # Isso transforma '/auth/registro' em '/api/auth/registro'
    app.register_blueprint(api, url_prefix='/api')

    # Rota Raiz para teste rápido de saúde da API
    @app.route('/')
    def index():
        return jsonify({"status": "online", "mensagem": "Backend Startup Rafael rodando!"}), 200

    with app.app_context():
        try:
            # Cria tabelas se não existirem (mas prefira usar o script SQL no MySQL Workbench)
            db.create_all()
            app.logger.info("Verificação de banco de dados concluída.")
        except Exception as e:
            app.logger.error(f"Erro ao conectar no banco: {e}")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)