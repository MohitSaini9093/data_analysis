# a vibe coding
# python 3.8.0
# version 1.0

from flask import Flask,Blueprint
from routes.home import home
from flask_cors import CORS

app = Flask(__name__)
app.secret_key='\x892J\xf0o\x0f\x84\x859\x966\x99\xe2\xdb\xdf\xaa\x02\x0e\x994\xa7U\x8a\xfe'
app.register_blueprint(home)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
CORS(app, supports_credentials=True)
# Ensure upload directory exists
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
