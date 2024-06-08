from flask import render_template,Flask,session,request,redirect,jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app=Flask(__name__)

heart_count=0

@app.route('/home')
def home():
    global heart_count
    heart_count=heart_count+1
    return jsonify({"message" : "Hello from Server: {}".format(os.getenv('ID')),"status" : "successful"})

@app.route('/heartbeat')
def heartbeat():
    return jsonify({"responce" :heart_count,"status" : "successful"})

port=os.getenv('port')
if port==None:
    port=5001

print('My port:',port)
app.run(host='0.0.0.0', port=port, debug=True)