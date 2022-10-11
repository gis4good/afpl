# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 10:50:37 2022

@author: THIS-LAPPY
"""


from flask import Flask


app=Flask(__name__)
@app.route('/home/')
def world():
    x='hello home'
    return x
    
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    app.run(threaded=True, port=5000)    