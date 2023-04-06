# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 10:50:37 2022

@author: THIS-LAPPY
"""


from flask import Flask
import geopy.distance
from flask import request
from collections.abc import Mapping


app=Flask(__name__)
@app.route('/home/')
def world():
    x='hello home'
    return x
    
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


@app.route('/dist/',methods=['GET'])
def distance():
    try:
        x1 = request.args.get('x1')
        x2 = request.args.get('x2')
        y1 = request.args.get('y1')
        y2 = request.args.get('y2')
        coords_1 = (x1,y1)
        coords_2 = (x2,y2)
        dist=geopy.distance.geodesic(coords_1, coords_2).km
        dist={'Distance (Km)':dist}
    
        return dist
    except Exception as e:
        err={'Error':str(e)}
        return err
        

if __name__ == '__main__':
    app.run()  