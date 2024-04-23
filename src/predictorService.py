import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from os import getenv

label_encoder = LabelEncoder()

def dataSetNormalizer(dataSetPath):

    df = pd.read_csv(dataSetPath, delimiter=',')
    df['type'] = label_encoder.fit_transform(df['type'])

    x = df[['type', 'date']]
    y = df['price']

    return [x, y]


def trainModel(normedDataset): 
    x, y = normedDataset

    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=2)

    model = LinearRegression()

    model.fit(x_train, y_train)

    return model


def pricePredictor(car_type, date):
    dataset = dataSetNormalizer(getenv('DATASET_PATH'))
    model = trainModel(dataset)

    car_type_enc = label_encoder.transform([car_type])[0]
    print (car_type_enc, date)

    return model.predict([[car_type_enc, date]])[0].round(0)

