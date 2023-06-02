import numpy as pd
import pandas as pd
import random
import xgboost as xgb


def create_features(df):
    df = df.copy()
    df['index'] = range(1, len(df) + 1)
    return df


def predictionExpense(gastos):
    minValue = min(gastos)
    maxValue = max(gastos)

    # Generar 30 números aleatorios
    for _ in range(30):
        dataPrediction = round(random.uniform(minValue, maxValue), 2)
        gastos.append(dataPrediction)

    # Convertir los datos en un DataFrame
    dataFrame = pd.DataFrame(gastos, columns=['gastos'])

    df = create_features(dataFrame)

    FEATURES = ['index']
    TARGET = 'gastos'

    X_train = df[FEATURES]
    y_train = df[TARGET]

    reg = xgb.XGBRegressor(base_score=0.5, booster='gbtree',
                           n_estimators=1000,
                           early_stopping_rounds=50,
                           objective='reg:squarederror',
                           max_depth=3,
                           learning_rate=0.01)
    reg.fit(X_train, y_train,
            eval_set=[(X_train, y_train)],
            verbose=100)

    df['prediction'] = reg.predict(X_train)

    last_30_predictions = df['prediction'].tail(30).tolist()
    return last_30_predictions
