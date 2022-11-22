import flask
from flask import request,render_template
from flask_cors import CORS
import sklearn

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "BTDm187YK74IQxUtzUMYLTNs0i31GWrlJ5GzIrQdGdWa"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app=flask.Flask(__name__,static_url_path='')
CORS(app)

@app.route('/',methods=['GET'])
def SendHomePage():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predictResult():
    a=float(request.form['age'])
    b=float(request.form['gender'])
    c=float(request.form['total_bilirubin'])
    j=float(request.form['direct_bilirubin'])
    d=float(request.form['alkaline_phosphotase'])
    e=float(request.form['alamine_aminotransferase'])
    f=float(request.form['aspartate_aminotransferase'])
    g=float(request.form['total_protiens'])
    h=float(request.form['albumin'])
    i=float(request.form['albumin_and_globulin_ratio'])

    x=[[a,b,c,j,d,e,f,g,h,i]]
    payload_scoring = {"input_data": [{"fields": [[a,b,c,j,d,e,f,g,h,i]], "values": x}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/059aad29-e5f5-4c73-9edb-89e123be4b34/predictions?version=2022-11-20', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions=response_scoring.json()
    predict=predictions['predictions'][0]['values'][0][0]
    print("Final Prediction :",predict)
    if(predict==2):
        res="Liver Disease Predicted"
    else:
        res="No Liver Disease Predicted"
    return render_template('predict.html',predict=res)

if __name__=='__main__':
    app.run(debug=False)