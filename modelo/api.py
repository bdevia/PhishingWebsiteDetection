from flask import Flask, request, jsonify
import main as mn
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score

# Leemos el .CSV
data = pd.read_csv("./datos/dataset_phishing.csv")

#drop columns
columnas_eliminar = ["random_domain", "domain_age", "dns_record", "page_rank", "nb_redirection", "nb_external_redirection", "nb_hyperlinks", "ratio_intHyperlinks", "ratio_extHyperlinks", "ratio_extRedirection", "ratio_extErrors", "external_favicon", "links_in_tags", "ratio_intMedia", "domain_with_copyright", "domain_registration_length", "google_index"]
data_final = data.drop(columnas_eliminar, axis=1)
data_final["status"] = data_final.status.map({"legitimate": 0, "phishing":1})
mapeo = ["legitimate", "phishing"]

# Separamos los conjuntos
Y = np.array(data_final["status"])
data_final.drop(["url", "status"], inplace=True, axis=1)
X = np.array(data_final)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

# Creamos el Random Forest
rf_classifier = RandomForestClassifier(n_estimators=200, random_state=42)

# Entrenamos
rf_classifier.fit(X_train, Y_train)

# Predecimos
y_pred = rf_classifier.predict(X_test)

# Metricas
precision = precision_score(Y_test, y_pred)
recall = recall_score(Y_test, y_pred)
f1 = f1_score(Y_test, y_pred)

print("Metricas del modelo:\n")
print("Precisión:","%.2f" % (precision*100),"%")
print("Recall:", "%.2f" % (recall*100),"%")
print("F1 score:", "%.2f" % f1)
print("---------------------------------\n")

#nuevos_parametros = datos de la pagina
# Convertir el vector de parámetros a un array de numpy
#nuevos_parametros = np.array([nuevos_parametros])

# Realizar la predicción utilizando el modelo entrenado
#prediccion = best_model.predict(nuevos_parametros)

#print(prediccion)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return 'Escuchando en puerto 8080'

@app.route('/save_url', methods=['POST'])
def guardar_url():
    datos = request.get_json()
    print("Añadiendo URL:", datos['url'])
    
    vector = mn.vector_data(datos['url'])  # Vector a agregar
    vector = np.array(vector).reshape(1, -1)
    
    X_train_new = np.vstack((X_train, vector))

    Y_train_new = np.append(Y_train, 0)

    rf_classifier.fit(X_train_new, Y_train_new)
    
    reply = {'status': 'OK'}
    return jsonify(reply)

@app.route('/get_url', methods=['POST'])
def recibir_solicitud():
    datos = request.get_json()
    print(datos['url'])
    
    vector = mn.vector_data(datos['url'])
    #print(vector)
    #reply = {'status': 'OK'}
    
    new_prediction = rf_classifier.predict(np.array(vector).reshape(1, -1))
    
    if new_prediction[0] == 1:
        reply = {'status': 1}
        print(datos['url']," is phishing")
    else:
        reply = {'status': 0}
        print(datos['url']," is legitimate")
    return jsonify(reply)

if __name__ == '__main__':
    app.run(port=8080)  # Establece el puerto en 8080