# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 10:50:37 2022

@author: THIS-LAPPY
"""


from flask import Flask


app=Flask(__name__)
@app.route('/home')
def world():
    x='hello home'
    return x
    


if __name__ == '__main__':
    app.run(host='172.16.2.101',port=8001,debug=False)    