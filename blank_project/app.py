from flask import Flask, request, url_for, redirect
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        return "Hello World!"

if __name__ == '__main__':
    app.run()
