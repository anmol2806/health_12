#app.py
from flask import Flask,request, url_for, redirect, render_template, jsonify
import sqlite3 as sql
from flask_cors import CORS, cross_origin
import pickle
import numpy as np
#from sklearn.externals import joblib
#import sklearn.external.joblib as extjoblib
import joblib

app = Flask(__name__)
# load the saved model file and use for prediction
logit_model = joblib.load('heart_disease.pkl')
logit_model_diabetes = joblib.load('logit_diabetes_model.pkl')
logit_model_bmi=joblib.load(open('clf.pkl','rb'))




@app.after_request # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


# ==================================
#  Insert data in database (SIGNUP)
# ==================================
def insertUser(username, email, password, contact):
    con = sql.connect("test.db")
    cur = con.cursor()
    phone = int(contact)
    query = ("""INSERT INTO USERS
             (username,email,password,contact)
             VALUES ('%s','%s','%s',%d)""" %
             (username, email, password, phone))
    cur.execute(query)
    con.commit()
    con.close()


# =====================================
#  Validating data in database (LOGIN)
# =====================================
def validUser(email, password):
    con = sql.connect("test.db")
    cur = con.cursor()
    query = ("""SELECT * FROM USERS
             where email = '%s' and password = '%s'
             """ %
             (email, password))
    cur.execute(query)
    data = cur.fetchall()
    con.close()
    return data


# ===================
#    Flask Routing
# ===================

@app.route('/')
def home111():
    return render_template('login_1.html')

# Login page
@app.route('/signin/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        rd = validUser(request.form['email'], request.form['password'])
        if rd:
            return render_template('homepage_1.html')
        else:
            return "UnSucessful login"
    else:
        return render_template('login_1.html')


# Signup page
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        contact = request.form['contact']
        insertUser(username, email, password, contact)
        return redirect(url_for('login'))
    else:
        return render_template('login_1.html')

# api json 
@app.route('/sum', methods=['GET','POST'])
def sum():
    sum = 0
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    sum = a+b
    return jsonify(sum)


@app.route('/mainpage')
def mainhome():
    return render_template("homepage_1.html")


@app.route('/heart')
def home1():
    return render_template("indexheart.html")
# Always at end of file !Important!

@app.route('/heart/predict',methods=['POST','GET'])
def predict1():
    # receive the values send by user in three text boxes thru request object -> requesst.form.values()
    
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    print(final_features)
       
    prediction1=logit_model.predict(final_features)
    if prediction1 == 1:
        pred = "You have Heart Disease, please consult a Doctor."
    elif prediction1 == 0:
        pred = "You don't have Heart Disease."
    output = pred
   
    return render_template('heart_pred.html', pred= '{}'.format(output))
    
    
    
    
    
@app.route('/diabetes')
def home2():
    return render_template('index_diabetes.html')  

@app.route('/diabetes/predict',methods=['POST'])
def predict2():
    '''
    For rendering results on HTML GUI
    '''
    float_features = [float(x) for x in request.form.values()]
    final_features1 = [np.array(float_features)]
    prediction2 = logit_model_diabetes.predict(final_features1 )

    if prediction2 == 1:
        pred = "You have Diabetes, please consult a Doctor."
    elif prediction2 == 0:
        pred = "You don't have Diabetes."
    output = pred

    return render_template('index_diabetes.html', prediction_text='{}'.format(output))
    





@app.route('/bmi')
def home3():
    return render_template("bmi_theory.html")


@app.route('/bmi/predict',methods=['POST','GET'])
def predict3():
    int_features = [int(x) for x in request.form.values()]
    y=int_features[2]/(int_features[1]*0.0254)**2
    int_features.append(y)
    final_features = [np.array(int_features)]
    prediction=logit_model_bmi.predict(final_features)
    
    return render_template('bmi_theory.html', pred=prediction)




    
if __name__== '__main__':
    app.run(debug=True)
    