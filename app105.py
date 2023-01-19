from flask import Flask, render_template, url_for, redirect, request, session
import joblib
import numpy as np


app = Flask(__name__)

model1 = 'models/classi_jb.aiml'
loaded_model_v1 = joblib.load(model1)
predictiondicts = {2: "Benign Tumor", 4: "Malignant Tumor"}

model2 = 'models/regre_jb.aiml'
loaded_model_v2 = joblib.load(model2)

@app.route('/')
def index():

  return render_template('classi.html')

@app.route('/regression')
def regression():

  return render_template('regre.html')


@app.route('/classification-prediction', methods=["GET", "POST"])
def classi():

  clump_val = request.form.get("clump", False)
  ucsize_val = request.form.get("ucsize", False)
  ucshape_val = request.form.get("ucshape", False)
  marAd_val = request.form.get("marAd", False)
  secs_val = request.form.get("secs", False)
  bare_val = request.form.get("bare", False)
  bland_val = request.form.get("bland", False)
  normNuc_val = request.form.get("normNuc", False)
  mitosis_val = request.form.get("mitosis", False)
  
  clump = float(clump_val)
  ucsize = float(ucsize_val)
  ucshape = float(ucshape_val)
  marAd = float(marAd_val)
  secs = float(secs_val)
  bare = float(bare_val)
  bland = float(bland_val)
  normNuc = float(normNuc_val)
  mitosis = float(mitosis_val)

  classi_val = [[clump, ucsize, ucshape, marAd, secs, bare, bland, normNuc, mitosis]]

  classi_pred = loaded_model_v1.predict(classi_val)    
  predicted = predictiondicts[classi_pred[0]]   

  return render_template('classi.html', Prediction=predicted)



@app.route('/regression-prediction', methods=["GET", "POST"])
def regre():

  age_val = request.form.get("age", False)
  sex_val = request.form.get("sex", False)
  bmi_val = request.form.get("bmi", False)
  children_val = request.form.get("children", False)
  smoker_val = request.form.get("smoker", False)

  region_val = request.form.get("region", False)
  if region_val == '1':
    rNE_val = 1
    rNW_val = 0
    rSE_val = 0
    rSW_val = 0
  
  elif region_val == '2':
    rNE_val = 0
    rNW_val = 1
    rSE_val = 0
    rSW_val = 0

  elif region_val == '3':
    rNE_val = 0
    rNW_val = 0
    rSE_val = 1
    rSW_val = 0

  else:
    rNE_val = 0
    rNW_val = 0
    rSE_val = 0
    rSW_val = 1
  
  age = float(age_val)
  sex = float(sex_val)
  bmi = float(bmi_val)
  children = float(children_val)
  smoker = float(smoker_val)

  rNE = float(rNE_val)
  rNW = float(rNW_val)
  rSE = float(rSE_val)
  rSW = float(rSW_val)



  regre_val = [[age, sex, bmi, children, smoker, rNE, rNW, rSE, rSW]]
  regre_pred = loaded_model_v2.predict(regre_val)
  
  regre_pred = float(regre_pred)
  ss = "{:,.2f}".format(regre_pred)
  
  formatted_res = "$" + str(ss) 

  return render_template('regre.html', Predict=formatted_res)



if __name__ == "__main__":
  app.run(debug=True)