import math
import numpy as np
import pandas as pd
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt 
plt.style.use('fivethirtyeight')

def predictionsExpense(gastos):
    # Convetir los datos en dataframe
    dataFrame=pd.DataFrame(gastos, columns=['gastos'])
    dataGastos=dataFrame.values

    training_data_len=math.ceil(len(dataGastos)*.8) # 80% de los datos son para entrenamiento

    # Scalar los datos
    scaler=MinMaxScaler(feature_range=(0,1))
    scaled_data=scaler.fit_transform(dataGastos)

    # Crear los datos de entrenamiento
    train_data=scaled_data[0:training_data_len, :]

    x_train=[]
    y_train=[]

    for x in range(60, len(train_data)):
        x_train.append(train_data[x-60:x, 0])
        y_train.append(train_data[x, 0])

    # Convertir los datos a un numpy array
    x_train, y_train=np.array(x_train), np.array(y_train)

    # Reshapear los datos
    x_train=np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_train.shape

    # Construir el modelo LSTM
    model=Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(LSTM(50, return_sequences=False)) 
    model.add(Dense(25))
    model.add(Dense(1))

    # Compilar el modelo
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Entrenar el modelo
    model.fit(x_train, y_train, batch_size=1, epochs=1)

    test_data=scaled_data[training_data_len-60:, :]

    # Crear los datos de prueba
    x_test=[]
    for x in range(60, len(test_data)):
        x_test.append(test_data[x-60:x, 0])

    # Convertir los datos a un numpy array
    x_test=np.array(x_test)

    # Reshapear los datos
    x_test=np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    # Obtener los valores de prediccion
    predictions=model.predict(x_test)
    predictions=scaler.inverse_transform(predictions)
    predictionsGastos=predictions.flatten().tolist()
    
    return predictionsGastos