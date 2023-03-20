from flask import Flask, Response, redirect, render_template, request, Markup, jsonify
import numpy as np
import pandas as pd
import sklearn
from utils.map import func
from utils.bar import bar
from utils.deg import deg
import requests
import config
import pickle
import os
# from utils.model import ResNet9

data = pd.read_csv('Data/data1.csv')
app = Flask(__name__,static_folder='static')

model1 = pickle.load(open('RandomForest.pkl','rb'))
model2 = pickle.load(open('fertilizer.pkl','rb'))

@ app.route('/')
def index():
    return render_template('index.html')

@ app.route('/main',methods=["POST","GET"])
def main():
    return render_template('main.html')

@ app.route('/terms')
def terms():
    return render_template('terms.html')

@ app.route('/policy')
def policy():
    return render_template('policies.html')

@ app.route('/tech')
def tech():
    map = func()
    map.save('templates/f.html')
    return render_template('base.html')

@app.route('/map')
def map_1():
    return render_template('f.html')

@app.route('/models', methods=['POST'])
def models():
    distances = [(float(row["Latitude"]) - float(request.form['lat']))**2 + (float(row["Longitude"]) - float(request.form['lng']))**2 for _, row in data.iterrows()]
    index = min(range(len(distances)), key=distances.__getitem__)
    l1 = [request.form['ph'],request.form['p'],request.form['k'],request.form['s']]
    l1 = list(map(float,l1))
    l2 = [data.loc[index]["predictions_pH"],data.loc[index]["predictions_P"],data.loc[index]["predictions_K"],data.loc[index]["predictions_S"]]
    bar(os.path.join(app.static_folder, 'images', 'barplot.png'),l1,l2)
    pred1 = model1.predict([[request.form['p'],request.form['k'],request.form['ph']]])
    pred2 = model2.predict([[request.form['ph'],request.form['p'],request.form['k'],request.form['s'],request.form['oc']]])
    output = {"crop":pred1[0],"fert":pred2[0]}
    normal = {"ph":request.form['ph'],"p":request.form['p'],"s":request.form['s'],"k":request.form['k']}
    preds = {"ph":data.loc[index]["predictions_pH"],"p":data.loc[index]["predictions_P"],"s":data.loc[index]["predictions_S"],"k":data.loc[index]["predictions_K"]}
    return render_template('model.html',output=output,deg=deg(normal,preds),lat=request.form['lat'],pred=preds,lng=request.form['lng'],soil=request.form['soil'],s=request.form['s'],p=request.form['p'],k=request.form['k'],ph=request.form['ph'],oc=request.form['oc'])

@ app.route('/tech', methods=['POST'])
def tech_post():
    if request.method =="POST":
        lat = float(request.form['lat'])
        lng = float(request.form['lng'])
        distances = [(float(row["Latitude"]) - lat)**2 + (float(row["Longitude"]) - lng)**2 for _, row in data.iterrows()]
        index = min(range(len(distances)), key=distances.__getitem__)
        return Response(data.loc[index].to_json(orient="index"), mimetype='application/json')

if __name__ == "__main__":
    app.run(port=8888,debug=False)