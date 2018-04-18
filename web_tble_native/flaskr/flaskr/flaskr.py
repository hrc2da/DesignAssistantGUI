import os
import requests
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify

import sys
sys.path.append("/Users/Amrit/Desktop/hrc2/web_tble_native/flaskr/flaskr/arch_eval/")

from arch_eval.Evaluator import Evaluator
from preferencelearner.preferencelearner import PreferenceLearner

app = Flask(__name__) # create the application instance :)
app.secret_key = 'daphne'

evaluator = Evaluator()

evalurl = 'https://www.selva-research.com/api/vassar/evaluate-architecture'

@app.route('/')
def index():
	flash("welcome")
	return render_template('index.html')

@app.route('/_evaluate')
def evaluate():
    bS = request.args.get('bitString', "000000000000000000000000000000000000000000000000000000000000", type=str)
    bSarr = bitstring2arr(bS)
    print bSarr
    r = requests.post(evalurl,json={'inputs':bSarr})
    print r.json()
    s, c = r.json()['outputs']
    return jsonify(science=s, cost=c)
    #c, s, e = evaluator.eval_arch(bS)
	#return jsonify(science=s, cost=c, estimation = e)
    #
    #return r.json().json
def bitstring2arr(bitstring):
    return str(map(lambda x : bool(int(x)),list(bitstring))).lower()
