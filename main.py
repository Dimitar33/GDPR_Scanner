from flask import Flask

app = Flask(__name__)

@app.route('/')

def hello():
    return "Hello, GDPR scanner!"


@app.route('/bye/<name>')
def buy(name):
    return f"bye, {name}!"

if __name__ == '__main__':
    app.run(debug=True)