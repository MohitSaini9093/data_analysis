# a vibe coding
# python 3.8.0
# version 1.0

from flask import Flask,Blueprint
from routes.home import home
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(home)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
CORS(app)
# Ensure upload directory exists
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
