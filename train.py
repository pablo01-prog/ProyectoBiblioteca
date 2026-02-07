
# este archivo crea la "inteligencia local". Al ejecutarlo genera el archivo pkl

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib

# datos como ejemplo para entrenar

data = {
    'texto' : [
        'magia dragones espada guerrero aventura',
        'crimen detective asesinato misterio policia',
        'amor romance pareja enamorados boda',
        'futuro naves espaciales robots planetas',
        'fantasmas terror miedo susto sangre oscuro',
        'historia antigua guerra reyes imperio'
    ],
    'genero': [
        'Fantasia','Policial','Romance','Ciencia Ficcion','Terror','Historica'
    ]
}

# creacion de un data frame de los datos ejemplo
df = pd.DataFrame(data)

# creacion del modelo: vectorizador + algoritmo MultinomialNB

modelo = make_pipeline(TfidfVectorizer(), MultinomialNB())

# entrenamiento del modelo
modelo.fit(df['texto'], df['genero'])

# exportacion del modelo
joblib.dump(modelo, 'modelo_libros.pkl')

print("Modelo entrenado con exito. Archivo 'modelo_libros.pkl' creado.")