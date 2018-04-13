import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify

import sys
sys.path.append("/Users/Amrit/Desktop/hrc2/web_tble_native/flaskr/flaskr/arch_eval/")

from Evaluator import Evaluator

app = Flask(__name__) # create the application instance :)
app.secret_key = 'daphne'

evaluator = Evaluator()

@app.route('/')
def index():
	flash("welcome")
	return render_template('index.html')

@app.route('/_evaluate')
def evaluate():
	bS = request.args.get('bitString', "000000000000000000000000000000000000000000000000000000000000", type=str)
	c, s, e = evaluator.eval_arch(bS)
	return jsonify(science=s, cost=c, estimation = e)