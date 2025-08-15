import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from src.models.user import db
from src.routes.user import user_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

app.register_blueprint(user_bp, url_prefix='/api')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    # Se for a rota raiz, servir diretamente o Start Dolar
    if path == "":
        start_dolar_path = os.path.join(static_folder_path, 'dolarclub.com.br', 'start-dolar', 'index.html')
        if os.path.exists(start_dolar_path):
            return send_from_directory(os.path.join(static_folder_path, 'dolarclub.com.br', 'start-dolar'), 'index.html')
        else:
            return "Start Dolar page not found", 404

    # Tentar servir arquivos estáticos com diferentes caminhos base
    possible_paths = [
        path,
        os.path.join('dolarclub.com.br', path),
        os.path.join('dolarclub.com.br', 'start-dolar', path)
    ]
    
    for possible_path in possible_paths:
        full_path = os.path.join(static_folder_path, possible_path)
        if os.path.exists(full_path):
            if os.path.isfile(full_path):
                return send_from_directory(static_folder_path, possible_path)
    
    # Se não encontrar, tentar servir da pasta wp-content
    if path.startswith('wp-content/'):
        wp_path = os.path.join(static_folder_path, 'dolarclub.com.br', path)
        if os.path.exists(wp_path):
            return send_from_directory(os.path.join(static_folder_path, 'dolarclub.com.br'), path)
    
    # Se ainda não encontrar, redirecionar para Start Dolar
    start_dolar_path = os.path.join(static_folder_path, 'dolarclub.com.br', 'start-dolar', 'index.html')
    if os.path.exists(start_dolar_path):
        return send_from_directory(os.path.join(static_folder_path, 'dolarclub.com.br', 'start-dolar'), 'index.html')
    else:
        return "Page not found", 404

@app.route('/startdolar/')
@app.route('/startdolar/index.html')
def start_dolar():
    """Rota para o site Start Dolar"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404
    
    start_dolar_path = os.path.join(static_folder_path, 'dolarclub.com.br', 'start-dolar', 'index.html')
    if os.path.exists(start_dolar_path):
        return send_from_directory(os.path.join(static_folder_path, 'dolarclub.com.br', 'start-dolar'), 'index.html')
    else:
        return "Start Dolar page not found", 404

@app.route('/start-dolar/')
@app.route('/start-dolar/index.html')
def start_dolar_alt():
    """Rota alternativa para o site Start Dolar"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404
    
    start_dolar_path = os.path.join(static_folder_path, 'dolarclub.com.br', 'start-dolar', 'index.html')
    if os.path.exists(start_dolar_path):
        return send_from_directory(os.path.join(static_folder_path, 'dolarclub.com.br', 'start-dolar'), 'index.html')
    else:
        return "Start Dolar page not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
