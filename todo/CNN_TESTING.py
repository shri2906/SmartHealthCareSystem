
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from keras.models import load_model

from .symptoms_list import *

import os


def get_result(symptoms_inserted):


    path = os.getcwd()
    print(path)

    sym = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for k in range(0,len(sym)):
        for z in symptoms_inserted:
            if(z==symptoms[k]):
                sym[k-1]=1
##    print(sym)

    data=pd.read_csv(path + "/todo/" +  "Training.csv")
    genre_list = data.iloc[:, -1]
    encoder = LabelEncoder()
    y = encoder.fit_transform(genre_list)

    model = load_model(path + "/todo/" + 'NN.h5')

    ##sym = [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    symptoms_to_algorithm = np.array([sym])
    predictions = model.predict(symptoms_to_algorithm)
    acc =  "%.2f" % round((max(predictions[0]) * 100),2)

    result_encoded = np.argmax(predictions[0])

    result = encoder.inverse_transform([result_encoded])

    data=pd.read_csv(path + "/todo/" + "Health_Doctor_excercise_diet.csv")

    doctor = data['Doctor']
    exercise = data['exercise']
    diet = data['diet']
    Diseases = data['disease_name']
    medicine = data['medicine']

    ##print(Diseases)
    for i in range (0,len(Diseases)):
        if(Diseases[i]==result[0]):
            break

    doctor_info = doctor[i]
    exercise_info = exercise[i]
    diet_info = diet[i]
    medicine_info = medicine[i]

    return result[0],acc,doctor_info,exercise_info,diet_info,medicine_info

