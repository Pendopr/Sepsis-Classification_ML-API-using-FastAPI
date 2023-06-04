#importing packages
from fastapi import FastAPI
import uvicorn
import joblib
import sklearn
import pandas as pd
import numpy as np
import os

#creating an instance of fastapi
app = FastAPI(title ="API")


def load_model():
    cwd = os.getcwd()
    destination = os.path.join(cwd, "key_comp")

    imputer_filepath = os.path.join(destination, "numerical_imputer.joblib")
    scaler_filepath = os.path.join(destination, "scaler.joblib")
    model_filepath = os.path.join(destination, "lr_model.joblib")

    num_imputer = joblib.load(imputer_filepath)
    scaler = joblib.load(scaler_filepath)
    model = joblib.load(model_filepath)

    return num_imputer, scaler, model

def preprocess_input_data(df, num_imputer, scaler):
    input_data_df = pd.DataFrame([df])
    num_columns = [col for col in input_data_df.columns if input_data_df[col].dtype != 'object']
    input_data_imputed_num = num_imputer.transform(input_data_df[num_columns])
    input_scaled_df = pd.DataFrame(scaler.transform(input_data_imputed_num), columns=num_columns)
    return input_scaled_df


@app.get("/")
def read_root():
    return {"API": "A classification machine learning fastapi..."}

# ML endpoit
@app.get("/predict/{PRG}/{PL}/{PR}/{SK}/{TS}/{M11}/{BD2}/{Age}/{Insurance}")
def predict(PRG:int,PL:int,PR:int,SK:int,TS:int,M11:float,BD2:float,Age:int,Insurance:int):
    #creat a dataframe of the input data
    num_imputer, scaler, model = load_model()
   
    df = {
        'PRG':PRG,
        'PL':PL,
        'PR':PR,
        'SK':SK,
        'TS':TS,
        'M11':M11,
        'BD2':BD2,
        'Age':Age,
        'Insurance':Insurance
    }
    
    input_scaled_df = preprocess_input_data(df, num_imputer, scaler)
    
    probabilities = model.predict_proba(input_scaled_df)[0]
    prediction = np.argmax(probabilities)

    sepsis_status = "Positive" if prediction == 1 else "Negative"
    
    probability = probabilities[1] if prediction == 1 else probabilities[0]

    if prediction == 1:
        status_icon = "✔"   # Red 'X' icon for positive sepsis prediction
        sepsis_explanation = "which suggests that the patient is exhibiting sepsis symptoms and requires immediate medical attention."
    else:
        status_icon = "✘"  # Green checkmark icon for negative sepsis prediction
        sepsis_explanation = "which suggests that the patient is not currently exhibiting sepsis symptoms."

    statement = f"The patient's sepsis status is {sepsis_status} {status_icon} with a probability of {probability:.2f},{sepsis_explanation}"

    output_df = pd.DataFrame([df])

    result = {'predicted_sepsis': sepsis_status, 'statement': statement, 'input_data_df': output_df.to_dict('records')}

    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)


