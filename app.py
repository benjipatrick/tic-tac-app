
from flask import Flask, send_from_directory, request, jsonify
from flask_restful import Api, Resource, reqparse
# from flask_cors import CORS #comment this on deployment
from ticTacML.TicTacToe import TicTacToe
from ticTacML.Players import monte_carlo_player

import numpy as np

app = Flask(__name__, static_url_path='', static_folder='tic-tac-web-app/build')
# CORS(app) #comment this on deployment

game = TicTacToe()
monte_carlo_player = monte_carlo_player(game, iters=10000)

@app.route('/game/status', methods = ['POST'])
def result():
    return jsonify(getStatus(request.data))

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')


def getStatus(data):
    board = []
    data = data.decode("utf-8")
    turn = 0
    for c in data:
        if c == 'n': 
            board.append(None)
        elif c == 'O': 
            board.append(-1)
            turn += 1
        elif c == 'X': 
            board.append(1)
            turn += 1
    return game.get_game_status(board, turn), monte_carlo_player.play(board, -1, turn)
  