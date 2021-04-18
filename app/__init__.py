from flask import Flask

app = Flask(__name__)
app.secret_key = 'b_5#y2LF4Q8z\n\xec]/'

if __name__ == '__main__':
    app.run(debug=True)
from app import routes