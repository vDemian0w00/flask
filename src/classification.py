import json
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
import numpy as np

# Clasificacion
class Classification_DG:
    # Gastos que se pagan en un periodo de tiempo frecuente y la cantidad es siempre igual o llega a variar muy poco (NECESARIOS)
    FRE_IMP = "Frecuente Imprescindible"
    # Gastos que se pagan en un periodo de tiempo frecuente y la cantidad es siempre igual o llega a variar muy poco (PUEDEN EVITARSE)
    FRE_PRE = "Frecuente Prescindible"
    # Subcategoria de gasto diario (NECESARIOS)
    VAR_IMP = "Variable Imprescindible"
    # Subcategoria de gasto diario (PUEDEN EVITARSE)
    VAR_PRE = "Variable Prescindible"
    # Gastos pequeños que se realizan cada día y que suman mucho al final del mes
    HORMIGA = "Hormiga"
    # Gastos que no se pueden prever y que se realizan en un momento dado
    IMPREVISTOS = "Imprevisto"

class Review:
    def __init__(self, name, description, classification):
        self.name = name
        self.description = description
        self.classification = classification

class ReviewContainer:
    def __init__(self, reviews):
        self.reviews = reviews

    def get_dataSet(self):
        return np.array([f'{x.name} - {x.description}' for x in self.reviews])

    def get_x(self, vectorizer):
        data_vector = vectorizer.transform(self.get_dataSet())
        return data_vector

    def get_y(self):
        return np.array([x.classification for x in self.reviews])

file_names = np.array(['./data/classification/fre_imp.json', './data/classification/fre_pre.json', './data/classification/var_imp.json',
                        './data/classification/var_pre.json', './data/classification/hormiga.json', './data/classification/imprevistos.json'])
file_categories = np.array([Classification_DG.FRE_IMP, Classification_DG.FRE_PRE, Classification_DG.VAR_IMP,
                            Classification_DG.VAR_PRE, Classification_DG.HORMIGA, Classification_DG.IMPREVISTOS])

reviews = []
for i in range(len(file_names)):
    file_name = file_names[i]
    classification = file_categories[i]
    with open(file_name, 'r', encoding='utf-8') as f:
        data = f.read()
        review_json = json.loads(data)
        for review_from_json in review_json:
            review = Review(
                review_from_json['name'], review_from_json['description'], classification)
            reviews.append(review)


# Preparar los datos para la clasificacion
# 60% para entrenamiento y 40% para pruebas
train, _ = train_test_split(reviews, test_size=0.4, random_state=42)
train_container = ReviewContainer(train)

# Vectorizacion de datos
corpus = train_container.get_dataSet()
vectorizer = TfidfVectorizer()
vectorizer.fit(corpus)

# Entrenamiento de datos
train_x = train_container.get_x(vectorizer)
train_y = train_container.get_y()

# Clasificador
clf = svm.SVC(C=16, kernel='linear', gamma='auto')
clf.fit(train_x, train_y)


def classificationExpense(gasto):
    test_set = [gasto]
    new_test = vectorizer.transform(test_set)

    return clf.predict(new_test)[0]
