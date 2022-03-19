from flask import Flask, render_template, request
from matplotlib.style import context
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type=request.form['Fuel_Type']
        if(Fuel_Type=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        elif(Fuel_Type =='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        Year=2022-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output=round(prediction[0],2)

        if (output<5):
            image = "less_than_5"
        elif (output>=5 and output <10):
            image= "5-10"
        elif (output>=10 and output <20):
            image = "10-20"
        elif (output>=20 and output <50):
            image = "20-50"
        elif (output>=50):
            image= "above_50"

        image_url = "../static/images/{}.jpg".format(image)

        if output<0:
            prediction_text = "Sorry You can not sell this car."
        else:
            prediction_text="Your Car is worth for around {} lakhs. You can sell this car at this Price.".format(output)

        print(prediction_text)
        print(image_url)

        return render_template('predict.html',prediction_text=prediction_text,image_url=image_url)
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)