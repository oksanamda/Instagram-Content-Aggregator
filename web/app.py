from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import random
import time

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

db = list()  # The mock database

posts = 500  # num posts to generate

quantity = 20  # num posts to return per request

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form.to_dict()
        # блок try-except - проверка на int
        try:
            return redirect(url_for("load", instalogin = int(data['instalogin'])))
        except:
            return redirect(url_for('result'))
    return render_template('index.html')


@app.route('/result')
def result():
    return render_template('result_page.html')


@app.route("/result/load/<instalogin>")
def load(instalogin=0):
    """ Route to return the posts """

    time.sleep(0.2)  # Used to simulate delay

    # смотри если будет нужно задать определенное число начиная с которого будут 
    # заливаться посты то тогда это можно прислать в запросе как counter
    # пока фиксируем counter, но как только ты придумаешь интерфейс, я могу реализовать это
    # то же самое и с quantity
    # Милена

    #if request.args:
    #    counter = int(request.args.get("c"))  # The 'counter' value sent in the QS

    counter = int(instalogin)
    if counter <= 0:
        print(f"Returning posts 0 to {quantity}")
        # Slice 0 -> quantity from the db
        res = make_response(jsonify(db[0: quantity]), 200)

    elif counter >= posts:
        print("No more posts")
        res = make_response(jsonify({}), 200)

    else:
        print(f"Returning posts {counter} to {counter + quantity}")
        # Slice counter -> quantity from the db
        res = make_response(jsonify(db[counter: counter + quantity]), 200)

    return res

if __name__ == '__main__':
    app.run(debug = True)