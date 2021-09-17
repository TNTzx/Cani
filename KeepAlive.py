# this code is copypasted lmao help

from flask import Flask
from threading import Thread
from flask import Flask, jsonify, request
import json, os, signal


app = Flask('')

@app.route('/')
def home():
    return "Helloooo!"
  

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()