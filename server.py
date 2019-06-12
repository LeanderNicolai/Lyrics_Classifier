"""Server file for the movie recommender flask app"""
from flask import Flask, render_template, request
from pa_func_base import tmp_flask

APP = Flask(__name__)


@APP.route('/')
def hello_world():

    return render_template('main.html')


@APP.route('/results')
def predictions():
    query_string = request.args['Movie1'] + '$$' + \
        request.args['Movie2'] + '$$' + \
        request.args['Movie3']
    print('type of query string is: ', type(query_string))
    print(query_string)
    qs = tmp_flask(query_string)
    print("QS IS: ", qs)
    # if len(query_string) > 1:
    #     query_string = 'test'
    # qs = tmp_flask(query_string)
    # print(qs)
    return render_template('results.html', results=query_string, pred=qs)
